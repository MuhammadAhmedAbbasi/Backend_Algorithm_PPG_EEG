import os
import sys
import json
from redis import Redis

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取项目根目录的路径
project_root = os.path.dirname(os.path.dirname(current_file_path))
# 将项目根目录添加到搜索路径中
sys.path.append(project_root)
# Load configuration from JSON file
config_file = os.path.join(project_root, 'Service', 'config.json')

with open(config_file, 'r') as file:
    config_data = json.load(file)

# Extract settings from the loaded config data
model_input_minutes = config_data['model_input_minutes']  # Dictionary containing feature-related configurations
sample_augmentation = config_data['sample_augmentation']  # Dictionary containing augmentation settings
sampling = config_data['sampling']  # Dictionary containing sampling settings
settings = config_data["settings"]
wave_plot = config_data["wave_plot_setting"]

# Assign to variables with names used in other parts of the code
depression_window_minutes = model_input_minutes['depression_window_minutes']  # Window size for depression sample analysis
anxiety_window_minutes = model_input_minutes['anxiety_window_minutes']  # Window size for anxiety sample analysis
stress_window_minutes = model_input_minutes['stress_window_minutes']  # Window size for stress sample analysis
vitality_window_minutes = model_input_minutes['vitality_window_minutes']  # Window size for vitality sample analysis
insomnia_window_minutes  = model_input_minutes['insomnia_window_minutes']  # Window size for Insomnia sample analysis
hrv_index_minutes = model_input_minutes['hrv_index_minutes']  # window size for hrv features calculation

augmentation_factor = sample_augmentation['augmentation_factor']  # Factor for data augmentation, controlling the generation of synthetic samples
num_best_quality_samples = sample_augmentation['num_best_quality_samples']  # Number of top-quality samples to retain after quality assessment

selected_data_testing_time = settings['selected_data_testing_time'] # Time to select the data for testing of problem

sampling_frequency = sampling['sampling_frequency']  # Sampling frequency of the PPG data in Hertz (Hz)
data_minimum_minutes_threshold = sampling['data_minimum_minutes_threshold']  # Minimum required duration of the PPG data for processing; raises exception if data is below this threshold

wave_divisor = wave_plot["normalization_divisor"]
filter_minimum_range = wave_plot["filter_minimum_range"]
filter_maximum_range = wave_plot["filter_maximum_range"]