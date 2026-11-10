# Changelog

## 1.7.0

- Align with platform 1.7.0 and support matching-source npx installation with optional archive verification.
- Add isolated multi-server sessions, endpoint-only profile cloning, and safe cross-server Scenario draft copy.
- Remove older version caches after verified updates and move them to per-client backups.
- Restore previous managed sources and launcher configuration after failed updates.
- Add side-effect-free dry-run install and update plans.
- Add portable profile bundles with secret-safe validation and conflict-protected imports.
- Add safe complete skill-pack copying with ID remapping and secret-file exclusion.
- Add sanitized ambient workflow copying with disabled-for-review installation.
- Add secret-free MCP server connection copying with non-secret header mappings and explicit credential rebinding.
- Add agent-definition migration with disabled-for-review creation and explicit skill remapping.
- Add unified dry-run-first catalog migration with dependency ordering and conflict aborts.
- Add secret-free MCP server connection copying with non-secret header mappings and explicit credential rebinding.
- Add sanitized ambient workflow copying with disabled-for-review installation.

## 1.4.0

- Synchronize all Cursor canonical skills, including product docs, file workflows, Wiki inspection, and platform-update inspection.
- Add credential-profile guidance, Scenario sync preview/apply guidance, and `yaaif_features` backend capability checks; align with bridge 1.4.0.

## 1.3.2

- Align plugin version with platform 1.3.2.

## 1.3.0

- Align plugin version with `@yaaif/platform-mcp` 1.3.0 and the Cursor / Claude plugins.
- Shared Node installer: `npx @yaaif/platform-mcp@1.3.0 --install --client codex` (optional `--plugin-src` / `--offline`).
- Alias skills matching the shared short names (`yaaif-login`, `yaaif-plan`,
  `yaaif-sync-scenario`, `yaaif-new-skill`, `yaaif-new-mcp`,
  `yaaif-new-workflow`, `yaaif-ops`).
- Scenario skill: `/yaaif-sync-scenario` shortcut and observe-by-default catalog
  ground rule.
- Inventory + skill-sync CI against `cursor-plugin` (IDE-token substitutions;
  alias skills allowlisted).
- Fix `interface.logo` to `assets/logo.svg`.

## 0.1.0

- Initial Codex plugin: nine skills, `.mcp.json` via
  `npx @yaaif/platform-mcp --client codex`, isolated `~/.yaaif/codex` state.
