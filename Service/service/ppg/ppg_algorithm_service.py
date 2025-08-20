import os
import numpy as np

from Algorithm.PPG.common.ppg_feature_processor import *
from Algorithm.PPG.common.ppg_model_service import ModelService
from Algorithm.PPG.ppg_anxiety.service.ppg_anxiety_feature import ppg_anxiety_feature
from Algorithm.PPG.ppg_depression.service.ppg_depression_feature import ppg_depression_feature
from Algorithm.PPG.ppg_stress.service.ppg_stress_feature import ppg_stress_feature
from Algorithm.PPG.ppg_vitality.service.ppg_vitality_feature import ppg_vitality_feature
from Algorithm.PPG.ppg_insomnia.service.ppg_insomnia_feature import ppg_insomnia_feature
from Algorithm.PPG.common.ppg_index_calculator import *
from Algorithm.PPG.common.data.hrv_index import HrvIndex
from Algorithm.PPG.common.data.hrv_quality import HrvQuality
from Algorithm.PPG.common.data.psycho_index import PsychoIndex
from Algorithm.PPG.common.data.psycho_chunks_prediction import PsychoChunksPrediction
from dataclasses import fields
from Service.config import *
from scipy.stats import norm

#构建模型
main_path = '../../../'
depression_service = ModelService(service_base = os.path.join(os.path.dirname(os.getcwd()),"Algorithm", "PPG", "ppg_depression", "service"))
anxiety_service = ModelService(service_base = os.path.join(os.path.dirname(os.getcwd()), "Algorithm", "PPG", "ppg_anxiety", "service"))
stress_service = ModelService(service_base = os.path.join(os.path.dirname(os.getcwd()), "Algorithm", "PPG", "ppg_stress", "service"))
vitality_service = ModelService(service_base = os.path.join(os.path.dirname(os.getcwd()), "Algorithm", "PPG", "ppg_vitality", "service"))
insomnia_service = ModelService(service_base = os.path.join(os.path.dirname(os.getcwd()), "Algorithm", "PPG", "ppg_insomnia", "service"))

# This function return depression, axiety, stress and vitality 
def ppg_get_pyschoindex(X:list, fs: int, gender: str, age: int, selected_chunk_time: int = selected_data_testing_time) -> PsychoIndex:
    try:
        sample_length = selected_chunk_time * 60 * fs
        # # Slice the data to get only the first 3 minutes of data
        if len(X) > sample_length:
            X = X[:sample_length]
        # Depression features
        features_depression = ppg_depression_feature(X, fs, depression_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)
        # Anxiety features
        features_anxiety = ppg_anxiety_feature(X, fs, anxiety_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)
        # stress features
        feature_stress = ppg_stress_feature(X, fs, stress_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)
        # vitality features
        feature_vitality = ppg_vitality_feature(X, fs, vitality_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)
        #Insomnia Feature
        feature_insomnia = ppg_insomnia_feature(X, fs, insomnia_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)

        # Predicting Anxiety, Depression, Stress, Vitality
        depression_prediction = depression_service.predict(features_depression)
        anxiety_prediction = anxiety_service.predict(features_anxiety)
        stress_prediction = stress_service.predict(feature_stress)
        vitality_prediction = vitality_service.predict(feature_vitality)
        insomnia_prediction = insomnia_service.predict(feature_insomnia)

        return PsychoIndex(depression_prediction=depression_prediction, anxiety_prediction = anxiety_prediction,
                             stress_prediction = stress_prediction, vitality_prediction = vitality_prediction, insomnia_prediction = insomnia_prediction) 
    except Exception as e:
        return PsychoIndex(depression_prediction=-1, anxiety_prediction = -1,
                             stress_prediction = -1, vitality_prediction = -1, insomnia_prediction = -1) 

# This function is calculating the HRV features
def ppg_get_hrv_index(X: list, fs, selected_chunk_time: int = 1) -> HrvIndex:
    sample_length = selected_chunk_time * 60 * fs
    # # Slice the data to get only the first 3 minutes of data
    if len(X) > sample_length:
        X = X[:sample_length]
    keys = ['HRV_SDNN', 'HRV_RMSSD', 'HRV_pNN50', 'HRV_HF', 'HRV_LF', 'HRV_LFHF']
    features = generate_valid_feature(X, fs, hrv_index_minutes, augmentation_factor, num_best_quality_samples)[keys]
    # Define the keys directly
    return HrvIndex(
        HRV_SDNN = round(np.average(features['HRV_SDNN'].to_numpy()), 4),
        HRV_RMSSD = round(np.average(features['HRV_RMSSD'].to_numpy()), 4),
        HRV_pNN50 = round(np.average(features['HRV_pNN50'].to_numpy()), 4),
        HRV_HF = round(np.average(features['HRV_HF'].to_numpy()), 4),
        HRV_LF = round(np.average(features['HRV_LF'].to_numpy()), 4),
        HRV_LFHF = round(np.average(features['HRV_LFHF'].to_numpy()), 4)
    )

# This function is calculating the index based on age 
def ppg_get_hrv_quality(features, age) -> HrvQuality:
    norm_SDNN = get_SDNN(age)
    norm_RMSSD = get_RMSSD(age)
    norm_pNN50 = get_pNN50(age)
    norm_LFHF = get_LFHF(age)
 
    q_SDNN = norm_SDNN.cdf(float(features.HRV_SDNN))
    q_RMSSD = norm_RMSSD.cdf(float(features.HRV_RMSSD))
    q_pNN50 = norm_pNN50.cdf(float(features.HRV_pNN50))
    q_LHF = norm_LFHF.cdf(float(features.HRV_LFHF))
    return HrvQuality(q_SDNN = round(q_SDNN, 4), q_RMSSD = round(q_RMSSD, 4), 
                    q_pNN50 = round(q_pNN50, 4),q_LHF = round(q_LHF, 4) )

def ppg_get_processed_wave(X: list, fs, selected_chunk_time: int = 1):
    sample_length = selected_chunk_time * 60 * fs
    # # Slice the data to get only the first 3 minutes of data
    if len(X) > sample_length:
        X = X[:sample_length]

    return generate_processed_wave(X, fs, wave_divisor, filter_minimum_range, filter_maximum_range)
 


# This function is calculating the subject's each chunk result 
def ppg_get_model_chunk_result(X:list, fs: int, gender: str, age: int, selected_chunk_time: int = 1) -> PsychoChunksPrediction:
    sample_length = selected_chunk_time * 60 * fs
    # # Slice the data to get only the first 3 minutes of data
    if len(X) > sample_length:
        X = X[:sample_length]

    features_depression = ppg_depression_feature(X, fs, depression_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)
    features_anxiety = ppg_anxiety_feature(X, fs, anxiety_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)
    feature_stress = ppg_stress_feature(X, fs, stress_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)
    feature_vitality = ppg_vitality_feature(X, fs, vitality_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)
    feature_insomnia = ppg_insomnia_feature(X, fs, insomnia_window_minutes, age, gender, augmentation_factor, num_best_quality_samples)
    depression_prediction = depression_service.predict_by_chunk(features_depression)
    anxiety_prediction = anxiety_service.predict_by_chunk(features_anxiety)
    stress_prediction = stress_service.predict_by_chunk(feature_stress)
    vitality_prediction = vitality_service.predict_by_chunk(feature_vitality)
    insomnia_prediction = insomnia_service.predict_by_chunk(feature_insomnia)
    return PsychoChunksPrediction(depression = depression_prediction, anxiety = anxiety_prediction,
                                        stress = stress_prediction, vitality = vitality_prediction,
                                        insomnia = insomnia_prediction)
