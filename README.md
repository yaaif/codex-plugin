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
npx -y @yaaif/platform-mcp@1.2.0 --client codex
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

## Development and release

Before installing a release candidate, use Codex’s `plugin-creator` validator
against `plugins/yaaif-platform` and verify that `.agents/plugins/marketplace.json`
still names the `yaaif` marketplace with the `AVAILABLE` / `ON_INSTALL` policy.

Release order is: publish `@yaaif/platform-mcp`, publish the compatibility
`@yaaif/cursor-mcp` wrapper, install and smoke-test this local marketplace,
then submit the tested repository to the OpenAI plugin directory.
