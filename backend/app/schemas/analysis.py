from pydantic import BaseModel, Field


class SkillGapRequest(BaseModel):
    known_skill_ids: list[str] = Field(
        default_factory=list,
        description="IDs of skills the user already has",
    )
    target_career_id: str = Field(description="ID of the career the user wants to reach")


class Resource(BaseModel):
    id: str
    title: str
    url: str
    type: str


class MissingSkill(BaseModel):
    id: str
    name: str
    category: str
    resources: list[Resource]


class SkillGapResponse(BaseModel):
    target_career_id: str
    target_career_title: str
    required_skill_count: int
    known_skill_count: int
    missing_skills: list[MissingSkill]


class LearningPathStep(BaseModel):
    id: str
    name: str


class LearningPathResponse(BaseModel):
    from_skill_id: str
    to_skill_id: str
    path_found: bool
    hop_count: int
    path: list[LearningPathStep]
