from typing import Optional
from pydantic import BaseModel


class EegMentalHealth(BaseModel):
    """
    eeg心理健康数据分析结果

    Properties:
        depressionLevel (int): 抑郁状态
        anxietyLevel (int): 焦虑状态
        attention (float): 注意力
        relax (float): 放松度
        stress (float): 压力水平
        enjoyment (float): 愉悦度
    """

    depressionLevel: int = 0  # 抑郁状态
    anxietyLevel: int = 0  # 焦虑状态

    attention: float = 0  # 注意力
    relax: float = 0  # 放松度
    stress: float = 0  # 压力水平
    enjoyment: float = 0  # 愉悦度


class EegProcessedData(BaseModel):
    """
    eeeg数据处理结果

    Properties:
        eeg_left_wave (list[float]): 左脑波
        eeg_right_wave (list[float]): 右脑波

        eeg_alpha_power (float): α频段能量占比
        eeg_beta_power (float): β频段能量占比
        eeg_theta_power (float): θ频段能量占比
        eeg_delta_power (float): δ频段能量占比
        eeg_gamma_power (float): γ频段能量占比
    """

    eeg_left_wave: list[float] = []  # 左脑波
    eeg_right_wave: list[float] = []  # 右脑波

    eeg_alpha_power: float = 0.0  # α频段能量占比
    eeg_beta_power: float = 0.0  # β频段能量占比
    eeg_theta_power: float = 0.0  # θ频段能量占比
    eeg_delta_power: float = 0.0  # δ频段能量占比
    eeg_gamma_power: float = 0.0  # γ频段能量占比


class EegStartResponse(BaseModel):
    """
    eeg命令响应
    """

    session_id: str = ""  # 会话id
    upload_bytes_size: int = 150 * 3  # 上传数据大小


class EegUploadResponse(BaseModel):
    """
    eeg数据分析结果

    Properties:
        eeg_mental_health (EegMentalHealth): eeg心理健康数据分析结果
        eeg_processed_data (Optional[EegProcesssedData]): eeg数据处理结果
    """

    eeg_mental_health: EegMentalHealth = EegMentalHealth()  # eeg心理健康数据分析结果
    eeg_processed_data: Optional[EegProcessedData] = None  # eeg数据处理结果
