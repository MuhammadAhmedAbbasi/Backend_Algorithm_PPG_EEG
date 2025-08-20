import numpy as np
from abc import ABC, abstractmethod
from scipy.fftpack import fft

class Filter(ABC):
    def __init__(self):
        pass
        
    @abstractmethod
    def is_valid(self, datas: list) -> bool:
        pass

class FFTDataCheck(Filter):
    def __init__(self, threshold: int = 9):
        """
        初始化FFTDataCheck类
        """
        super().__init__()
        self.threshold = threshold
    
    def is_valid(self, data: list) -> bool:
        """
        检查数据质量
        
        参数:
            data (list): 需要处理的数据列表。
            num (int): 取样点数，默认为500。
        
        返回:
            bool: 如果最大值小于9，返回False，否则返回True。
        """

        # Perform FFT and check condition
        data_fft = np.fft.fft(data)  # 修改这里
        return np.max(2.0 / len(data) * np.abs(data_fft[:len(data) // 2])) > self.threshold