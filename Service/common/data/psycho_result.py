from pydantic import BaseModel


class PsychoResult(BaseModel):
    depression: int
    anxiety: int
    stress: int
    vitality: int