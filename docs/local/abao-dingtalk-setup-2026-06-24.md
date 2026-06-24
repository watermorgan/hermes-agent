# Abao DingTalk Setup - 2026-06-24

## Scope

- Profile: `abao`
- Platform: DingTalk
- Goal: create and connect a dedicated DingTalk robot for Abao without reusing Ting, FAQ Bot, or Adae credentials.
- Secret policy: credentials are stored only in the local Hermes profile env file and are not recorded here.

## Backup

Before changing the profile, `~/.hermes/profiles/abao` was backed up to:

```text
/Users/weitao/.hermes/backups/abao-pre-dingtalk-setup-20260624_201426.tgz
```

## Changes Applied

- Ran the Hermes DingTalk gateway setup QR flow for `abao`.
- Authorized the DingTalk developer registration flow with the user's DingTalk admin account.
- Created/confirmed the DingTalk app/robot:
  - app name: `阿宝`
  - robot name: `阿宝`
  - robot config: enabled
  - message receive mode: `Stream模式`
  - app state: `已上线`
  - visibility shown in DingTalk console: `部分成员可见`
- Stored DingTalk credentials in:

```text
/Users/weitao/.hermes/profiles/abao/.env
```

- Removed `API_SERVER_KEY` from the `abao` profile env to stop the duplicate API server on port `8642`.
- Added profile-local `GATEWAY_ALLOW_ALL_USERS=true` so the DingTalk robot can respond instead of denying all inbound users.
- Installed and loaded the profile-specific launchd service:

```text
/Users/weitao/Library/LaunchAgents/ai.hermes.gateway-abao.plist
```

The launchd service runs:

```text
/Users/weitao/soda-base/hermes-agent/venv/bin/python -m hermes_cli.main --profile abao gateway run --replace
```

## Verification

Commands run from `/Users/weitao/soda-base/hermes-agent`:

```bash
venv/bin/python -m hermes_cli.main --profile abao gateway status
venv/bin/python -m hermes_cli.main gateway list
venv/bin/python -m hermes_cli.main --profile abao gateway status --deep
venv/bin/python -m hermes_cli.main --profile abao prompt-size --platform dingtalk --json
TIMEFORMAT='elapsed=%R'; time venv/bin/python -m hermes_cli.main --profile abao -z '用一句话说明你是谁，以及你主要负责什么。不要调用工具。'
```

Observed results:

- `abao` launchd service loaded and running.
- `abao` gateway PID present alongside `default`, `adae`, `faqbot`, and `ting`.
- DingTalk adapter connected via Stream Mode.
- After removing `API_SERVER_KEY`, the restarted gateway no longer connects or retries `api_server`, so the port `8642` warning is gone for the current run.
- Prompt size for DingTalk:
  - system prompt: `34,748` chars / `38,162` bytes
  - skills index: `9,246` chars / `9,336` bytes
  - memory: `475` chars / `1,077` bytes
  - user profile: `254` chars / `592` bytes
  - tools: `11` tools / `20,540` JSON bytes
- Local one-shot model smoke test completed in about `10.0s` and identified itself as Abao's coordinator role.

## Remaining Risks

- A real DingTalk inbound chat was requested but not observed in the gateway log during this setup window. The first real user message should still be tested from DingTalk.
- `GATEWAY_ALLOW_ALL_USERS=true` is profile-local but intentionally permissive. Risk is partly limited by DingTalk's current `部分成员可见` visibility, but production hardening should replace this with a narrower access policy if Hermes gains DingTalk-specific allowlist support or once user IDs are known.
- The DingTalk console banner says current changes take effect after version publication. The app already shows `已上线`, and the robot config is enabled; if a future console edit does not appear in chat, publish a new version from `版本管理与发布`.
