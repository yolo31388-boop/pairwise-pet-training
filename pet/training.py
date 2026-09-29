"""宠物训练与技能树系统"""
import math
from dataclasses import dataclass, field

# 品质训练点倍率：品质越高，每级获得的训练点越多
QUALITY_MULTIPLIER = {
    "common": 1.0,
    "uncommon": 1.2,
    "rare": 1.5,
    "epic": 2.0,
    "legendary": 3.0,
}

# 三大技能分支：攻击 / 防御 / 辅助
SKILL_BRANCHES = ("attack", "defense", "support")

# 所有宠物类型均可学习的通用训练类型
UNIVERSAL_TRAINING_TYPE = "universal"


@dataclass
class Pet:
    pid: str
    name: str
    level: int = 1
    quality: str = "common"
    pet_type: str = "physical"
    training_points: int = 0
    skills: list = field(default_factory=list)
    spent_points: int = 0  # 已投入技能树的训练点，洗点时据此返还


@dataclass(frozen=True)
class SkillNode:
    skill_id: str
    name: str
    pet_type: str
    branch: str
    level_req: int          # 学习所需的宠物等级
    cost: int               # 消耗的训练点
    prerequisites: tuple = ()
    conflicts: tuple = ()


def _build_skill_tree() -> dict:
    """按宠物类型与分支构建技能树，节点带前置、等级与互斥信息。"""
    nodes = [
        # 物理宠物 - 攻击分支
        SkillNode("basic_strike", "基础打击", "physical", "attack", 1, 1),
        SkillNode("power_attack", "强力攻击", "physical", "attack", 10, 2,
                  prerequisites=("basic_strike",)),
        SkillNode("berserker", "狂战士", "physical", "attack", 20, 3,
                  prerequisites=("power_attack",), conflicts=("defender",)),
        SkillNode("ultimate", "终极奥义", "physical", "attack", 40, 5,
                  prerequisites=("berserker",)),
        # 物理宠物 - 防御分支
        SkillNode("iron_skin", "铁皮", "physical", "defense", 1, 1),
        SkillNode("tough_body", "坚韧体魄", "physical", "defense", 10, 2,
                  prerequisites=("iron_skin",)),
        SkillNode("defender", "守护者", "physical", "defense", 20, 3,
                  prerequisites=("tough_body",), conflicts=("berserker",)),
        # 物理宠物 - 辅助分支
        SkillNode("rally", "鼓舞", "physical", "support", 1, 1),
        SkillNode("battle_cry", "战吼", "physical", "support", 10, 2,
                  prerequisites=("rally",)),
        SkillNode("warlord", "督军", "physical", "support", 20, 3,
                  prerequisites=("battle_cry",)),
        # 法术宠物 - 攻击分支
        SkillNode("magic_bolt", "魔法飞弹", "magical", "attack", 1, 1),
        SkillNode("fireball", "火球术", "magical", "attack", 10, 2,
                  prerequisites=("magic_bolt",)),
        SkillNode("archmage", "大法师", "magical", "attack", 20, 3,
                  prerequisites=("fireball",), conflicts=("rune_warden",)),
        SkillNode("ultimate_spell", "终极法术", "magical", "attack", 40, 5,
                  prerequisites=("archmage",)),
        # 法术宠物 - 防御分支
        SkillNode("magic_barrier", "魔法屏障", "magical", "defense", 1, 1),
        SkillNode("frost_armor", "冰霜护甲", "magical", "defense", 10, 2,
                  prerequisites=("magic_barrier",)),
        SkillNode("rune_warden", "符文守卫", "magical", "defense", 20, 3,
                  prerequisites=("frost_armor",), conflicts=("archmage",)),
        # 法术宠物 - 辅助分支
        SkillNode("heal", "治疗术", "magical", "support", 1, 1),
        SkillNode("bless", "祝福", "magical", "support", 10, 2,
                  prerequisites=("heal",)),
        SkillNode("saint", "圣者", "magical", "support", 20, 3,
                  prerequisites=("bless",)),
    ]
    tree: dict = {}
    for node in nodes:
        tree[node.skill_id] = node
    return tree


class TrainingSystem:
    def __init__(self):
        self.pets: dict[str, Pet] = {}
        self.skill_tree: dict[str, SkillNode] = _build_skill_tree()

    def get_training_points(self, level: int, quality: str) -> int:
        """训练点 = 等级 × 品质倍率，传说宠物更多。"""
        if level < 1:
            return 0
        multiplier = QUALITY_MULTIPLIER.get(quality, 1.0)
        return max(1, int(level * multiplier))

    def get_skill_branches(self, pet_type: str) -> list:
        """技能树按宠物类型展开为攻击/防御/辅助多个分支。"""
        available = {
            node.pet_type for node in self.skill_tree.values()
        }
        if pet_type not in available:
            raise ValueError(f"unknown pet type: {pet_type}")
        return list(SKILL_BRANCHES)

    def has_prerequisite(self, skill_id: str, learned: list) -> bool:
        """必须已学会技能的全部前置技能。"""
        node = self.skill_tree.get(skill_id)
        if node is None:
            return False
        learned_set = set(learned)
        return all(req in learned_set for req in node.prerequisites)

    def reset_training(self, pid: str) -> int:
        """洗点：清空已学技能，全额返还已投入与未使用的训练点。"""
        pet = self.pets[pid]
        refund = pet.spent_points + pet.training_points
        pet.skills.clear()
        pet.spent_points = 0
        pet.training_points = refund
        return refund

    def get_training_effect(self, level: int) -> float:
        """训练效果按等级开方增长，等级越高边际收益越小。"""
        if level <= 0:
            return 0.0
        return 5.0 * math.sqrt(level)

    def can_train_type(self, pet_type: str, training_type: str) -> bool:
        """只能学习与自身宠物类型一致的训练（通用训练除外）。"""
        if training_type == UNIVERSAL_TRAINING_TYPE:
            return True
        return pet_type == training_type

    def meets_level_req(self, pet_level: int, skill_level: int) -> bool:
        """宠物等级达到技能要求才可学习。"""
        return pet_level >= skill_level

    def are_skills_mutually_exclusive(self, s1: str, s2: str) -> bool:
        """互斥节点：学会其中一个后另一个锁定。"""
        node = self.skill_tree.get(s1)
        if node is not None and s2 in node.conflicts:
            return True
        other = self.skill_tree.get(s2)
        if other is not None and s1 in other.conflicts:
            return True
        return False

    def learn_skill(self, pid: str, skill_id: str) -> None:
        """学习技能：依次校验类型、等级、前置、互斥与训练点。"""
        pet = self.pets[pid]
        node = self.skill_tree.get(skill_id)
        if node is None:
            raise ValueError(f"unknown skill: {skill_id}")
        if not self.can_train_type(pet.pet_type, node.pet_type):
            raise ValueError(
                f"pet type {pet.pet_type} cannot learn {node.pet_type} skill"
            )
        if not self.meets_level_req(pet.level, node.level_req):
            raise ValueError(
                f"pet level {pet.level} < required {node.level_req}"
            )
        if skill_id in pet.skills:
            raise ValueError(f"skill already learned: {skill_id}")
        if not self.has_prerequisite(skill_id, pet.skills):
            raise ValueError(f"prerequisite not met for {skill_id}")
        for learned in pet.skills:
            if self.are_skills_mutually_exclusive(skill_id, learned):
                raise ValueError(f"{skill_id} conflicts with {learned}")
        if pet.training_points < node.cost:
            raise ValueError("not enough training points")
        pet.training_points -= node.cost
        pet.spent_points += node.cost
        pet.skills.append(skill_id)
