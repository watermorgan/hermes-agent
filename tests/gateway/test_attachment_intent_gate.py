import pytest

from gateway.config import GatewayConfig, Platform
from gateway.platforms.base import MessageEvent, MessageType
from gateway.run import GatewayRunner
from gateway.session import SessionSource, build_session_key


def _make_runner() -> GatewayRunner:
    runner = GatewayRunner.__new__(GatewayRunner)
    runner.config = GatewayConfig(group_sessions_per_user=True)
    runner.adapters = {}
    runner._model = "MiniMax-M3"
    runner._base_url = None
    runner._decide_image_input_mode = lambda: "native"
    return runner


def _source(platform: Platform) -> SessionSource:
    return SessionSource(
        platform=platform,
        chat_id=f"{platform.value}-chat",
        chat_type="private",
        user_name="buyer",
    )


def _image_event(source: SessionSource, text: str = "") -> MessageEvent:
    return MessageEvent(
        text=text,
        message_type=MessageType.PHOTO,
        source=source,
        media_urls=["/tmp/order-photo.jpg"],
        media_types=["image/jpeg"],
    )


@pytest.mark.asyncio
async def test_feishu_image_only_asks_for_intent_without_attaching_image():
    runner = _make_runner()
    source = _source(Platform.FEISHU)

    result = await runner._prepare_inbound_message_text(
        event=_image_event(source),
        source=source,
        history=[],
    )

    assert "user sent attachment" in result
    lowered = result.lower()
    assert "ask one concise clarification question" in lowered
    assert "do not analyze" in lowered
    assert runner._consume_pending_native_image_paths(build_session_key(source)) == []


@pytest.mark.asyncio
async def test_feishu_image_to_excel_keeps_image_available_to_agent():
    runner = _make_runner()
    source = _source(Platform.FEISHU)

    result = await runner._prepare_inbound_message_text(
        event=_image_event(source, "将这两张图片整理成 Excel 输出，检查没问题再给我"),
        source=source,
        history=[],
    )

    assert "整理成 Excel" in result
    assert "ask one concise clarification question" not in result
    assert runner._consume_pending_native_image_paths(build_session_key(source)) == [
        "/tmp/order-photo.jpg"
    ]


@pytest.mark.asyncio
async def test_dingtalk_image_only_asks_for_intent_without_attaching_image():
    runner = _make_runner()
    source = _source(Platform.DINGTALK)

    result = await runner._prepare_inbound_message_text(
        event=_image_event(source),
        source=source,
        history=[],
    )

    assert "user sent attachment" in result
    assert "ask one concise clarification question" in result.lower()
    assert runner._consume_pending_native_image_paths(build_session_key(source)) == []


@pytest.mark.asyncio
async def test_feishu_reuploaded_image_uses_recent_excel_intent():
    runner = _make_runner()
    source = _source(Platform.FEISHU)
    history = [
        {
            "role": "user",
            "content": "将以下两张图片，整理成excel输出，检查没问题再给我",
        },
        {"role": "assistant", "content": "可以，你重新发图片。"},
    ]

    result = await runner._prepare_inbound_message_text(
        event=_image_event(source, "我重新发你图片"),
        source=source,
        history=history,
    )

    assert "我重新发你图片" in result
    assert "ask one concise clarification question" not in result
    assert runner._consume_pending_native_image_paths(build_session_key(source)) == [
        "/tmp/order-photo.jpg"
    ]
