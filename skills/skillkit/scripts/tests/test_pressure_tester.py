import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pressure_tester import PressureTester, PressureType, SkillType


def test_pressure_tester_initialization():
    tester = PressureTester()
    assert tester is not None
    assert hasattr(tester, 'pressure_types')


def test_run_pressure_scenario_returns_result():
    tester = PressureTester()
    result = tester.run_scenario(
        skill_path="test-skill",
        pressure_type=PressureType.TIME,
        skill_type=SkillType.DISCIPLINE,
    )
    assert result is not None
    assert 'compliance_score' in result
    assert 'rationalizations_found' in result
