from pydantic import BaseModel

class ppg_pyscho_result(BaseModel):
    depression: int
    anxiety: int
    stress: int
    vitality: int
    #insomnia: int