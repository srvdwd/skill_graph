from pydantic import BaseModel


class SkillSummary(BaseModel):
    id: str
    name: str
    category: str
    description: str


class RelatedSkill(BaseModel):
    id: str
    name: str
    relationship: str  # "RELATED_TO" | "PREREQUISITE_FOR" | "REQUIRES_PREREQUISITE"


class SkillDetail(BaseModel):
    id: str
    name: str
    category: str
    description: str
    related_skills: list[RelatedSkill]
