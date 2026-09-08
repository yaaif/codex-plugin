# YAAIF for Codex

The YAAIF Codex plugin provides a local stdio MCP bridge and Codex-native
skills for authenticated YAAIF planning, skill creation, MCP deployment,
scenario lifecycle, ambient workflows, diagnostics, platform tools, and
read-only operations support.

**Version:** 1.3.0  
**Logo:** [`plugins/yaaif-platform/assets/logo.svg`](plugins/yaaif-platform/assets/logo.svg)

This plugin is on the same **1.3.0** contract as Cursor and Claude Code (nine
core skills, ten short names, Agent Spec preview/apply). Codex has no
`userConfig` and no `commands/` directory — short names are alias skills.

## Install

Optional profile + login, then add this repository as a local marketplace in
Codex and install the **YAAIF** plugin (`yaaif-platform`). The marketplace
entry is deliberately `AVAILABLE` with `ON_INSTALL` authentication.

```bash
npx -y @yaaif/platform-mcp@1.3.1 --install --client codex
```

The plugin starts:

```text
npx -y @yaaif/platform-mcp@1.3.1 --client codex
```

The process inherits `YAAIF_*` from Codex. Node.js 20 or later is required.
Run `yaaif-login` (or `yaaif_ensure_session`) in a new task for browser PKCE
login, or `yaaif_login_device` where a browser callback is not available.

> **Note:** `@yaaif/platform-mcp` must be on the public npm registry before a
> marketplace install can start the bridge. See
> [docs/npm-publish.md](docs/npm-publish.md). Until then, use a local
> [monorepo override](#local-mcp-override).

## Profiles and state

Codex uses `~/.yaaif/codex` exclusively. It never reads or overwrites Cursor
state in `~/.yaaif/cursor` or Claude state in `~/.yaaif/claude`.

| Profile | Intended use |
| --- | --- |
| `hosted` | Hosted YAAIF endpoints |
| `local` | OIDC and APIs on the local stack |
| `local-hybrid` | Hosted/tunnel OIDC with local APIs |

Override endpoints, tenant, CA, and mTLS with `YAAIF_*` environment variables
or `~/.yaaif/codex/profiles.json`.

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

## Skills and aliases

Ask Codex to use the skill by name (`$yaaif-login`, “use yaaif-plan”, …).

| Skill | Short alias | Purpose |
| --- | --- | --- |
| `yaaif-auth` | `yaaif-login` | Platform profile + login + tenant |
| `yaaif-doctor` | `yaaif-doctor` | Connectivity / TLS / auth diagnostics |
| `yaaif-plan-usecase` | `yaaif-plan` | Use-case plan → approve → create Scenario + objects |
| `yaaif-scenario` | `yaaif-scenario` | Create or maintain a Scenario; Admin UI **Open in Codex** |
| — | `yaaif-sync-scenario` | Apply spec → objects, or explicitly adopt live drift |
| `yaaif-create-skill` | `yaaif-new-skill` | Author + load skill |
| `yaaif-create-mcp` | `yaaif-new-mcp` | Scaffold + deploy MCP + API key bind |
| `yaaif-create-ambient` | `yaaif-new-workflow` | Ambient workflows |
| `yaaif-platform-tools` | `yaaif-platform-tools` | Discover/call agent-service built-in local tools |
| `yaaif-ops-support` | `yaaif-ops` | Read-only incident triage |

## Local MCP override

Until `@yaaif/platform-mcp` is published, or when developing the bridge, point
Codex at the monorepo build (do not commit this path):

```json
{
  "mcpServers": {
    "yaaif": {
      "command": "node",
      "args": [
        "/path/to/yaaif-platform/integrations/cursor-plugin/packages/mcp/dist/cli.js",
        "--client",
        "codex"
      ]
    }
  }
}
```

Build first: `cd integrations/cursor-plugin/packages/mcp && npm install && npm run build`.

## Development and release

```bash
python3 scripts/check-plugin.py --require-skill-sync
```

Release order: publish `@yaaif/platform-mcp@<version>` from `cursor-plugin` →
confirm with `npm view` → keep the pin in
[`plugins/yaaif-platform/.mcp.json`](plugins/yaaif-platform/.mcp.json) →
smoke-test this local marketplace → submit to the OpenAI plugin directory.

See [CHANGELOG.md](CHANGELOG.md) and [docs/npm-publish.md](docs/npm-publish.md).
