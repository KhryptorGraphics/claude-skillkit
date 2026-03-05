"""
Integration test for skillkit v2 full workflow.
Tests all components working together.
"""

import json
import subprocess
import tempfile
from pathlib import Path


class TestFullWorkflow:
    """End-to-end test of full mode workflow."""

    REPO_ROOT = Path(__file__).resolve().parents[4]

    def test_decision_helper_recommends_mode(self):
        """Decision helper should recommend mode."""
        result = subprocess.run(
            [
                "python3",
                "skills/skillkit/scripts/decision_helper.py",
                "--analyze",
                "TDD discipline skill",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
            cwd=str(self.REPO_ROOT),
        )

        output = json.loads(result.stdout)
        assert "workflow_mode" in output

    def test_pressure_tester_runs(self):
        """Pressure tester should execute and return results (v2 stub returns hardcoded values)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    "python3",
                    "skills/skillkit/scripts/pressure_tester.py",
                    tmpdir,
                    "--pressure",
                    "time",
                    "--skill-type",
                    "discipline",
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                cwd=str(self.REPO_ROOT),
            )

            output = json.loads(result.stdout)
            # Assert structural shape only (v2 stub returns hardcoded values)
            assert "compliance_score" in output
            assert "status" in output
            assert "rationalizations_found" in output

    def test_quality_scorer_behavioral(self):
        """Quality scorer should include behavioral when --behavioral flag used."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "test-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("---\nname: test\n---\n# Test\n")

            result = subprocess.run(
                [
                    "python3",
                    "skills/skillkit/scripts/quality_scorer.py",
                    str(skill_dir),
                    "--behavioral",
                    "--skill-type",
                    "discipline",
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                cwd=str(self.REPO_ROOT),
            )

            output = json.loads(result.stdout)
            assert output.get("mode") == "full"
