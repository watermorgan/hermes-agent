# Abao Intent And Thinking Upgrade - 2026-06-25

## Goal

Upgrade Abao from a simple coordinator into a three-mode assistant:

- all-purpose personal assistant
- thinking partner for decisions and strategy
- intent-gated router for the Hermes agent legion

The upgrade is profile/skill level only. It does not change Hermes product code or export-agent code.

## Profile Scope

Updated local profile files:

- `/Users/weitao/.hermes/profiles/abao/SOUL.md`
- `/Users/weitao/.hermes/profiles/abao/memories/MEMORY.md`
- `/Users/weitao/.hermes/profiles/abao/skills/agent-legion-router/SKILL.md`
- `/Users/weitao/.hermes/profiles/abao/skills/maoxuan-decision-lens/SKILL.md`
- `/Users/weitao/.hermes/profiles/abao/config.yaml`

Backup before edits:

- `/Users/weitao/.hermes/backups/abao-profile-upgrade-20260625-152533.tar.gz`

## Behavior Contract

Abao now classifies each user request before deciding whether to call an expert:

```text
intent: 普通助手 / 思维陪练 / 专家任务 / 跨智能体协调
domain: 外贸 / 技术 / FAQ / 个人事务 / 决策 / 混合
confidence: 0-1
needs_expert: true/false
expert: Ting / A-Dai / FAQ / none
need_clarification: true/false
next_action: 自答 / 追问 / 交接 / 拆解
```

Routing thresholds:

- `confidence >= 0.75`: route when the domain is clear.
- `0.45 <= confidence < 0.75`: ask one clarifying question.
- `confidence < 0.45`: Abao handles as assistant or thinking partner first.
- External side effects require confirmation.

## Expert Routing

- Ting: foreign trade, customer communication, quotation, trade docs, BOM, translation, PDF/Excel/image table extraction.
- A-Dai: code, architecture, deployment, logs, CI/CD, technical incidents.
- FAQ Bot: AIGC platform product FAQ, presales, deployment consulting, security governance.
- Abao: personal work, thinking partner, status coordination, task decomposition.

## Maoxuan Decision Lens

Abao has a bounded decision lens inspired by the Maoxuan-Changzheng method system:

- 主要矛盾
- 实事求是
- 调查研究
- 矛盾分析
- 实践论
- 持久战
- 群众路线
- 组织建设

This is not a slogan layer. It should be used implicitly for high-value decisions, strategy, review, and long-term planning. Casual chat should not force this framework.

## Verification

Local contract test:

```bash
./.venv/bin/pytest -o addopts='' tests/local/test_abao_profile_contract.py -q
```

The test intentionally reads the local Abao profile under `~/.hermes/profiles/abao`; if that profile does not exist, it skips.

## Runtime Tuning

Abao DingTalk no longer enables the `file` toolset. This removes direct `read_file`, `write_file`, `search_files`, and `patch` schemas from DingTalk sessions. The intent is to keep DingTalk safer and lighter: file uploads should first clarify user intent, then route to the appropriate expert or workflow instead of letting Abao mutate files directly.

Prompt-size check:

```bash
abao prompt-size --platform dingtalk --json
```

Latest checked result after tuning:

- DingTalk tools: 7
- DingTalk tool schema bytes: 14,754
- DingTalk system prompt chars: 35,810
