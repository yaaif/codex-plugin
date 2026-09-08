# Changelog

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
