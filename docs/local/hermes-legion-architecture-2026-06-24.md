# Hermes Agent Legion Architecture - 2026-06-24

This document captures the first Hermes-native migration of the old OpenClaw
agent organization. It intentionally omits API keys, channel tokens, webhook
URLs, account IDs, and customer content.

## Decision

Hermes Agent is the primary project going forward. OpenClaw is no longer the
main iteration target; it remains a read-only migration source unless a future
task explicitly reopens OpenClaw work.

The agent topology is:

- `abao`: personal coordinator, routing hub, daily assistant, status summary.
- `ting`: foreign-trade specialist, direct DingTalk-facing expert.
- `adae`: engineering, architecture, deployment, and diagnostics specialist.
- `faqbot`: AIGC platform product, presales, deployment FAQ, and security
  governance specialist.

## Core Architecture

Agents can be reached directly. `abao` is not a mandatory gateway.

This matters for Ting: users can still message Ting directly in DingTalk. Ting
should handle foreign-trade tasks independently. `abao` only helps when a task
is ambiguous, cross-domain, or needs routing/status coordination.

## Routing Contract

| Domain | Primary agent | Notes |
| --- | --- | --- |
| Foreign trade, PDF/Excel translation, BOM, quotes, customer email | `ting` | Direct expert entry is expected. |
| Code, architecture, deployment, CI/CD, logs, production diagnostics | `adae` | Technical work should produce evidence and git records. |
| AIGC platform product, presales, deployment FAQ, security governance | `faqbot` | Product-facing answers should avoid unverified claims. |
| Daily tasks, reminders, status tracking, cross-agent coordination | `abao` | Coordinator, not bottleneck. |

## Local Runtime Changes

Created Hermes profiles:

- `~/.hermes/profiles/abao`
- `~/.hermes/profiles/faqbot`

Updated Hermes profile content:

- `~/.hermes/profiles/abao/SOUL.md`
- `~/.hermes/profiles/abao/memories/MEMORY.md`
- `~/.hermes/profiles/abao/skills/agent-legion-router/SKILL.md`
- `~/.hermes/profiles/abao/config.yaml` platform toolsets only
- `~/.hermes/profiles/faqbot/SOUL.md`
- `~/.hermes/profiles/faqbot/memories/MEMORY.md`
- `~/.hermes/profiles/faqbot/skills/aigc-product-router/SKILL.md`
- `~/.hermes/profiles/faqbot/config.yaml` platform toolsets only
- `~/.hermes/profiles/adae/SOUL.md`

No OpenClaw product code was changed for this migration.

## Migration Sources

Read-only OpenClaw sources used:

- `~/.openclaw/shared/agents-overview.md`
- `~/.openclaw/workspace/SOUL.md`
- `~/.openclaw/workspace/TOOLS.md`
- `~/.openclaw/workspace-adae/SOUL.md`
- `~/.openclaw/workspace-faq-bot/SOUL.md`
- `~/.openclaw/workspace-faq-bot/MEMORY.md`

## Backup

Before editing `~/.hermes`, a local archive was created:

- `~/.hermes/backups/hermes-legion-pre-migration-20260624_152215.tgz`

## Toolset Policy

`abao` gets coordination tools, but not broad browser/code/terminal execution by
default. CLI can use `kanban`; message-platform surfaces stay lower-noise.

`faqbot` gets only knowledge/file/search/memory tools by default. It should not
perform technical execution; implementation and deployment issues route to
`adae`.

`adae` behavior was strengthened, but its dangerous tool surface was not widened
in this pass. Technical execution should continue through CLI/Codex where
verification and git hygiene are visible.

## Validation Target

Minimum validation for this pass:

- `hermes profile list` shows `abao`, `ting`, `adae`, `faqbot`.
- `prompt-size` works for `abao`, `faqbot`, `adae`, and `ting`.
- Existing Ting attachment gate and prompt-size tests still pass.
- Existing running Ting/adae/default gateways are not restarted or disrupted.

## Known Gaps

- `abao` and `faqbot` are created as profiles but gateway channels are not
  started in this pass.
- Existing `default` and `adae` launchd service definitions are stale relative
  to the current install; this was observed but not restarted during migration.
- OpenClaw A2A event ledger is not migrated. Hermes Kanban/profile descriptions
  are the preferred future coordination mechanism.
- Profile configs were cloned locally and may contain local provider details;
  repository docs only store redacted profile intent and toolset shape.
