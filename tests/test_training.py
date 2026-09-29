"""宠物训练与技能树系统 - 红态测试"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pet.training import TrainingSystem, Pet

class TestTrainingPoints:
    def test_legendary_pet_gets_more_points(self):
        ts = TrainingSystem()
        p1 = ts.get_training_points(10, "common")
        p2 = ts.get_training_points(10, "legendary")
        assert p2 > p1

class TestSkillBranches:
    def test_multiple_skill_branches(self):
        ts = TrainingSystem()
        branches = ts.get_skill_branches("physical")
        assert len(branches) > 1

class TestPrerequisite:
    def test_ultimate_skill_needs_prerequisite(self):
        ts = TrainingSystem()
        assert ts.has_prerequisite("ultimate", []) == False

class TestResetRefund:
    def test_reset_returns_training_points(self):
        ts = TrainingSystem()
        ts.pets["p1"] = Pet("p1", "pet", training_points=5)
        refund = ts.reset_training("p1")
        assert refund > 0

class TestDiminishingReturns:
    def test_high_level_training_diminishes(self):
        ts = TrainingSystem()
        e1 = ts.get_training_effect(1)
        e10 = ts.get_training_effect(10)
        assert e10 < e1 * 10

class TestTypeRestriction:
    def test_physical_pet_cannot_train_magic(self):
        ts = TrainingSystem()
        assert ts.can_train_type("physical", "magical") == False

class TestLevelRequirement:
    def test_low_level_cannot_train_high_skill(self):
        ts = TrainingSystem()
        assert ts.meets_level_req(1, 50) == False

class TestMutualExclusivity:
    def test_some_skills_are_mutually_exclusive(self):
        ts = TrainingSystem()
        assert ts.are_skills_mutually_exclusive("berserker", "defender") == True
