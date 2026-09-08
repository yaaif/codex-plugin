#!/usr/bin/env python3
"""Inventory and skill-sync checks for the YAAIF Codex plugin."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PLUGIN_VERSION = "1.3.0"
MCP_PACKAGE = "@yaaif/platform-mcp@1.3.1"

EXPECTED_SKILLS = (
    "yaaif-auth",
    "yaaif-create-ambient",
    "yaaif-create-mcp",
    "yaaif-create-skill",
    "yaaif-doctor",
    "yaaif-ops-support",
    "yaaif-plan-usecase",
    "yaaif-platform-tools",
    "yaaif-scenario",
)

ALIAS_SKILLS = (
    "yaaif-login",
    "yaaif-new-mcp",
    "yaaif-new-skill",
    "yaaif-new-workflow",
    "yaaif-ops",
    "yaaif-plan",
    "yaaif-sync-scenario",
)

_PROTECT = "cursor-plugin"


def canonicalize_skill_text(text: str) -> str:
    """Normalize IDE-specific tokens so Cursor and Codex skill copies can be compared."""
    protected = "\0CURSOR_PLUGIN\0"
    text = text.replace(_PROTECT, protected)
    text = text.replace("/yaaif-platform:", "/")
    text = text.replace("~/.yaaif/claude", "{{STATE}}")
    text = text.replace("~/.yaaif/cursor", "{{STATE}}")
    text = text.replace("~/.yaaif/codex", "{{STATE}}")
    text = text.replace("yaaif-claude", "{{OIDC}}")
    text = text.replace("yaaif-cursor", "{{OIDC}}")
    text = text.replace("yaaif-codex", "{{OIDC}}")
    text = text.replace("--client claude", "--client {{CLIENT}}")
    text = text.replace("--client cursor", "--client {{CLIENT}}")
    text = text.replace("--client codex", "--client {{CLIENT}}")
    text = text.replace("Claude Code", "{{IDE}}")
    text = text.replace("Cursor", "{{IDE}}")
    text = text.replace("Codex", "{{IDE}}")
    text = text.replace("MCP REST", "{{REST}}")
    text = text.replace("{{IDE}} REST", "{{REST}}")
    text = text.replace("The bridge discovers", "{{DISCOVERS}}")
    text = text.replace("{{IDE}} discovers", "{{DISCOVERS}}")
    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    return text.replace(protected, _PROTECT)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def plugin_root(repo_root: Path) -> Path:
    return repo_root / "plugins" / "yaaif-platform"


def check_inventory(repo_root: Path) -> list[str]:
    errors: list[str] = []
    root = plugin_root(repo_root)
    plugin_path = root / ".codex-plugin" / "plugin.json"
    mcp_path = root / ".mcp.json"
    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    logo = root / "assets" / "logo.svg"

    if not plugin_path.is_file():
        return [f"missing {plugin_path}"]
    plugin = _load_json(plugin_path)
    if plugin.get("version") != PLUGIN_VERSION:
        errors.append(f"plugin.json version {plugin.get('version')!r} != {PLUGIN_VERSION}")
    if plugin.get("name") != "yaaif-platform":
        errors.append(f"plugin.json name {plugin.get('name')!r} != 'yaaif-platform'")
    logo_ref = (plugin.get("interface") or {}).get("logo", "")
    if "logo.png" in logo_ref:
        errors.append(f"interface.logo still points at missing png: {logo_ref}")

    if not mcp_path.is_file():
        errors.append(f"missing {mcp_path}")
    else:
        mcp = _load_json(mcp_path)
        args = mcp.get("mcpServers", {}).get("yaaif", {}).get("args") or []
        if MCP_PACKAGE not in args:
            errors.append(f".mcp.json does not pin {MCP_PACKAGE}: {args}")
        if "--client" not in args or "codex" not in args:
            errors.append(f".mcp.json missing --client codex: {args}")

    if marketplace_path.is_file():
        market = _load_json(marketplace_path)
        plugins = market.get("plugins") or []
        if not plugins or plugins[0].get("version") != PLUGIN_VERSION:
            errors.append(f"marketplace.json plugin version != {PLUGIN_VERSION}")

    if not logo.is_file():
        errors.append("missing assets/logo.svg")

    skills_dir = root / "skills"
    allowed = set(EXPECTED_SKILLS) | set(ALIAS_SKILLS)
    for name in EXPECTED_SKILLS:
        skill = skills_dir / name / "SKILL.md"
        if not skill.is_file():
            errors.append(f"missing skill {skill}")
    for name in ALIAS_SKILLS:
        skill = skills_dir / name / "SKILL.md"
        if not skill.is_file():
            errors.append(f"missing alias skill {skill}")

    extra_skills = sorted(
        p.name for p in skills_dir.iterdir() if p.is_dir() and p.name not in allowed
    )
    if extra_skills:
        errors.append(f"unexpected skills: {extra_skills}")

    return errors


def _iter_skill_files(skills_root: Path) -> list[Path]:
    return sorted(p for p in skills_root.rglob("*") if p.is_file() and not p.name.startswith("."))


def check_skill_sync(repo_root: Path, cursor_root: Path) -> list[str]:
    errors: list[str] = []
    cursor_skills = cursor_root / "skills"
    codex_skills = plugin_root(repo_root) / "skills"
    if not cursor_skills.is_dir():
        return [f"cursor skills dir missing: {cursor_skills}"]

    cursor_files = {p.relative_to(cursor_skills): p for p in _iter_skill_files(cursor_skills)}
    core_codex = {
        p.relative_to(codex_skills): p
        for p in _iter_skill_files(codex_skills)
        if p.relative_to(codex_skills).parts[0] in EXPECTED_SKILLS
    }

    missing = sorted(cursor_files.keys() - core_codex.keys())
    extra = sorted(core_codex.keys() - cursor_files.keys())
    if missing:
        errors.append(f"codex skills missing vs cursor: {missing}")
    if extra:
        errors.append(f"codex core skills extra vs cursor: {extra}")

    for rel in sorted(cursor_files.keys() & core_codex.keys()):
        expected = canonicalize_skill_text(cursor_files[rel].read_text(encoding="utf-8"))
        actual = canonicalize_skill_text(core_codex[rel].read_text(encoding="utf-8"))
        if expected != actual:
            errors.append(f"skill drift after IDE substitutions: skills/{rel}")
    return errors


def resolve_cursor_root(explicit: str | None, repo_root: Path) -> Path | None:
    if explicit:
        return Path(explicit).expanduser().resolve()
    sibling = (repo_root / ".." / "cursor-plugin").resolve()
    if sibling.is_dir() and (sibling / "skills").is_dir():
        return sibling
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="codex-plugin repo root",
    )
    parser.add_argument(
        "--cursor-root",
        default=None,
        help="cursor-plugin root (defaults to ../cursor-plugin or CURSOR_PLUGIN_ROOT)",
    )
    parser.add_argument(
        "--require-skill-sync",
        action="store_true",
        help="fail if cursor-plugin skills are not available to compare",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    errors = check_inventory(root)

    cursor_root = resolve_cursor_root(args.cursor_root or os.environ.get("CURSOR_PLUGIN_ROOT"), root)
    if cursor_root is None:
        msg = "cursor-plugin skills not found (set --cursor-root or CURSOR_PLUGIN_ROOT)"
        if args.require_skill_sync:
            errors.append(msg)
        else:
            print(f"skip skill-sync: {msg}", file=sys.stderr)
    else:
        errors.extend(check_skill_sync(root, cursor_root))

    if errors:
        print("check-plugin failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("check-plugin ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
