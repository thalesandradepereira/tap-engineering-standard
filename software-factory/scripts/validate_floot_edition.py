#!/usr/bin/env python3
"""Validate published Floot edition traceability snapshot (no Floot API needed)."""
from pathlib import Path
import json
import re
ROOT = Path(__file__).resolve().parents[1] / "floot-edition"
def main():
    manifest=json.loads((ROOT/"snapshot-manifest.json").read_text())
    assert manifest["release"]=="0.1.0"
    assert manifest["public_url"]=="https://tap-software-factory.floot.app"
    assert len(manifest["files"])==19 and len(set(manifest["files"]))==19
    for item in manifest["files"]:
        p=(ROOT/"snapshot"/item).resolve()
        assert p.is_relative_to((ROOT/"snapshot").resolve()) and p.is_file(),item
        content=p.read_text()
        assert not re.search(r"ptoken=|ghp_[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|-----BEGIN .*PRIVATE KEY-----",content),item
    for doc in ["README.md","README.pt-BR.md","QA_STATUS.md","schema.sql"]:
        assert (ROOT/doc).is_file(),doc
    for doc in ["README.md","README.pt-BR.md"]:
        content=(ROOT/doc).read_text()
        for token in ["v0.1.0","https://tap-software-factory.floot.app","Graphify","GitHub","MacBook","PostgreSQL"]:
            assert token in content,(doc,token)
    print("Floot snapshot QA PASS: 19 files, bilingual docs, source provenance, no preview tokens.")
if __name__=="__main__":main()
