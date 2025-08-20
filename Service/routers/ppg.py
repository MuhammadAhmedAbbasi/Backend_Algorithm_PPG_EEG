from fastapi import APIRouter
from service.ppg.ppg_algorithm_service import *
from .api_result import ApiResult
from Service.config import *

from Service.common.data.ppg_parameters import PPGParams
from Service.common.data.ppg_hrv_index_result import PPGHrvIndexResult
from Service.common.data.ppg_pyscho_result import ppg_pyscho_result
from Service.common.data.ppg_pyscho_chunk import PPGChunkPredictResult
from Service.common.data.ppg_wave_result import PPGWaveResult
from fastapi import APIRouter

router = APIRouter(
    prefix = "/ppg",
    tags = ["ppg"],
)

@router.post("/pyscho-index")
async def get_pyscho_index(ppg_param: PPGParams):
    try:
        # Extract parameters from the request body
        X = ppg_param.datas
        fs = ppg_param.freq
        gender = ppg_param.sex
        age = ppg_param.age
        
        # Check if the input data length meets the minimum required duration
        if len(X) >= (sampling_frequency * data_minimum_minutes_threshold * 60):
            # Perform prediction
            prediction_results = ppg_get_pyschoindex(X, fs, gender, age)
            # Extract predictions
            depression_prediction = prediction_results.depression_prediction
            anxiety_prediction = prediction_results.anxiety_prediction
            stress_prediction = prediction_results.stress_prediction
            vitality_prediction = prediction_results.vitality_prediction
            insomnia_service = prediction_results.insomnia_prediction

            
            # Create the result object
            result = ppg_pyscho_result(
                depression = depression_prediction,
                anxiety = anxiety_prediction,
                stress = stress_prediction,
                vitality = vitality_prediction
                #insomnia = insomnia_service
            )
            
            return ApiResult.Success(result)
        else:
            raise ValueError("The input data length is insufficient.")
    
    except ValueError as ve:
        # Handle specific ValueError exceptions
        return ApiResult.Error(str(ve))
    except Exception as e:
        # Handle general exceptions
        return ApiResult.Error(f"An error occurred: {str(e)}")

@router.post("/hrv-index")
async def get_hrv_index(ppg_param: PPGParams):
    try:
        X = ppg_param.datas
        fs = ppg_param.freq
        feature_calculation = ppg_get_hrv_index(X, fs)
        hrv_quality = ppg_get_hrv_quality(feature_calculation,12)

        reslut = PPGHrvIndexResult(
            hrv_index = feature_calculation,
            hrv_quality = hrv_quality
        )
        return ApiResult.Success(reslut)
    except Exception as e:
        return ApiResult.Error(str(e))

@router.post("/wave")
async def get_wave(ppg_param: PPGParams):
    try:
        raw_wave = ppg_param.datas
        fs = ppg_param.freq
        processed_wave, wave_quality= ppg_get_processed_wave(raw_wave, fs)

        reslut = PPGWaveResult(
            raw_wave = raw_wave,
            processed_wave = processed_wave
            #wave_quality = wave_quality
        )

        return ApiResult.Success(reslut)
    except Exception as e:
        return ApiResult.Error(str(e))

@router.post("/analysis")
async def get_pyscho_index(ppg_param: PPGParams):
    try:
        X = ppg_param.datas
        fs = ppg_param.freq
        gender = ppg_param.sex
        age = ppg_param.age

        
        prediction_results = ppg_get_model_chunk_result(X, fs, gender, age)
        depression_prediction = prediction_results.depression
        anxiety_prediction = prediction_results.anxiety
        stress_prediction = prediction_results.stress
        vitality_prediction = prediction_results.vitality
        insomnia_prediction = prediction_results.insomnia
        
        reslut = PPGChunkPredictResult(
            depression = depression_prediction,
            anxiety = anxiety_prediction,
            stress = stress_prediction,
            vitality = vitality_prediction
            #insomnia = insomnia_prediction
             )
        

        return ApiResult.Success(reslut)
    except Exception as e:
        return ApiResult.Error(str(e))