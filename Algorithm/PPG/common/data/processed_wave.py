from pydantic import BaseModel
from typing import List
class ProcessedWave(BaseModel):
    processed_wave: List[float]
    wave_quality: float