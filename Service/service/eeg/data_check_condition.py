from abc import ABC, abstractmethod
from .eeg_data_check import Filter, FFTDataCheck

class DataChecker(ABC):
    @abstractmethod
    def check_data_conditions(self, fp1_data: list, fp2_data: list) -> bool:
        """
        Abstract method to check specific conditions on FP1 and FP2 data.

        Parameters:
        fp1_data (list<float>): FP1 channel data.
        fp2_data (list<float>): FP2 channel data.

        Returns:
        bool: True if conditions are met, False otherwise.
        """
        pass

class FFTValueChecker(DataChecker):
    def __init__(self):
        self.threshold = 0.1
        self.filter = FFTDataCheck()

    def check_data_conditions(self, fp1_data, fp2_data):
        # Check if percentage of zeros exceeds threshold in either data set
        if (fp1_data.count(0) / len(fp1_data) > self.threshold) or (fp2_data.count(0) / len(fp2_data) > self.threshold):
            return False
        
        # Check if both datasets pass the FFT filter validity check
        if not (self.filter.is_valid(fp1_data) and self.filter.is_valid(fp2_data)):
            return False
        
        return True
