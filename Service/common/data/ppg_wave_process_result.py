from pydantic import BaseModel
from typing import List


class PPGWaveProcessResult(BaseModel):
    raw_wave: List
    processed_wave: List[float]
    wave_quality: float