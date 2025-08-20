from enum import Enum
from pydantic import BaseModel


class MentalHealthType(Enum):
    DEPRESSION = "depression"
    ANXIETY = "anxiety"
    FATIGUE = "fatigue"
    STRESS = 'stress'
    VITALITY = 'vitality'
    ATTENTION = 'attention'


class EmotionType(Enum):
    ATTENTION = "attention"
    RELAX = "relax"
    STRESS = "stress"
    ENJOYMENT = "enjoyment"


class MentalHealthResult(BaseModel):
    """
    心理健康数据分析结果

    Properties:
        type (MentalHealthType): 类型，如抑郁状态，焦虑状态
        value (int): 值
    """

    type: MentalHealthType = MentalHealthType.DEPRESSION  # 类型
    value: int = 0  # 值


class EmotionResult(BaseModel):
    """
    情感数据分析结果

    Properties:
        type (EmotionType): 类型，如注意力，放松度，压力水平，愉悦度
        value (float): 值
    """

    type: EmotionType = EmotionType.ATTENTION  # 类型
    value: float = 0  # 值
