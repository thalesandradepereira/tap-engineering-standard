"""Validate TAP Software Factory manifests, Skills and Graphify wiring (stdlib only)."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "tap-make-software", "tap-code-workspace", "tap-data-auth",
    "tap-mobile-factory", "tap-deploy-ops", "tap-qa-security",
    "tap-graphify", "tap-sandbox-executor", "tap-cloud-infrastructure",
}

def main():
    directory = ROOT / "plugins"
    found = {x.name for x in directory.iterdir() if x.is_dir() and (x / "plugin.json").exists()}
    assert found == EXPECTED, f"Unexpected plugin inventory: {found ^ EXPECTED}"
    inventory = json.loads((ROOT / "plugin-inventory.json").read_text(encoding="utf-8"))
    inv = {x["name"]: x for x in inventory["plugins"]}
    assert set(inv) == EXPECTED
    total = 0
    for name in sorted(EXPECTED):
        folder = directory / name
        manifest = json.loads((folder / "plugin.json").read_text(encoding="utf-8"))
        assert manifest["name"] == name
        assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
        assert len(manifest["extensions"]["com.openai"]["interface"]["shortDescription"]) <= 30
        skills = list(folder.glob("skills/*/SKILL.md"))
        assert skills and len(skills) == inv[name]["skills"], name
        for f in skills:
            text = f.read_text(encoding="utf-8")
            assert text.startswith("---\n"), f
            front = text.split("---", 2)[1]
            assert re.search(r"^name: " + re.escape(f.parent.name) + r"$", front, re.M), f
            assert re.search(r"^description: .+", front, re.M), f
            total += 1
        if (folder / "mcp.json").exists():
            assert json.loads((folder / "mcp.json").read_text(encoding="utf-8"))["mcpServers"]
        for f in folder.rglob("*"):
            assert not f.is_symlink(), f
            assert not (f.is_file() and f.name in {".env", "id_rsa", ".npmrc"}), f
    core = directory / "tap-make-software"
    assert len(list(core.glob("skills/*/SKILL.md"))) == 10
    for name in EXPECTED - {"tap-make-software"}:
        original = directory / name / "skills" / name / "SKILL.md"
        copy = core / "skills" / name / "SKILL.md"
        assert copy.read_bytes() == original.read_bytes(), name
    endpoint = "https://api.graphify.com/mcp"
    for name in ("tap-graphify", "tap-make-software"):
        mcp = json.loads((directory / name / "mcp.json").read_text(encoding="utf-8"))
        assert mcp["mcpServers"]["graphify"]["url"] == endpoint
    print(f"PASS: {len(EXPECTED)} plugins, {total} Skill files, 10 integrated Skills, Graphify MCP wiring")

if __name__ == "__main__":
    main()
