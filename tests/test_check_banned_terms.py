import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_banned_terms as c


class ScanTests(unittest.TestCase):
    def test_built_in_patterns_catch_leaks(self):
        for text in ("mail me at someone@example.com", "see /Users/anyone/project", "key abcdefghijklmnopqrstuvwxyz012345"):
            self.assertTrue(c.scan_text(text, c.BUILT_IN), text)

    def test_clean_text_passes(self):
        self.assertEqual(c.scan_text("A pipeline with 500+ tests and one scoring method.", c.BUILT_IN), [])

    def test_local_terms_file_is_applied_and_case_insensitive(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / ".banned-terms").write_text("# comment\nsecretword\n", encoding="utf-8")
            (root / "a.md").write_text("This mentions SecretWord here.\n", encoding="utf-8")
            self.assertEqual(c.main([], root=root), 1)
            (root / "a.md").write_text("Nothing to see.\n", encoding="utf-8")
            self.assertEqual(c.main([], root=root), 0)


if __name__ == "__main__":
    unittest.main()
