# FAQ Bot Channel Migration - 2026-06-24

This records the Hermes `faqbot` channel migration from the old OpenClaw
configuration. It intentionally omits all credential values, webhook URLs,
tokens, account IDs, and customer content.

## Source

Read-only source:

- `~/.openclaw/openclaw.json`

OpenClaw accounts used:

- `channels.feishu.accounts["faq-bot"]`
- `channels.dingtalk.accounts["faq-bot"]`

OpenClaw bindings confirmed:

- `faq-bot -> feishu / faq-bot`
- `faq-bot -> dingtalk / faq-bot`

## Destination

Hermes profile:

- `~/.hermes/profiles/faqbot`

Credential keys migrated to `~/.hermes/profiles/faqbot/.env`:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_DOMAIN=feishu`
- `FEISHU_CONNECTION_MODE=websocket`
- `FEISHU_GROUP_POLICY=allowlist`
- `DINGTALK_CLIENT_ID`
- `DINGTALK_CLIENT_SECRET`
- `DINGTALK_REQUIRE_MENTION=true`
- `GATEWAY_ALLOW_ALL_USERS=true`

The inherited `API_SERVER_KEY` was removed from `faqbot/.env` to avoid starting
an unnecessary `api_server` on the already-used local port.

Non-secret platform settings added to `faqbot/config.yaml`:

```yaml
platforms:
  feishu:
    enabled: true
    extra:
      domain: feishu
      connection_mode: websocket
      require_mention: true
  dingtalk:
    enabled: true
    extra:
      require_mention: true
```

## Backup

Backup before migration:

- `~/.hermes/backups/faqbot-pre-channel-migration-20260624_170233.tgz`

## Validation

Completed checks:

- `hermes profile list` showed `faqbot`.
- `hermes --profile faqbot gateway start` generated and started the launchd
  service.
- `hermes --profile faqbot gateway status` showed service loaded and running.
- Gateway logs showed:
  - `✓ feishu connected`
  - `✓ dingtalk connected`
  - `Gateway running with 2 platform(s)`
- After removing `API_SERVER_KEY`, the restarted gateway no longer tried to
  start `api_server`.
- `prompt-size --profile faqbot --platform feishu --json` succeeded:
  - 9 tools
  - 17,692 bytes of tool schema
  - 36,984 bytes system prompt
- `prompt-size --profile faqbot --platform dingtalk --json` succeeded:
  - 9 tools
  - 17,692 bytes of tool schema
  - 36,609 bytes system prompt
- Local model smoke:
  - prompt: "用一句话说明你是谁，以及你主要负责什么。不要调用工具。"
  - response identified itself as FAQ Bot and described AIGC platform product,
    presales, deployment, security governance, and integration support.

## Remaining Risks

- Live inbound Feishu/DingTalk user-message samples were not sent during this
  migration. Connection-level validation is complete; user-visible chat
  validation still needs a real message.
- `GATEWAY_ALLOW_ALL_USERS=true` restores usability without per-user allowlists.
  Tighten this later with Feishu/DingTalk user IDs if the bot enters shared
  groups or sensitive environments.
- Feishu group policy remains `allowlist`; without explicit allowed user IDs,
  group behavior may be stricter than direct-message behavior.
