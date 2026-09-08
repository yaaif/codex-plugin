# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| `1.3.x` | Yes |
| `1.1.x` | No |
| `0.1.x` | No |

## Threat model (summary)

This Codex plugin ships:

- Markdown skills and docs
- A `.mcp.json` declaration that launches a local **stdio** MCP bridge via `npx @yaaif/platform-mcp@<version> --client codex`, authenticating to a customer-configured YAA\F environment
- Shared Node installer: `npx @yaaif/platform-mcp --install --client codex` (optional `--offline`)

It does **not** ship opaque binaries, remote install scripts, or embedded credentials. The MCP bridge itself is a shared package (source in
[`cursor-plugin/packages/mcp`](https://github.com/yaaif/cursor-plugin/tree/main/packages/mcp)) used identically by the Cursor, Codex, and Claude Code plugins.

### Auth

- Uses Keycloak OIDC authorization code + PKCE (S256) with a loopback redirect (`http://127.0.0.1:<ephemeral>/callback`)
- Optional device-code login for headless/CI (`yaaif_login_device`) when enabled on the Keycloak client
- Tokens are stored at `~/.yaaif/codex/session.json` with mode `0600`
- Session also records `profile_id` + `oidc_authority` (issuer mismatch forces re-login)
- API calls send `Authorization: Bearer` + `X-Tenant-ID` only
- Does **not** use platform S2S secrets, desktop connection keys, or AI-gateway keys
- Tenant **API keys** (`yaaif_api_key_*`) are the supported credential for MCP → platform APIs
- State is fully isolated from Cursor (`~/.yaaif/cursor`) and Claude (`~/.yaaif/claude`)

### MCP surface

Tools can create/update skills, MCP deployments, and ambient workflows on the configured tenant. Treat enablement like granting Admin UI access for the signed-in user.

## Reporting a vulnerability

Email **security@yaaif.com** (or your BeezLabs security contact) with reproduction steps. Do not open public issues for undisclosed vulnerabilities.

## Marketplace review notes

- Runtime is Node executing `npx @yaaif/platform-mcp@<version> --client codex` from the public npm registry
- No secrets are required in this plugin repo; `YAAIF_*` environment variables hold environment URLs only
