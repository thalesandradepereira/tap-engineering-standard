#!/usr/bin/env python3
"""Bilingual Software Factory documentation quality gate (stdlib only)."""
from __future__ import annotations
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
HEADINGS = {
    "README.md": ("## Overview", "## Architecture", "### Implementation inventory", "## Current functionality and boundaries", "## Get started — MacBook", "## Quality assurance", "## Security, privacy and governance", "## Release and support"),
    "README.pt-BR.md": ("## Visão geral", "## Arquitetura", "### Inventário de módulos", "## Funcionalidades e limites reais", "## Primeiros passos — MacBook", "## Garantia de qualidade", "## Segurança, privacidade e governança", "## Versões e suporte"),
}
LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]+\")?\)")
SECRET = re.compile(r"(ghp_[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)")
def main():
    inventory = json.loads((ROOT / "plugin-inventory.json").read_text(encoding="utf-8"))["plugins"]
    assert len(inventory) == 10 and len({item["name"] for item in inventory}) == 10
    versions = {p["name"]: p["version"] for p in inventory}
    assert versions["tap-make-software"] == "4.1.0"
    assert versions["tap-studio-runtime"] == "0.2.0"
    errors = []
    count = 0
    for name, sections in HEADINGS.items():
        path = ROOT / name
        content = path.read_text(encoding="utf-8")
        if len(content) < 5500:
            errors.append(name + ": too short")
        for heading in sections:
            if heading not in content:
                errors.append(name + ": missing heading " + heading)
        for plugin, version in versions.items():
            if plugin not in content or version not in content:
                errors.append(name + ": missing " + plugin + " " + version)
        for word in ("Graphify", "Floot", "MacBook", "OAuth", "SQLite", "174"):
            if word not in content:
                errors.append(name + ": missing key fact " + word)
        if content.count(chr(96)*3 + "mermaid") != 1:
            errors.append(name + ": Mermaid architecture block missing")
        if SECRET.search(content):
            errors.append(name + ": potential credential")
        for url in LINK.findall(content):
            parts = urlsplit(url)
            if parts.scheme in ("http", "https", "mailto") or url.startswith("#"):
                continue
            if parts.scheme or url.startswith("//"):
                errors.append(name + ": bad URI " + url)
                continue
            destination = (path.parent / unquote(parts.path)).resolve()
            if not destination.is_relative_to(REPO.resolve()) or not destination.exists():
                errors.append(name + ": broken link " + url)
            else:
                count += 1
    if "[Português (Brasil)](README.pt-BR.md)" not in (ROOT / "README.md").read_text():
        errors.append("EN -> PT switch missing")
    if "[English](README.md)" not in (ROOT / "README.pt-BR.md").read_text():
        errors.append("PT -> EN switch missing")
    for root_doc, dest in (("README.md", "software-factory/README.md"), ("README.pt-BR.md", "software-factory/README.pt-BR.md")):
        if dest not in (REPO / root_doc).read_text():
            errors.append(root_doc + ": factory link missing")
    if errors:
        raise SystemExit("README QA FAILED:\n" + "\n".join(errors))
    print(f"README QA PASS: two languages, ten plugins, {count} internal links, architecture and governance")
if __name__ == "__main__":
    main()
