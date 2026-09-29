"""宠物训练与技能树系统 - 含8个bug"""
from dataclasses import dataclass, field

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
        self.skill_tree: dict = {}  # bug2: 无分支

    def get_training_points(self, level: int, quality: str) -> int:
        # bug1: 固定点数
        return 10

    def get_skill_branches(self, pet_type: str) -> list:
        # bug2: 无分支
        return ["main"]

    def has_prerequisite(self, skill_id: str, learned: list) -> bool:
        # bug3: 无前置
        return True

    def reset_training(self, pid: str) -> int:
        # bug4: 不返还
        return 0

    def get_training_effect(self, level: int) -> float:
        # bug5: 线性
        return level * 5.0

    def can_train_type(self, pet_type: str, training_type: str) -> bool:
        # bug6: 跨类型
        return True

    def meets_level_req(self, pet_level: int, skill_level: int) -> bool:
        # bug7: 无等级要求
        return True

    def are_skills_mutually_exclusive(self, s1: str, s2: str) -> bool:
        # bug8: 无互斥
        return False
