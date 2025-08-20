from pydantic import BaseModel
from typing import List

class PPGWaveResult(BaseModel):
    raw_wave: List[float]
    processed_wave: List[float]
    #wave_quality: float