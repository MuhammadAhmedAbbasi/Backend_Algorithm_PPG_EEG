import asyncio
import math

from typing import AsyncGenerator, Callable

class EegMentalHealthService:
    __upload_freq: int = 0
    __time_window_size: float = 1.0
    __calc_size: int = 0

    def __init__(
        self,
        upload_freq: int = 250,
        time_window_size: float = 2.0,
        calc_method: Callable[[list, list], int] = lambda x, y: True,
    ):
        """
        service to calculate mental health

        Args:
            upload_freq (int, optional): upload (hz). Defaults to 250 hz.
            time_window_size (float, optional): time window size(s). Defaults to 2.0 s.
            calc_method (Callable[[list, list], bool], optional): _description_. Defaults to lambdax.
        """

        self.__upload_freq = upload_freq
        self.__time_window_size = time_window_size
        self.__calc_method = calc_method
        self.__calc_size = math.floor(self.__upload_freq * self.__time_window_size)

        self.__lock: asyncio.Lock = asyncio.Lock()
        self.__queue: asyncio.Queue[int] = asyncio.Queue()
        self.__fp1_data: list = []
        self.__fp2_data: list = []

        # self.__filter: Filter = FFTDataCheck()

    async def upload_data(self, fp1: list, fp2: list):
        """
        upload data to service
        """
        async with self.__lock:
            self.__fp1_data.extend(fp1)
            self.__fp2_data.extend(fp2)

            calc_size = self.__calc_size

            if len(self.__fp1_data) < calc_size:
                return

            while len(self.__fp1_data) >= calc_size:
                fp1_data = self.__fp1_data[:calc_size]
                fp2_data = self.__fp2_data[:calc_size]

                self.__fp1_data = self.__fp1_data[calc_size:]
                self.__fp2_data = self.__fp2_data[calc_size:]

                await self.calc_mental_health(fp1_data, fp2_data)

    async def calc_mental_health(self, fp1: list, fp2: list):
        """
        calculate mental health
        """
        try:
            result = self.__calc_method(fp1, fp2)
            await self.__queue.put(result)
        except Exception as e:
            print(e)

    async def subricble_result(self) -> AsyncGenerator[int, None]:
        """
        subscribe result
        """
        while True:
            result = await self.__queue.get()
            yield result
