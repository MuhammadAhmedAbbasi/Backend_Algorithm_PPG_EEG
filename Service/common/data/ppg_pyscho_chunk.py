from pydantic import BaseModel

class PPGChunkPredictResult(BaseModel):
    depression: list[int]
    anxiety: list[int]
    stress: list[int]
    vitality: list[int]
    #insomnia: list[int]