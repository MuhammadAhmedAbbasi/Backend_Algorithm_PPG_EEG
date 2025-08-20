import asyncio
from typing import Any, AsyncIterator, Callable

import grpc
from entity.mental_health.base import (
    EmotionResult,
    EmotionType,
    MentalHealthResult,
    MentalHealthType,
)
from entity.mental_health.eeg_response import EegProcessedData
from google.protobuf.empty_pb2 import Empty

from service.eeg import BaseEegService, EegServiceFactory

from ..generated import affective_pb2, eeg_pb2, eeg_pb2_grpc, mentalHealth_pb2

mental_health_typ_mapping: dict[
    MentalHealthType, mentalHealth_pb2.MentalHealthType.ValueType
] = {
    MentalHealthType.DEPRESSION: mentalHealth_pb2.MentalHealthType.Depression,
    MentalHealthType.ANXIETY: mentalHealth_pb2.MentalHealthType.Anxiety,
    MentalHealthType.STRESS: mentalHealth_pb2.MentalHealthType.Stress,
    MentalHealthType.VITALITY: mentalHealth_pb2.MentalHealthType.Vitality,
    MentalHealthType.FATIGUE: mentalHealth_pb2.MentalHealthType.Fatigue,
    MentalHealthType.ATTENTION: mentalHealth_pb2.MentalHealthType.Attention
}

affective_typ_mapping: dict[EmotionType, affective_pb2.AffectiveType.ValueType] = {
    EmotionType.ATTENTION: affective_pb2.AffectiveType.Attention,
    EmotionType.RELAX: affective_pb2.AffectiveType.Relax,
    EmotionType.STRESS: affective_pb2.AffectiveType.Stress,
    EmotionType.ENJOYMENT: affective_pb2.AffectiveType.Enjoyment,
}


class EegService(eeg_pb2_grpc.EegServicer):
    """
    implement the eeg service
    """

    async def Start(
        self, request: eeg_pb2.EegStartRequest, context: grpc.aio.ServicerContext
    ) -> eeg_pb2.EegStartRely:
        """
        start eeg service
        """

        self.__eeg_service: BaseEegService = EegServiceFactory.create()
        success = await self.__eeg_service.start(request.processDataVerbose)

        return eeg_pb2.EegStartRely(success=success)

    async def Stop(
        self, request: eeg_pb2.EegStopRequest, context: grpc.aio.ServicerContext
    ) -> Empty:
        """
        stop eeg service
        """

        await self.__eeg_service.stop()
        return Empty()

    async def Upload(
        self,
        request_iterator: AsyncIterator[eeg_pb2.EegUploadRequest],
        context: grpc.aio.ServicerContext,
    ):
        """
        upload eeg data
        """

        lock = asyncio.Lock()

        async def process_data_stream(
            data_stream: AsyncIterator,
            response_creator: Callable[[Any], eeg_pb2.MixedUploadReply],
        ):
            async for data in data_stream:
                async with lock:
                    try:
                        processed_data = response_creator(data)
                        await context.write(processed_data)
                    except Exception as e:
                        print(e)

        async def receive_processed_data():
            def map_processed_data(data: EegProcessedData) -> eeg_pb2.MixedUploadReply:
                return eeg_pb2.MixedUploadReply(
                    processedData=eeg_pb2.EegProcessedData(
                        eegLeftWave=data.eeg_left_wave,
                        eegRightWave=data.eeg_right_wave,
                        eegAlphaPower=data.eeg_alpha_power,
                        eegBetaPower=data.eeg_beta_power,
                        eegThetaPower=data.eeg_theta_power,
                        eegDeltaPower=data.eeg_delta_power,
                        eegGammaPower=data.eeg_gamma_power,
                    )
                )

            await process_data_stream(
                self.__eeg_service.subscrible_processed_data(),
                map_processed_data,
            )

        async def receive_emotion_data():
            def map_emotion_data(data: EmotionResult) -> eeg_pb2.MixedUploadReply:
                return eeg_pb2.MixedUploadReply(
                    affectiveData=affective_pb2.AffectiveData(
                        type=affective_typ_mapping[data.type], value=data.value
                    )
                )

            await process_data_stream(
                self.__eeg_service.subscribe_emotion(), map_emotion_data
            )

        async def receive_mental_health_data():
            def map_mental_health_data(
                data: MentalHealthResult,
            ) -> eeg_pb2.MixedUploadReply:
                return eeg_pb2.MixedUploadReply(
                    mentalHealthLevel=mentalHealth_pb2.MentalHealthLevel(
                        type=mental_health_typ_mapping[data.type], level=data.value
                    )
                )

            await process_data_stream(
                self.__eeg_service.subscribe_mental_health(), map_mental_health_data
            )

        processed_data_task = asyncio.create_task(receive_processed_data())
        mental_health_data_task = asyncio.create_task(receive_mental_health_data())
        emotion_data_task = asyncio.create_task(receive_emotion_data())

        async for request in request_iterator:
            await self.__eeg_service.upload(list(request.data))

        await asyncio.gather(
            processed_data_task, emotion_data_task, mental_health_data_task
        )
