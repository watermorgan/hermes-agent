# Ting Personalization Snapshot - 2026-06-16

This snapshot preserves the local Hermes Ting personalization work that lives
partly in `~/.hermes/profiles/ting`. It intentionally omits secrets, webhook
URLs, tokens, account identifiers, and raw customer content.

## Purpose

Hermes Ting is being tuned as a personal foreign-trade assistant that can:

- answer normal questions quickly;
- ask one short clarification before processing bare DingTalk/Feishu uploads;
- handle explicit file/image tasks without saying it cannot help;
- route PDF translation and real Excel translation to export-agent MCP tools;
- treat image/screenshot-to-table tasks as vision/OCR extraction, not Excel
  translation;
- keep runtime tool noise low on DingTalk and Feishu.

## Tracked Code Changes

These changes are in this repository branch:

- `gateway/run.py`
  - Adds a DingTalk/Feishu/Lark attachment intent gate.
  - Bare uploads without user intent are converted into an agent-visible note
    asking one concise clarification question.
  - Explicit captions such as image-to-Excel, translation, summary, review,
    extraction, or conversion bypass the gate.
  - Recent user history can carry intent for reuploaded files, so "I resent the
    images" after an earlier image-to-Excel request proceeds normally.
  - Audio/voice messages are not gated by this attachment logic.
- `hermes_cli/prompt_size.py`
  - Makes prompt-size diagnostics use the same platform toolset config as real
    sessions.
  - Discovers MCP tools before sizing so export-agent schema size is visible.
  - Reports tool names in JSON output for regression checks.
- `tests/gateway/test_attachment_intent_gate.py`
  - Covers Feishu/DingTalk image-only clarification behavior.
  - Covers explicit image-to-Excel behavior.
  - Covers recent-history intent reuse on reupload.
- `tests/hermes_cli/test_prompt_size.py`
  - Covers platform toolset sizing.
  - Covers MCP discovery during prompt-size diagnostics.

## Runtime Profile Changes

These files are outside the git repository and were edited locally:

- `~/.hermes/profiles/ting/SOUL.md`
  - Strengthened file/image routing rules.
  - Bare files/images/screenshots ask one concise clarification before work.
  - Explicit task requests proceed without repeated clarification.
  - Image/screenshot/scan to Excel/table uses vision/OCR and CSV/table output.
  - PDF translation uses the PDF export-agent service.
  - Real `.xlsx`/`.xls` translation uses the Excel export-agent service.
  - Missing files get a short path/upload request, not a long checklist or
    blocking clarification loop.
  - File paths may only be reported after a successful `write_file`, copying
    the returned `resolved_path` exactly.
- `~/.hermes/profiles/ting/skills/file-task-router/SKILL.md`
  - Adds Ting file-task routing for attachments, PDF, Excel, image-to-table,
    quote/order/contract review, and normal text questions.
  - Prevents dead-end "I cannot process images" responses when a useful route
    exists.
- `~/.hermes/profiles/ting/memories/MEMORY.md`
  - Compresses stable routing memories and removes stale duplicated detail.
  - Keeps the durable rules about Excel translation, image table extraction,
    exact `resolved_path` reporting, DingTalk file delivery, and speed.
- `~/.hermes/profiles/ting/config.yaml`
  - Narrows DingTalk/Feishu runtime toolsets to reduce latency and accidental
    tool loops.
  - Leaves export-agent MCP tools enabled for professional PDF/Excel routes.

## Local Backups

Backups were created before modifying `~/.hermes` profile files:

- `~/.hermes/profiles/ting/SOUL.md.bak.20260616_104108`
- `~/.hermes/profiles/ting/backups/skills-file-router.20260616_104108.tgz`
- `~/.hermes/profiles/ting/SOUL.md.bak.20260616_111743`
- `~/.hermes/profiles/ting/config.yaml.bak.20260616_112429`
- `~/.hermes/profiles/ting/memories/MEMORY.md.bak.20260616_112835`
- `~/.hermes/profiles/ting/memories/MEMORY.md.bak.20260616_114532`

## Current Toolset Shape

Current DingTalk/Feishu profile intent:

- Enabled core toolsets: `web`, `file`, `vision`, `skills`, `memory`,
  `session_search`.
- Disabled noisy or risky general toolsets: browser, terminal, code execution,
  image generation, text-to-speech, clarification tool, delegation, cron,
  messaging, todo, and computer use.
- MCP export-agent PDF/Excel tools stay enabled.

## Prompt Size Baseline

After the prompt-size diagnostic fix and Ting profile compression:

- DingTalk: 23 tools, 25,496 bytes of tool schema.
- Feishu: 28 tools, 28,675 bytes of tool schema.
- Ting memory block: 1,109 chars / 2,012 bytes.
- DingTalk system prompt: 41,016 chars / 48,347 bytes.
- Feishu system prompt: 41,389 chars / 48,722 bytes.

The old diagnostic path over-counted the runtime tool surface because it did
not honor platform toolsets and missed the real MCP discovery step.

## Verification Snapshot

Completed checks during this tuning pass:

- `pytest -o addopts="-m 'not integration'"` targeted gateway, image routing,
  session, audio routing, and prompt-size tests: 99 passed.
- `ruff check` on changed Python files: passed.
- `py_compile` on changed runtime modules: passed.
- Ting image-to-table CLI smoke produced a consistent CSV at
  `/private/tmp/ting-packing-list-smoke.csv`.
- DingTalk gateway process restarted and connected after the profile changes.

## Known Residual Risks

- Image/OCR table extraction is correct but still slow in CLI smoke tests,
  around one minute for the sample packing-list image.
- True `.xlsx` generation for image-to-table is not yet a dedicated service
  route; CSV/table output is the current reliable fallback.
- Real external DingTalk/Feishu customer-message latency still needs a fresh
  post-commit live sample because local CLI timing includes model and tool
  startup overhead.
- Keep export-agent product code untouched unless the route contract changes
  are explicitly requested.
