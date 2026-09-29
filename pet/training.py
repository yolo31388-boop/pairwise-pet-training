"""宠物训练与技能树系统"""
import math
from dataclasses import dataclass, field

QUALITY_MULTIPLIER = {
    "common": 1.0,
    "uncommon": 1.2,
    "rare": 1.5,
    "epic": 2.0,
    "legendary": 3.0,
}

SKILL_BRANCHES = {
    "physical": ["attack", "defense", "support"],
    "magical": ["attack", "defense", "support"],
    "hybrid": ["attack", "defense", "support"],
}

SKILL_PREREQUISITES = {
    "basic_attack": [],
    "advanced_attack": ["basic_attack"],
    "ultimate": ["advanced_attack"],
    "basic_defense": [],
    "advanced_defense": ["basic_defense"],
    "basic_support": [],
    "advanced_support": ["basic_support"],
}

MUTUALLY_EXCLUSIVE_PAIRS = {
    frozenset({"berserker", "defender"}),
    frozenset({"glass_cannon", "tank"}),
    frozenset({"healer", "necromancer"}),
}

RESET_REFUND_RATE = 1.0


@dataclass
class Pet:
    pid: str
    name: str
    level: int = 1
    quality: str = "common"
    pet_type: str = "physical"
    training_points: int = 0
    skills: list = field(default_factory=list)


class TrainingSystem:
    def __init__(self):
        self.pets: dict[str, Pet] = {}
        self.skill_tree: dict = {t: list(b) for t, b in SKILL_BRANCHES.items()}

    def get_training_points(self, level: int, quality: str) -> int:
        multiplier = QUALITY_MULTIPLIER.get(quality, 1.0)
        return int(level * multiplier)

    def get_skill_branches(self, pet_type: str) -> list:
        return list(self.skill_tree.get(pet_type, SKILL_BRANCHES["physical"]))

    def has_prerequisite(self, skill_id: str, learned: list) -> bool:
        prereqs = SKILL_PREREQUISITES.get(skill_id, [])
        return all(p in learned for p in prereqs)

    def reset_training(self, pid: str) -> int:
        pet = self.pets.get(pid)
        if pet is None:
            return 0
        refund = int(pet.training_points * RESET_REFUND_RATE)
        pet.training_points = 0
        pet.skills.clear()
        return refund

    def get_training_effect(self, level: int) -> float:
        return 5.0 * math.sqrt(level)

    def can_train_type(self, pet_type: str, training_type: str) -> bool:
        if pet_type == "hybrid":
            return True
        return pet_type == training_type

    def meets_level_req(self, pet_level: int, skill_level: int) -> bool:
        return pet_level >= skill_level

    def are_skills_mutually_exclusive(self, s1: str, s2: str) -> bool:
        return frozenset({s1, s2}) in MUTUALLY_EXCLUSIVE_PAIRS
