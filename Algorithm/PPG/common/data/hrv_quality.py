from pydantic import BaseModel
import numpy as np


class HrvQuality(BaseModel):
    q_SDNN: float
    q_RMSSD: float
    q_LHF: float
    q_pNN50: float