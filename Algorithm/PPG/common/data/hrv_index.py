from pydantic import BaseModel
import numpy as np


class HrvIndex(BaseModel):
    HRV_SDNN: float
    HRV_RMSSD: float
    HRV_pNN50: float
    HRV_HF: float
    HRV_LF: float
    HRV_LFHF: float