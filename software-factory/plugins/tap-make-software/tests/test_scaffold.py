"""Negative and positive checks for the pure-Python scaffolder."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from html.parser import HTMLParser

SOURCE = Path(__file__).resolve().parents[1] / "tools" / "scaffold.py"
spec = importlib.util.spec_from_file_location("tap_scaffold", SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "script": self.references.append(attrs.get("src"))

class ScaffoldTests(unittest.TestCase):
    def test_generates_complete_demo(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = mod.generate("meu-projeto", Path(tmp))
            self.assertEqual(set(x.name for x in out.iterdir()), {"index.html","style.css","app.js","sw.js","manifest.webmanifest","README.md"})
            p = Markup();p.feed((out/"index.html").read_text())
            self.assertTrue({"new-task","tasks","title","status","search","filter","export","empty","count"} <= p.ids)
            self.assertEqual(p.references, ["./app.js"])
            self.assertEqual(json.loads((out/"manifest.webmanifest").read_text())["display"], "standalone")
            self.assertIn("textContent=task.title",(out/"app.js").read_text())
    def test_blocks_path_traversal_and_invalid_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("../outside", "a/b", "-x", "a--b", "A", "a-", "", ".env", "a b", "á"):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    mod.generate(name, Path(tmp))
    def test_refuses_overwrite_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = mod.generate("demo", Path(tmp))
            before = (out / "index.html").read_bytes()
            with self.assertRaises(FileExistsError): mod.generate("demo", Path(tmp))
            self.assertEqual((out / "index.html").read_bytes(),before)
    def test_refuses_unknown_template(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
            mod.generate("demo", Path(tmp), "fullstack")
    def test_no_external_runtime_dependencies(self):
        s=SOURCE.read_text()
        for banned in ("subprocess", "requests", "urllib", "http.client", "os.system", "eval(", "exec("):
            self.assertNotIn(banned,s)

if __name__ == "__main__": unittest.main()
