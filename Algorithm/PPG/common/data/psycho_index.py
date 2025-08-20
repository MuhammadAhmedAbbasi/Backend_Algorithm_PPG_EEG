from pydantic import BaseModel
import numpy as np


class PsychoIndex(BaseModel):
    depression_prediction: int
    anxiety_prediction: int
    stress_prediction: int
    vitality_prediction: int
    insomnia_prediction: int