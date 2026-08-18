from pydantic import BaseModel


class CareerSummary(BaseModel):
    id: str
    title: str
    description: str


class SkillRef(BaseModel):
    id: str
    name: str
    category: str


class CareerDetail(BaseModel):
    id: str
    title: str
    description: str
    required_skills: list[SkillRef]
