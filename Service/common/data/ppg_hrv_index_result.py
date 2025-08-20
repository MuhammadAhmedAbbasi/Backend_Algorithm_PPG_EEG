from pydantic import BaseModel
from Algorithm.PPG.common.data.hrv_index import HrvIndex
from Algorithm.PPG.common.data.hrv_quality import HrvQuality

class PPGHrvIndexResult(BaseModel):
    hrv_index: HrvIndex
    hrv_quality: HrvQuality