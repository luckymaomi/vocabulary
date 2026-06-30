import asyncio
import json

import pytest

from services.ai_client import (
    AiClientError,
    build_chat_payload,
    extract_message,
    get_api_key_from_payload,
    load_api_keys_masked,
    load_api_keys_raw,
)


def test_load_api_keys_from_dict(tmp_path):
    key_file = tmp_path / "keys.json"
    key_file.write_text(json.dumps({"keys": ["sk-alpha", "sk-beta"]}), encoding="utf-8")

    assert load_api_keys_raw(str(key_file)) == ["sk-alpha", "sk-beta"]


def test_load_api_keys_masked(tmp_path):
    key_file = tmp_path / "keys.json"
    key_file.write_text(json.dumps(["abcdefghi", "123"]), encoding="utf-8")

    assert load_api_keys_masked(str(key_file)) == [
        {"index": 0, "label": "key1", "masked": "abc***ghi"},
        {"index": 1, "label": "key2", "masked": "***"},
    ]


def test_get_api_key_from_payload_prefers_explicit_key(tmp_path):
    key_file = tmp_path / "keys.json"
    key_file.write_text(json.dumps(["stored-key"]), encoding="utf-8")

    payload = {"api_key": " explicit-key ", "key_index": 0}

    assert get_api_key_from_payload(payload, str(key_file)) == "explicit-key"


def test_get_api_key_from_payload_reads_index(tmp_path):
    key_file = tmp_path / "keys.json"
    key_file.write_text(json.dumps(["first", "second"]), encoding="utf-8")

    assert get_api_key_from_payload({"key_index": 1}, str(key_file)) == "second"


def test_build_chat_payload_with_system_message():
    payload = build_chat_payload("model-a", "hello", "system text", stream=True)

    assert payload["model"] == "model-a"
    assert payload["stream"] is True
    assert payload["messages"] == [
        {"role": "system", "content": "system text"},
        {"role": "user", "content": "hello"},
    ]


def test_extract_message_strips_leading_newline():
    result = {"choices": [{"message": {"content": "\n\nhello"}}]}

    assert extract_message(result) == "hello"


def test_ai_client_error_is_exception():
    with pytest.raises(AiClientError):
        raise AiClientError(503, "busy")
