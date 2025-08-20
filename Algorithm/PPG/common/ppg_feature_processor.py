import neurokit2 as nk
import numpy as np
import pandas as pd
from scipy import fftpack
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="neurokit2")


def hilbert_analysis(X):
    # envelop detecting
    hx = fftpack.hilbert(X)
    hy = np.sqrt(X**2 + hx**2)
    y = (2 * X - hy) / hy * 0.5 + 0.5
    return y


def process_hilbert(X, fs):
    X = nk.ppg_clean(X, sampling_rate=fs)
    Y = hilbert_analysis(X)
    Y = nk.signal_filter(
        Y, sampling_rate=fs, lowcut=1, highcut=4, method="butterworth", order=5
    )
    return Y

def generate_windows(X, fs, win_minutes, win_step) -> list[list, int]:
    """
    创造切片集合
    params：
        X:原始信号
        fs：采样频率
        win_minutes：切分时间，如果赋-1，则不切
    return：
        返回被切分信号的list
    """
    win_size = int(60 * win_minutes * fs)
    step = int(win_size // win_step)
    item = []

    # 低于win_size的1/2抛出异常
    if len(X) <= win_size * 0.5:
        raise Exception(
            f"Too short data length ({len(X)/(fs * 60):.02} minutes) expected >= {win_minutes/2:.02} minutes"
        )
    # 根据不同信号长度，返回窗口集合
    if len(X) <= win_size:
        return [X]
    else:
        n = (len(X) - win_size) // step
        for i in range(n):
            start = i * step
            item.append(X[start : start + win_size])

        # 处理最后一截
        item.append(X[(n - 1) * step :])

        return item

def generate_train_feature(
    subject_id, subject_wave, subject_label,subject_gender, subject_age,fs, win_minutes, augment, if_gender = True
) -> pd.DataFrame:
    subject_wave_processed = process_hilbert(subject_wave, fs)
    win_items = generate_windows(subject_wave_processed, fs, win_minutes, augment)

    dataset = pd.DataFrame()
    for x in win_items:
        ppg_df, info = nk.ppg_process(x, fs)
        peaks = ppg_df["PPG_Peaks"]
        subject_wave_cleaned = nk.ppg_clean(x, sampling_rate=fs)
        wave_quality = np.mean(nk.ppg_quality(subject_wave_cleaned, sampling_rate=125, method="templatematch"))
        wave_quality_df = pd.DataFrame({"wave_quality": [wave_quality]})
        feat = pd.concat([nk.hrv_time(peaks, fs), nk.hrv_frequency(peaks, fs), wave_quality_df], axis=1)
        dataset = pd.concat([dataset, feat]).reset_index(drop=True)

    dataset.fillna(0, inplace=True)
    dataset["label"] = subject_label
    dataset["id"] = subject_id
    if if_gender:
        dataset['age'] = subject_age
        dataset['gender'] = subject_gender
    return dataset

def calc_hrv_features(X, fs):
    X, peaks = nk_process(X, fs)

    hrv_TIME = hrv_time(peaks, fs)
    hrv_FREQ = nk.hrv_frequency(peaks, sampling_rate=fs, show=False, psd_method="welch")
    hrv_NOLINER = hrv_noliner(peaks, fs)



    hrv_feature = pd.concat([hrv_TIME, hrv_FREQ, hrv_NOLINER], axis=1)
    hrv_feature.fillna(0, inplace=True)

    return hrv_feature

def quality_check(window_samples, fs: int = 125, num_top_samples: int = 5):
    if not window_samples:
        # Handle case where there are no samples
        return []

    quality_samples = []
    # Clean and assess quality for each sample
    for sample in window_samples:
        subject_wave_cleaned = nk.ppg_clean(sample, sampling_rate=fs)
        wave_quality = np.mean(nk.ppg_quality(subject_wave_cleaned, sampling_rate=fs, method="templatematch"))
        quality_samples.append(wave_quality)
    
    # Create DataFrame to sort and select top quality samples
    wave_quality_df = pd.DataFrame({"wave_quality": quality_samples})
    wave_quality_df = wave_quality_df.sort_values(by='wave_quality', ascending=False)
    
    # Determine number of top samples to select
    num_samples = len(wave_quality_df)
    
    if num_samples <= num_top_samples:
        # If there are fewer or equal samples than requested, return all samples
        return window_samples
    
    # Select the top N samples based on quality
    wave_quality_df = wave_quality_df.head(num_top_samples)
    
    # Get indices of selected samples and return the corresponding data
    selected_samples_indices = wave_quality_df.index
    selected_data = [window_samples[i] for i in selected_samples_indices]
    
    return selected_data


# Generating the features for depression and stress data
def generate_valid_feature(input_wave, fs: int, win_minutes = 1, augment= 1, num_top_samples: int = 5) -> pd.DataFrame: 
    wave_processed = process_hilbert(input_wave, fs)
    win_items = generate_windows(wave_processed, fs, win_minutes, augment)
    #quality_items = quality_check(win_items,fs,num_top_samples)

    if len(win_items) > num_top_samples:
        win_items = win_items[:num_top_samples] 

    dataset = pd.DataFrame()
    for x in win_items:
        ppg_df, _ = nk.ppg_process(x, fs)
        peaks = ppg_df["PPG_Peaks"]
        feat = pd.concat([nk.hrv_time(peaks, fs), nk.hrv_frequency(peaks, fs)], axis=1)
        dataset = pd.concat([dataset, feat]).reset_index(drop=True)

    dataset.fillna(0, inplace=True)
    return dataset

def generate_processed_wave(X, fs,normalization = 1000000, minimum_range = -1, maximum_range = 1):
    X = [i/normalization for i in X]
    df = pd.Series(X)
    df = nk.ppg_clean(X, fs)
    df, info = nk.ppg_process(X, sampling_rate=fs)
    df = df["PPG_Clean"]
    df = df[df.apply(lambda x: np.isfinite(x) and minimum_range < x <= maximum_range)]
    wave_quality_factor = nk.ppg_quality(df, sampling_rate=fs, method="templatematch")
    return list(df), np.average(wave_quality_factor)

