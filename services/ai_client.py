import asyncio
import json
from dataclasses import dataclass
from typing import Any, AsyncGenerator

import httpx

from core.config import APIKEY_PATH
from core.logger import get_logger

logger = get_logger(__name__)

AI_CHAT_URL = "https://api.siliconflow.cn/v1/chat/completions"
AI_TIMEOUT = 30.0
AI_STREAM_TIMEOUT = 90.0
AI_MAX_RETRIES = 3
DEFAULT_MODEL = "Qwen/QwQ-32B"


@dataclass
class AiClientError(Exception):
    status_code: int
    detail: str


def load_api_keys_raw(path: str = APIKEY_PATH) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        return []

    if isinstance(data, dict) and isinstance(data.get("keys"), list):
        return [str(value) for value in data["keys"]]
    if isinstance(data, list):
        return [str(value) for value in data]
    return []


def load_api_keys_masked(path: str = APIKEY_PATH) -> list[dict[str, Any]]:
    keys = []
    for index, key in enumerate(load_api_keys_raw(path)):
        if not key:
            masked = ""
        elif len(key) <= 6:
            masked = "***"
        else:
            masked = f"{key[:3]}***{key[-3:]}"
        keys.append({"index": index, "label": f"key{index + 1}", "masked": masked})
    return keys


def get_api_key_from_payload(payload: dict[str, Any], path: str = APIKEY_PATH) -> str:
    api_key = str(payload.get("api_key") or "").strip()
    key_index = payload.get("key_index")

    if api_key or key_index is None:
        return api_key

    try:
        index = int(key_index)
    except Exception:
        return ""

    keys = load_api_keys_raw(path)
    if 0 <= index < len(keys):
        return keys[index]
    return ""


def build_messages(content: str, system: str = "") -> list[dict[str, str]]:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": content})
    return messages


def build_chat_payload(model: str, content: str, system: str = "", stream: bool = False) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model or DEFAULT_MODEL,
        "messages": build_messages(content, system),
    }
    if stream:
        payload["stream"] = True
        payload["max_tokens"] = 4096
    return payload


def build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


async def call_ai_with_retry(
    request_payload: dict[str, Any],
    headers: dict[str, str],
    max_retries: int = AI_MAX_RETRIES,
) -> dict[str, Any]:
    last_error = ""

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"AI请求尝试 {attempt}/{max_retries}")
            async with httpx.AsyncClient(timeout=AI_TIMEOUT) as client:
                response = await client.post(AI_CHAT_URL, json=request_payload, headers=headers)
                response.raise_for_status()
                logger.info(f"AI请求成功 (尝试 {attempt}/{max_retries})")
                return response.json()
        except httpx.TimeoutException as exc:
            last_error = f"请求超时（{AI_TIMEOUT}秒）"
            logger.warning(f"AI请求超时 (尝试 {attempt}/{max_retries}): {exc}")
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            last_error = f"HTTP {status_code}"
            logger.warning(f"AI请求失败 HTTP {status_code} (尝试 {attempt}/{max_retries})")
            if 400 <= status_code < 500:
                raise AiClientError(502, f"AI API错误: HTTP {status_code}") from exc
        except Exception as exc:
            last_error = str(exc)
            logger.warning(f"AI请求异常 (尝试 {attempt}/{max_retries}): {exc}")

        if attempt < max_retries:
            await asyncio.sleep(attempt)

    logger.error(f"AI请求失败，已重试 {max_retries} 次: {last_error}")
    raise AiClientError(503, f"AI服务繁忙，请稍后再试（已重试{max_retries}次）")


def extract_message(result: dict[str, Any]) -> str:
    try:
        message = result.get("choices", [{}])[0].get("message", {}).get("content")
    except Exception:
        message = None
    return "" if message is None else str(message).lstrip("\r\n")


async def stream_ai_chat(
    request_payload: dict[str, Any],
    headers: dict[str, str],
) -> AsyncGenerator[str, None]:
    total_chars = 0
    try:
        async with httpx.AsyncClient(timeout=AI_STREAM_TIMEOUT) as client:
            async with client.stream("POST", AI_CHAT_URL, json=request_payload, headers=headers) as response:
                response.raise_for_status()
                buffer = ""
                async for chunk in response.aiter_bytes():
                    buffer += chunk.decode("utf-8")
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()
                        if not line or not line.startswith("data: "):
                            continue

                        data_text = line[6:]
                        if data_text.strip() == "[DONE]":
                            break

                        try:
                            data = json.loads(data_text)
                        except json.JSONDecodeError:
                            continue

                        delta = data.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            total_chars += len(content)
                            yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"

                logger.info(f"AI流式聊天成功 - 总字符数: {total_chars}")
                yield "data: [DONE]\n\n"
    except httpx.TimeoutException as exc:
        logger.error(f"AI流式请求超时: {exc}")
        error = json.dumps({"error": "AI服务繁忙，请稍后再试（请求超时）"}, ensure_ascii=False)
        yield f"data: {error}\n\n"
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        logger.error(f"AI流式请求失败 HTTP {status_code}")
        error = json.dumps({"error": f"AI服务繁忙，请稍后再试（HTTP {status_code}）"}, ensure_ascii=False)
        yield f"data: {error}\n\n"
    except Exception as exc:
        logger.error(f"AI流式请求异常: {exc}", exc_info=True)
        error = json.dumps({"error": "AI服务繁忙，请稍后再试"}, ensure_ascii=False)
        yield f"data: {error}\n\n"
