import logging
from abc import ABC, abstractmethod
from typing import AsyncGenerator, List

from dependencies import get_logger
from entity.mental_health import (
    EegProcessedData,
    EegUploadResponse,
    EmotionResult,
    MentalHealthResult,
)


class BaseEegService(ABC):
    logger: logging.Logger

    def __init__(self):
        self.logger = get_logger()

    @abstractmethod
    async def start(self, process_data_verbose: bool) -> bool:
        """
        start eeg service

        Returns:
            bool, True if start successfully, False otherwise
        """
        pass

    @abstractmethod
    async def stop(self) -> bool:
        """stop eeg service"""
        pass

    @abstractmethod
    async def calc_mental_health(self, eeg_data: List[int]) -> EegUploadResponse:
        """
        calculate mental health based on eeg data

        Args:
            eeg_data: bytes, eeg data

        Returns:
            EegResponse, mental health data
        """
        pass

    @abstractmethod
    async def upload(self, eeg_data: List[int]):
        """upload eeg data"""
        pass

    @abstractmethod
    async def subscrible_processed_data(
        self,
    ) -> AsyncGenerator[EegProcessedData, None]:
        """subscribe processed eeg data"""
        yield EegProcessedData()

    @abstractmethod
    async def subscribe_emotion(self) -> AsyncGenerator[EmotionResult, None]:
        """subscribe emotion data"""
        yield EmotionResult()

    @abstractmethod
    async def subscribe_mental_health(self) -> AsyncGenerator[MentalHealthResult, None]:
        """subscribe affective data"""
        yield MentalHealthResult()
