from Algorithm.EEG.eeg_anxiety.service import eeg_anxiety_model
from Algorithm.EEG.eeg_depression.service import eeg_depression_model
from Algorithm.EEG.eeg_fatigue.service import eeg_fatigue_model
from Algorithm.EEG.eeg_stress.service import eeg_stress_model
from Algorithm.EEG.eeg_vitality.service import eeg_vitality_model
from .data_check_condition import FFTValueChecker

model = eeg_depression_model.eeg_depression_model()
model_anxiety = eeg_anxiety_model.eeg_anxiety_model()
model_fatigue = eeg_fatigue_model.eeg_fatigue_model()
model_stress = eeg_stress_model.eeg_stress_model()
model_vitality = eeg_vitality_model.eeg_vitality_model()
value_checker = FFTValueChecker()


# 给定fp1_data以及fp2_data, 计算得到用户是否为抑郁症患者
def eeg_depression(fp1_data: list, fp2_data: list) -> int:
    """
    Given FP1 and FP2 dual-channel EEG data, return whether the user is a depression patient.

    Parameters:
    fp1_data (list<float>): FP1 channel data.
    fp2_data (list<float>): FP2 channel data.

    Returns:
    int: -1 if data is unavailable, int: 0 if normal, int: 1 if suffering from depression
    """
    if not value_checker.check_data_conditions(fp1_data, fp2_data):
        return -1
    return 1 if model.predict(fp1_data, fp2_data) else 0


def eeg_anxiety(fp1_data: list, fp2_data: list) -> int:
    """
    Given FP1 and FP2 dual-channel EEG data, return whether the user is suffering from anxiety.

    Parameters:
    fp1_data (list<float>): FP1 channel data.
    fp2_data (list<float>): FP2 channel data.

    Returns:
    int: -1 if data is unavailable, int: 0 if normal, 1 if suffering from anxiety.
    """
    if not value_checker.check_data_conditions(fp1_data, fp2_data):
        return -1
    return int(model_anxiety.predict(fp1_data, fp2_data))


def eeg_fatigue(fp1_data: list, fp2_data: list) -> int:
    """
    Given FP1 and FP2 dual-channel EEG data, return whether the user is suffering from fatigue.

    Parameters:
    fp1_data (list<float>): FP1 channel data.
    fp2_data (list<float>): FP2 channel data.

    Returns:
    int: -1 if data is unavailable, int: 0 if normal, 1 if person is highly fatigue.
    """
    if not value_checker.check_data_conditions(fp1_data, fp2_data):
        return -1
    return int(model_fatigue.predict(fp1_data, fp2_data))


def eeg_stress(fp1_data: list, fp2_data: list) -> int:
    """
    Given FP1 and FP2 dual-channel EEG data, return whether the user is suffering from stress.

    Parameters:
    fp1_data (list<float>): FP1 channel data.
    fp2_data (list<float>): FP2 channel data.

    Returns:
    int: -1 if data is unavailable, int: 0 if normal, 1 if suffering from stress.
    """
    if not value_checker.check_data_conditions(fp1_data, fp2_data):
        return -1
    return int(model_stress.predict(fp1_data, fp2_data))

def eeg_vitality(fp1_data: list, fp2_data: list) -> int:
    """
    Given FP1 and FP2 dual-channel EEG data, return whether the user is suffering from vitality.

    Parameters:
    fp1_data (list<float>): FP1 channel data.
    fp2_data (list<float>): FP2 channel data.

    Returns:
    int: -1 if data is unavailable, int: 0 if normal, 1 if suffering from vitality.
    """
    if not value_checker.check_data_conditions(fp1_data, fp2_data):
        return -1
    return int(model_vitality.predict(fp1_data, fp2_data))
