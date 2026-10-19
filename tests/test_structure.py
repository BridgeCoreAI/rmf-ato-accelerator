import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SUMMARY = ROOT / "RMF_Executive_Summary.md"
LICENSE_FILE = ROOT / "LICENSE"


class TestFilesExist(unittest.TestCase):
    def test_expected_files(self):
        for f in (README, SUMMARY, LICENSE_FILE):
            self.assertTrue(f.is_file(), f"missing {f.name}")


class TestClaimsAreCalibrated(unittest.TestCase):
    """Enforces the calibrated-claims rule: this public repo is a published
    OVERVIEW; the full implementation is access-gated. If these fail, a
    headline has drifted back into overclaiming: fix the TEXT, not the test."""

    def test_no_overclaim_headline(self):
        for f in (README, SUMMARY):
            text = f.read_text(encoding="utf-8")
            self.assertNotIn("Published Reference Implementation", text,
                             f"{f.name}: overclaiming headline present")

    def test_access_gate_is_stated(self):
        for f in (README, SUMMARY):
            text = f.read_text(encoding="utf-8")
            self.assertIn("available upon request", text,
                          f"{f.name}: access gate not stated")


class TestVersioning(unittest.TestCase):
    def test_version_present_and_consistent(self):
        v_re = re.compile(r"v\d+\.\d+\.\d+")
        versions = set()
        for f in (README, SUMMARY):
            found = v_re.findall(f.read_text(encoding="utf-8"))
            self.assertTrue(found, f"{f.name}: no version string")
            versions.update(found)
        self.assertEqual(len(versions), 1, f"version drift: {versions}")


class TestLicensePosture(unittest.TestCase):
    def test_license_states_proprietary_posture(self):
        text = LICENSE_FILE.read_text(encoding="utf-8")
        self.assertIn("All rights reserved", text)


class TestSummarySubstance(unittest.TestCase):
    def test_executive_summary_is_substantive(self):
        words = len(SUMMARY.read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 150, f"summary only {words} words")
