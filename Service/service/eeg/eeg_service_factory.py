from .base_eeg_service import BaseEegService
from .enter_tech_eeg_service import EnterTechEegService


class EegServiceFactory(object):
    @staticmethod
    def create() -> BaseEegService:
        """create eeg service"""
        return EnterTechEegService()
