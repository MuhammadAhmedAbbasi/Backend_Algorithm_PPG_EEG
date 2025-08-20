import asyncio
from typing import AsyncGenerator, Dict, List, Optional
from typing import AsyncGenerator, Dict, List, Optional

from affectivecloud import ACClient
from affectivecloud.algorithm import AffectiveServices, BaseServices
from affectivecloud.protocols import (
    AffectiveServiceResponse,
    BaseServiceResponse,
    Services,
    SessionResponse,
)
from entity.mental_health.base import (
    EmotionResult,
    EmotionType,
    MentalHealthResult,
    MentalHealthType,
)
from entity.mental_health.eeg_response import EegProcessedData, EegUploadResponse
from pydantic import BaseModel

from .base_eeg_service import BaseEegService
from .eeg_algorithm_service import eeg_anxiety, eeg_depression, eeg_fatigue, eeg_stress, eeg_vitality
from .eeg_mental_health_service import EegMentalHealthService

API_URL: str = "wss://server.affectivecloud.cn/ws/algorithm/v2/"
APP_KEY: str = "3cf9ebb4-f8a4-11ee-9959-2e1d0f5ea2bb"
APP_SECRET: str = "4c333b8e11bcccd7a7ad9ff2f6efa2ff"
CLIENT_ID: str = "679ea2014211cbae584baa0be54f0433"

emotion_mappping: Dict[str, EmotionType] = {
    AffectiveServices.ATTENTION: EmotionType.ATTENTION,
    AffectiveServices.RELAXATION: EmotionType.RELAX,
    AffectiveServices.PRESSURE: EmotionType.STRESS,
    AffectiveServices.PLEASURE: EmotionType.ENJOYMENT,
}


class EntertechEegWaveData(BaseModel):
    eegl_wave: List[float] = []
    eegr_wave: List[float] = []
    eeg_alpha_power: float = 0.0
    eeg_beta_power: float = 0.0
    eeg_theta_power: float = 0.0
    eeg_delta_power: float = 0.0
    eeg_gamma_power: float = 0.0

    eegl_alpha_power: Optional[float] = 0.0
    eegl_beta_power: Optional[float] = 0.0
    eegl_theta_power: Optional[float] = 0.0
    eegl_delta_power: Optional[float] = 0.0
    eegl_gamma_power: Optional[float] = 0.0
    eegr_alpha_power: Optional[float] = 0.0
    eegr_beta_power: Optional[float] = 0.0
    eegr_theta_power: Optional[float] = 0.0
    eegr_delta_power: Optional[float] = 0.0
    eegr_gamma_power: Optional[float] = 0.0
    eeg_quality: int = 0


class AffectiveData:
    attention: Optional[float] = None  # 注意力值，数值越高代表注意力越高
    attention_chd: Optional[float] = None  # 儿童注意力值，数值越高代表注意力越高
    relaxation: Optional[float] = None  # 放松度值，数值越高代表放松度越高
    relaxation_chd: Optional[float] = None  # 儿童放松度值，数值越高代表放松度越高
    pressure: Optional[float] = None  # 压力水平值，数值越高代表压力水平越高
    pleasure: Optional[float] = None  # 愉悦度值，数值越高代表情绪愉悦度越高
    arousal: Optional[float] = None  # 激活度值，数值越高代表情绪激活度越高
    coherence: Optional[float] = None  # 和谐度值，数值越高代表越和谐
    sleep_degree: Optional[float] = None  # 睡眠程度，数值越小代表睡得越深
    sleep_state: Optional[int] = None  # 睡眠状态，0 表示未入睡，1 表示已入睡


class EnterTechEegService(BaseEegService):
    __process_data_verbose: bool = False
    __session_futre: asyncio.Future[bool]
    __is_running: bool = False
    __cycle: int = 3
    __cycle_size: int = 50
    __package_size: int = 20

    __upload_seq: int = 0
    __recieve_seq: int = 0

    def __init__(self):
        super().__init__()

        self.__client: ACClient  # affectivecloud client
        self.__depression_service: EegMentalHealthService = EegMentalHealthService(
            upload_freq=250, time_window_size=0.9, calc_method=eeg_depression
        )
        self.__anxiety_service: EegMentalHealthService = EegMentalHealthService(
            upload_freq=250, time_window_size=0.9, calc_method=eeg_anxiety
        )
        self.__fatigue_service: EegMentalHealthService = EegMentalHealthService(
            upload_freq=250, time_window_size=0.9, calc_method=eeg_fatigue
        )
        self.__stress_service: EegMentalHealthService = EegMentalHealthService(
            upload_freq=250, time_window_size=0.9, calc_method=eeg_stress
        )
        self.__vitality_service: EegMentalHealthService = EegMentalHealthService(
            upload_freq=250, time_window_size=0.9, calc_method=eeg_vitality
        )
        self.__eeg_futures: asyncio.Queue[asyncio.Future[EntertechEegWaveData]] = (
            asyncio.Queue()
        )
        self.__subscribe_eeg_queue: asyncio.Queue[EegProcessedData] = asyncio.Queue()
        self.__subscribe_mental_health_queue: asyncio.Queue[MentalHealthResult] = (
            asyncio.Queue()
        )
        self.__subscribe_emotion_queue: asyncio.Queue[EmotionResult] = asyncio.Queue()
        self.__upload_buffer: List[int] = []

    # override
    async def start(self, process_data_verbose: bool) -> bool:
        self.__process_data_verbose = process_data_verbose
        self.__session_futre = asyncio.Future[bool]()
        asyncio.create_task(self.__start_client())
        try:
            success = await asyncio.wait_for(self.__session_futre, timeout=60)
            if success:
                self.__is_running = True
                self.__upload_seq = 0
                self.__recieve_seq = 0

                asyncio.create_task(self.__subscrible_depress())
                asyncio.create_task(self.__subscrible_anxiety())
                asyncio.create_task(self.__subscrible_fatigue())
                asyncio.create_task(self.__subscrible_stress())
                asyncio.create_task(self.__subscrible_vitality())

            return success
        except asyncio.TimeoutError:
            return False

    # override
    async def stop(self) -> bool:
        try:
            await self.__client.close_session()
            self.__client.close()
        finally:
            self.__is_running = False
            return True

    # override
    async def calc_mental_health(self, eeg_data: List[int]) -> EegUploadResponse:

        raise NotImplementedError("calc_mental_health not implemented")

    # override
    async def upload(self, eeg_data: List[int]) -> None:
        try:
            self.__upload_buffer.extend(eeg_data)
            upload_szie = self.__package_size * self.__cycle_size * self.__cycle
            if len(self.__upload_buffer) < upload_szie:
                return

            upload_data = self.__upload_buffer[:upload_szie]
            self.__upload_buffer = self.__upload_buffer[upload_szie:]

            eeg_future = asyncio.Future[EntertechEegWaveData]()
            await self.__eeg_futures.put(eeg_future)

            async def send_eeg_data():
                await self.__client.upload_raw_data_from_device(
                    {
                        BaseServices.EEG: list(upload_data),
                    }
                )
                # solve the problem of the data not being sent
                await self.__client.upload_raw_data_from_device(
                    {
                        BaseServices.EEG: list([1]),
                    }
                )

                self.logger.debug(
                    f"[{self.__upload_seq}] upload eeg data success size: {len(upload_data)}"
                )

                self.__upload_seq += 1

            asyncio.create_task(send_eeg_data())

            async def wait_eeg_data():
                eeg_wave_data = await eeg_future

                if self.__process_data_verbose:
                    # map eeg data to EegProcesssedData
                    processed_data = EegProcessedData()
                    processed_data.eeg_left_wave = eeg_wave_data.eegl_wave
                    processed_data.eeg_right_wave = eeg_wave_data.eegr_wave
                    processed_data.eeg_alpha_power = eeg_wave_data.eeg_alpha_power
                    processed_data.eeg_beta_power = eeg_wave_data.eeg_beta_power
                    processed_data.eeg_theta_power = eeg_wave_data.eeg_theta_power
                    processed_data.eeg_delta_power = eeg_wave_data.eeg_delta_power
                    processed_data.eeg_gamma_power = eeg_wave_data.eeg_gamma_power

                    self.__subscribe_eeg_queue.put_nowait(processed_data)

                # calc mental health
                fp1 = eeg_wave_data.eegl_wave
                fp2 = eeg_wave_data.eegr_wave
                await asyncio.ensure_future(self.__depression_service.upload_data(fp1, fp2))
                await asyncio.ensure_future(self.__anxiety_service.upload_data(fp1, fp2))
                await asyncio.ensure_future(self.__fatigue_service.upload_data(fp1, fp2))
                await asyncio.ensure_future(self.__stress_service.upload_data(fp1, fp2))
                await asyncio.ensure_future(self.__vitality_service.upload_data(fp1, fp2))

            asyncio.ensure_future(wait_eeg_data())

        except Exception as e:
            self.logger.error("upload eeg data error: " + str(e))

    async def subscrible_processed_data(
        self,
    ) -> AsyncGenerator[EegProcessedData, None]:
        while self.__is_running:
            data = await self.__subscribe_eeg_queue.get()

            yield data

    async def subscribe_mental_health(self) -> AsyncGenerator[MentalHealthResult, None]:
        while self.__is_running:
            data = await self.__subscribe_mental_health_queue.get()

            yield data

    async def subscribe_emotion(self) -> AsyncGenerator[EmotionResult, None]:
        while self.__is_running:
            data = await self.__subscribe_emotion_queue.get()

            yield data

    async def __start_client(self) -> None:
        """
        start affectivecloud client
        """

        async def session_create(data: SessionResponse.Create) -> None:
            # fail to create session
            # if (data.code != 0):
            #     self.session_futre.set_result(False)
            #     return

            self.logger.info("session created. session_id: " + data.session_id)
            await self.__client.init_base_services(services=[BaseServices.EEG])

        async def session_restore(data: SessionResponse.Restore) -> None:
            self.logger.info("session restored")

        async def session_close(data: SessionResponse.Close) -> None:
            self.logger.info("session closed")

        async def base_service_init(data: BaseServiceResponse.Init) -> None:
            self.logger.info("base service initialized")
            await self.__client.subscribe_base_services(services=[BaseServices.EEG])
            await self.__client.start_affective_services(
                services=[
                    AffectiveServices.ATTENTION,
                    AffectiveServices.RELAXATION,
                    AffectiveServices.PRESSURE,
                    AffectiveServices.PLEASURE,
                ]
            )

        async def base_service_subscribe(data: BaseServiceResponse.Subscribe) -> None:
            self.logger.info("base service subscribed")

            if data.response_type is BaseServiceResponse.Subscribe.ResponseType.Status:
                return

            self.logger.debug(f"[{self.__recieve_seq}]recieve eeg data")
            self.__recieve_seq += 1

            if data.data is None:
                self.logger.error(f"base service subscribe error: {data.msg}")
                return

            future = await self.__eeg_futures.get()
            if future is not None:
                eeg_data = EntertechEegWaveData(**data.data[BaseServices.EEG])
                future.set_result(eeg_data)

        async def base_service_report(data: BaseServiceResponse.Unsubscribe) -> None:
            self.logger.info("base service report")

        async def affective_service_start(data: AffectiveServiceResponse.Start) -> None:
            self.logger.info("affective service start")
            await self.__client.subscribe_affective_services(
                services=[
                    AffectiveServices.ATTENTION,
                    AffectiveServices.RELAXATION,
                    AffectiveServices.PRESSURE,
                    AffectiveServices.PLEASURE,
                ]
            )

        async def affective_service_subscribe(
            data: AffectiveServiceResponse.Subscribe,
        ) -> None:
            self.logger.info("affective service subscribe")

            if (
                data.response_type
                is AffectiveServiceResponse.Subscribe.ResponseType.Status
            ):
                self.__session_futre.set_result(True)
                return

            if data.data is None:
                return

            # 根据data的key 获取对应的future
            affective_services = [
                AffectiveServices.ATTENTION,
                AffectiveServices.RELAXATION,
                AffectiveServices.PRESSURE,
                AffectiveServices.PLEASURE,
            ]
            affective_type: Optional[str] = next(
                (service for service in affective_services if service in data.data),
                None,
            )

            if affective_type is None:
                self.logger.error("unknown affective type:" + str(data))
                return

            self.logger.debug(
                "affective type:" + str(affective_type) + ", data:" + str(data.data)
            )

            emotion_type: EmotionType = emotion_mappping[affective_type]

            float_value: float = data.data[affective_type][affective_type]

            if (emotion_type is EmotionType.ATTENTION):
                int_value:int = int(float_value)
                self.logger.info("new attention level: " + str(int_value))

                self.__subscribe_mental_health_queue.put_nowait(MentalHealthResult(
                    type=MentalHealthType.ATTENTION, 
                    value=int_value))
            

            result = EmotionResult(
                type=emotion_type, value=float_value
            )

            self.__subscribe_emotion_queue.put_nowait(result)
            # futrue = await self.__affective_futures[affective_type].get()
            # if (futrue is not None):
            #     value = data.data[affective_type][affective_type]
            #     futrue.set_result(value)

        async def affective_service_report(
            data: AffectiveServiceResponse.Report,
        ) -> None:
            self.logger.info("affective service report")

        async def affective_service_finish(
            data: AffectiveServiceResponse.Finish,
        ) -> None:
            self.logger.info("affective service finish")

        self.__client = ACClient(
            url=API_URL,
            app_key=APP_KEY,
            secret=APP_SECRET,
            client_id=CLIENT_ID,
            upload_cycle=self.__cycle,
            recv_callbacks={
                Services.Type.SESSION: {
                    Services.Operation.Session.CREATE: session_create,
                    Services.Operation.Session.RESTORE: session_restore,
                    Services.Operation.Session.CLOSE: session_close,
                },
                Services.Type.BASE_SERVICE: {
                    Services.Operation.BaseService.INIT: base_service_init,
                    Services.Operation.BaseService.SUBSCRIBE: base_service_subscribe,
                    Services.Operation.BaseService.REPORT: base_service_report,
                },
                Services.Type.AFFECTIVE_SERVICE: {
                    Services.Operation.AffectiveService.START: affective_service_start,
                    Services.Operation.AffectiveService.SUBSCRIBE: affective_service_subscribe,
                    Services.Operation.AffectiveService.REPORT: affective_service_report,
                    Services.Operation.AffectiveService.FINISH: affective_service_finish,
                },
            },  # type: ignore
        )

        self.logger.info("client created")

        try:
            await self.__client.connect()

            async def wait_client_connect():
                while self.__client.ws is None or self.__client.ws.closed:
                    await asyncio.sleep(1)

            await asyncio.wait_for(wait_client_connect(), timeout=10)

            self.logger.info("client connected")
            asyncio.ensure_future(self.__client.create_session())
            success = await self.__session_futre
            if not success:
                return

            while not (self.__client.ws is None or self.__client.ws.closed):
                await asyncio.sleep(10)

            self.logger.info("client closed")
        except asyncio.TimeoutError:
            self.logger.error("client connect timeout")
        except Exception as e:
            self.logger.error("client connect error." + str(e))

    async def __subscrible_depress(self) -> None:
        """
        subscribe depression
        """
        while self.__is_running:
            async for data in self.__depression_service.subricble_result():
                level: int = data
                self.logger.info("drepression level: " + str(level))
                self.__subscribe_mental_health_queue.put_nowait(
                    MentalHealthResult(type=MentalHealthType.DEPRESSION, value=level)
                )

    async def __subscrible_anxiety(self) -> None:
        """
        subscribe anxiety
        """
        while self.__is_running:
            async for data in self.__anxiety_service.subricble_result():
                level:int = data
                self.logger.info("anxiety level: " + str(level))
                self.__subscribe_mental_health_queue.put_nowait(
                    MentalHealthResult(type=MentalHealthType.ANXIETY, value=level)
                )

    async def __subscrible_fatigue(self) -> None:
        """
        subscribe fatigue
        """
        while self.__is_running:
            async for data in self.__fatigue_service.subricble_result():
                level: int = data
                self.logger.info("fatigue level: " + str(level))
                self.__subscribe_mental_health_queue.put_nowait(
                    MentalHealthResult(type=MentalHealthType.FATIGUE, value=level)
                )

    async def __subscrible_stress(self) -> None:
        """
        subscribe stress
        """
        while self.__is_running:
            async for data in self.__stress_service.subricble_result():
                level: int = data
                self.logger.info("stress level: " + str(level))
                self.__subscribe_mental_health_queue.put_nowait(
                    MentalHealthResult(type=MentalHealthType.STRESS, value=level)
                )

    async def __subscrible_vitality(self) -> None:
        """
        subscribe vitality
        """
        while self.__is_running:
            async for data in self.__vitality_service.subricble_result():
                level: int = data
                self.logger.info("viltality level: " + str(level))
                self.__subscribe_mental_health_queue.put_nowait(
                    MentalHealthResult(type=MentalHealthType.VITALITY, value=level)
                )