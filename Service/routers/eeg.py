import logging
from typing import Dict, List, Optional

from dependencies import get_logger
from entity.mental_health import (
    EegStartRequest,
    EegStartResponse,
    EegStopRequest,
    EegUploadRequest,
)
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from service.eeg import BaseEegService, EegServiceFactory, eeg_anxiety, eeg_depression, eeg_stress, eeg_vitality

from .api_result import ApiResult

router = APIRouter(
    prefix="/eeg",
    tags=["eeg"],
)


class DepressionParam(BaseModel):
    """
    DepressionParam
    """

    fp1: List[float] = []
    fp2: List[float] = []


service_manager: Dict[str, BaseEegService] = {}


def generate_session_id():
    return "e022b518-848a-4839-b0dd-b4b3e86e07ed"
    # return str(uuid.uuid4())


def get_service(
    session_id: Optional[str] = None, logger: logging.Logger = Depends(get_logger)
) -> BaseEegService:
    return EegServiceFactory.create()


@router.post("/depression")
async def depression(depression_param: DepressionParam) -> ApiResult[int]:
    try:
        eeg_fp1_datas = depression_param.fp1
        eeg_fp2_datas = depression_param.fp2
        res = eeg_depression(eeg_fp1_datas, eeg_fp2_datas)

        return ApiResult.Success(res)
    except Exception as e:
        return ApiResult.Error(str(e))
    
@router.post("/anxiety")
async def anxiety(depression_param: DepressionParam) -> ApiResult[int]:
    try:
        eeg_fp1_datas = depression_param.fp1
        eeg_fp2_datas = depression_param.fp2
        res = eeg_anxiety(eeg_fp1_datas, eeg_fp2_datas)

        return ApiResult.Success(res)
    except Exception as e:
        return ApiResult.Error(str(e))

@router.post("/stress")
async def depression(depression_param: DepressionParam) -> ApiResult[int]:
    try:
        eeg_fp1_datas = depression_param.fp1
        eeg_fp2_datas = depression_param.fp2
        res = eeg_stress(eeg_fp1_datas, eeg_fp2_datas)

        return ApiResult.Success(res)
    except Exception as e:
        return ApiResult.Error(str(e))
    
@router.post("/vitality")
async def anxiety(depression_param: DepressionParam) -> ApiResult[int]:
    try:
        eeg_fp1_datas = depression_param.fp1
        eeg_fp2_datas = depression_param.fp2
        res = eeg_vitality(eeg_fp1_datas, eeg_fp2_datas)

        return ApiResult.Success(res)
    except Exception as e:
        return ApiResult.Error(str(e))


@router.post("/start")
async def start(
    start_req: EegStartRequest, service: BaseEegService = Depends(get_service)
) -> ApiResult:
    try:
        session_id = generate_session_id()
        success = await service.start(start_req.process_data_verbose)
        service_manager[session_id] = service

        if not success:
            return ApiResult.Error("start eeg service failed")

        response = EegStartResponse(session_id=session_id, upload_bytes_size=150 * 3)

        return ApiResult.Success(response)
    except Exception as e:
        return ApiResult.Error(str(e))


@router.post("/stop")
async def stop(stop_req: EegStopRequest) -> ApiResult:
    try:
        service = service_manager.get(stop_req.session_id)
        if service is None:
            return ApiResult.Error("session_id not found")

        await service.stop()
        service_manager.pop(stop_req.session_id)
        return ApiResult.Success()
    except Exception as e:
        return ApiResult.Error(str(e))


@router.post("/upload")
async def upload(upload_req: EegUploadRequest) -> ApiResult:
    try:
        service = service_manager.get(upload_req.session_id)
        if service is None:
            return ApiResult.Error("session_id not found")

        response = await service.calc_mental_health(upload_req.eeg_data)

        return ApiResult.Success(response)
    except Exception as e:
        return ApiResult.Error(str(e))
