# YAAIF for Codex

The YAAIF Codex plugin provides a local stdio MCP bridge and Codex-native
skills for authenticated YAAIF planning, skill creation, MCP deployment,
scenario lifecycle, ambient workflows, diagnostics, platform tools, and
read-only operations support.

## Install

Install this repository as a local marketplace in Codex, then install the
**YAAIF** plugin (`yaaif-platform`). The marketplace entry is deliberately
`AVAILABLE` with `ON_INSTALL` authentication.

The plugin starts:

```text
npx -y @yaaif/platform-mcp@1.3.0 --client codex
```

The process inherits `YAAIF_*` configuration from Codex. Node.js 20 or later is
required. Run `yaaif_ensure_session` in a new task to use browser PKCE login,
or `yaaif_login_device` where browser callback login is not available.

## Profiles and state

Codex uses `~/.yaaif/codex` exclusively. It never reads or overwrites Cursor
state in `~/.yaaif/cursor`.

| Profile | Intended use |
| --- | --- |
| `hosted` | Hosted YAAIF endpoints |
| `local` | OIDC and APIs on the local stack |
| `local-hybrid` | Hosted/tunnel OIDC with local APIs |

Override endpoints, tenant, CA, and mTLS with the existing `YAAIF_*`
environment variables. In particular, use `YAAIF_EXTRA_CA_FILE` for a local CA
and `YAAIF_CLIENT_CERT_FILE` / `YAAIF_CLIENT_KEY_FILE` for mTLS.

## Admin UI handoffs

YAAIF Admin UI exposes **Open in IDE** on scenarios, skills, agents, and
workflows. Choose **Open in Codex** to start a new Codex thread with a prefilled
prompt via `codex://threads/new?prompt=…`.

| Admin surface | Codex skill | Typical prompt fields |
| --- | --- | --- |
| Scenarios | `yaaif-scenario` | `spec_id`, `slug`, readiness blockers |
| Skills | `yaaif-create-skill` | `skill_id`, `goal` |
| Ambient workflows | `yaaif-create-ambient` | `workflow_id`, `agent_id` |
| Agents | MCP agent tools | `agent_id`, `agent_type` |

Install this plugin before using Admin UI handoffs. Authenticate with
`yaaif-auth`, then follow the skill named in the prompt. Codex state stays in
`~/.yaaif/codex` and never shares Cursor profiles.

## Skills

| Skill | Purpose |
| --- | --- |
| `yaaif-auth` | Platform profile + login + tenant |
| `yaaif-doctor` | Connectivity / TLS / auth diagnostics |
| `yaaif-plan-usecase` | Use-case plan → approve → create Scenario + agents/skills/workflows |
| `yaaif-scenario` | Create or maintain a Scenario (Agent Spec); Admin UI **Open in Codex** |
| `yaaif-create-skill` | Author + load skill (prefers platform local lifecycle tools) |
| `yaaif-platform-tools` | Discover/call agent-service built-in local tools |
| `yaaif-ops-support` | Read-only incident triage (session/ambient/desktop) |
| `yaaif-create-mcp` | Scaffold + deploy MCP (compose or k8s GitOps) + API key bind |
| `yaaif-create-ambient` | Ambient workflows; Admin UI **Open in Codex** for `workflow_id` |

## Development and release

Before installing a release candidate, use Codex’s `plugin-creator` validator
against `plugins/yaaif-platform` and verify that `.agents/plugins/marketplace.json`
still names the `yaaif` marketplace with the `AVAILABLE` / `ON_INSTALL` policy.

Release order is: publish `@yaaif/platform-mcp`, publish the compatibility
`@yaaif/cursor-mcp` wrapper, install and smoke-test this local marketplace,
then submit the tested repository to the OpenAI plugin directory.
