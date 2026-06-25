from pathlib import Path
import os

import pytest
import yaml


PROFILE_DIR = Path(
    os.environ.get("HERMES_ABAO_PROFILE_DIR", Path.home() / ".hermes/profiles/abao")
).expanduser()


def _read_profile_file(relative_path: str) -> str:
    if not PROFILE_DIR.exists():
        pytest.skip(f"Abao profile not found: {PROFILE_DIR}")
    path = PROFILE_DIR / relative_path
    assert path.exists(), f"Missing Abao profile file: {path}"
    return path.read_text(encoding="utf-8")


def _assert_contains_all(text: str, phrases: list[str]) -> None:
    missing = [phrase for phrase in phrases if phrase not in text]
    assert not missing, "Missing profile contract phrases: " + ", ".join(missing)


def test_abao_soul_separates_assistant_thinking_and_dispatch_modes() -> None:
    soul = _read_profile_file("SOUL.md")

    _assert_contains_all(
        soul,
        [
            "全能助手模式",
            "思维沟通者模式",
            "军团调度模式",
            "先识别意图，再决定是否调用专家",
            "聊聊/帮我想想/你怎么看",
            "默认不派专家",
        ],
    )


def test_abao_router_defines_structured_intent_gate() -> None:
    router = _read_profile_file("skills/agent-legion-router/SKILL.md")

    _assert_contains_all(
        router,
        [
            "intent:",
            "domain:",
            "confidence:",
            "needs_expert:",
            "expert:",
            "need_clarification:",
            "next_action:",
            "confidence >= 0.75",
            "0.45 <= confidence < 0.75",
            "confidence < 0.45",
            "外部副作用",
            "不要说“我转给”",
            "不要直接说“转给 Ting”",
            "适合交给",
            "可复制的转交摘要",
        ],
    )


def test_abao_maoxuan_decision_lens_is_present_and_bounded() -> None:
    lens = _read_profile_file("skills/maoxuan-decision-lens/SKILL.md")

    _assert_contains_all(
        lens,
        [
            "主要矛盾",
            "实事求是",
            "调查研究",
            "矛盾分析",
            "实践论",
            "持久战",
            "群众路线",
            "组织建设",
            "普通聊天不触发",
            "不要把方法论当口号输出",
        ],
    )


def test_abao_memory_records_upgrade_boundaries() -> None:
    memory = _read_profile_file("memories/MEMORY.md")

    _assert_contains_all(
        memory,
        [
            "先识别意图再路由",
            "思维沟通者",
            "毛选/长征方法体系",
            "普通聊天不强行套框架",
            "没有可靠回执时不要声称已经完成转交",
        ],
    )


def test_abao_dingtalk_toolset_avoids_direct_file_mutation() -> None:
    config = yaml.safe_load(_read_profile_file("config.yaml"))
    dingtalk_toolsets = config["platform_toolsets"]["dingtalk"]

    assert "file" not in dingtalk_toolsets
    _assert_contains_all(
        "\n".join(dingtalk_toolsets),
        ["skills", "memory", "session_search", "todo", "messaging"],
    )
