from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from core.ip_tracker import track_ip
from core.logger import get_logger
from services.ai_client import (
    DEFAULT_MODEL,
    AiClientError,
    build_chat_payload,
    build_headers,
    call_ai_with_retry,
    extract_message,
    get_api_key_from_payload,
    load_api_keys_masked,
    stream_ai_chat,
)

router = APIRouter()
logger = get_logger(__name__)


@router.get("/api/ai/keys")
async def api_ai_keys():
    keys = load_api_keys_masked()
    return {"count": len(keys), "keys": keys}


@router.post("/api/ai/chat")
async def api_ai_chat(payload: dict, request: Request):
    api_key = get_api_key_from_payload(payload)
    content = str(payload.get("content") or "").strip()
    model = str(payload.get("model") or DEFAULT_MODEL).strip()
    system = str(payload.get("system") or "").strip()

    if not api_key:
        logger.warning("AI请求失败：缺少API密钥")
        raise HTTPException(status_code=400, detail="missing api_key")
    if not content:
        logger.warning("AI请求失败：缺少内容")
        raise HTTPException(status_code=400, detail="missing content")

    logger.info(f"AI聊天请求 - 模型: {model}, 内容长度: {len(content)}")
    request_payload = build_chat_payload(model, content, system)
    headers = build_headers(api_key)

    try:
        result = await call_ai_with_retry(request_payload, headers)
        message = extract_message(result)
        logger.info(f"AI聊天成功 - 回复长度: {len(message)}")

        try:
            await track_ip(request, "AI对话", {})
        except Exception as exc:
            logger.warning(f"记录AI对话失败: {exc}")

        return {"message": message, "raw": result}
    except AiClientError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"AI聊天异常: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/api/ai/chat/stream")
async def api_ai_chat_stream(payload: dict, request: Request):
    api_key = get_api_key_from_payload(payload)
    content = str(payload.get("content") or "").strip()
    model = str(payload.get("model") or DEFAULT_MODEL).strip()
    system = str(payload.get("system") or "").strip()

    if not api_key:
        logger.warning("AI流式请求失败：缺少API密钥")
        raise HTTPException(status_code=400, detail="missing api_key")
    if not content:
        logger.warning("AI流式请求失败：缺少内容")
        raise HTTPException(status_code=400, detail="missing content")

    logger.info(f"AI流式聊天请求 - 模型: {model}, 内容长度: {len(content)}")

    try:
        await track_ip(request, "AI对话", {})
    except Exception as exc:
        logger.warning(f"记录AI对话失败: {exc}")

    request_payload = build_chat_payload(model, content, system, stream=True)
    headers = build_headers(api_key)
    return StreamingResponse(
        stream_ai_chat(request_payload, headers),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
