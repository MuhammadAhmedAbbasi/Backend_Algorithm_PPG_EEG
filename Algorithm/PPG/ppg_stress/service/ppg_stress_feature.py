import pandas as pd
import os
from datetime import datetime

from Algorithm.PPG.common.ppg_feature_processor import generate_valid_feature

def map_age(age):
    if age < 13:
        return [1, 0]
    elif age >= 13:
        return [0, 1] 
    
def map_gender(gender):
    return [1, 0] if gender == 'Female' else [0, 1]


def stress_feature():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files = [(file, os.path.join(script_dir, file)) for file in os.listdir(script_dir)]
    temp_csv_list=[]

    for name, path in files:
        file_date = os.path.splitext(name)[0].split('_')[-1]

        if '.csv' in name:
            temp_csv_list.append((path,file_date))
    model_norm_path, _ = sorted(temp_csv_list, key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"), reverse=True)[0]
    feat_norm_params = pd.read_csv(model_norm_path, index_col= 0)
    features = feat_norm_params.index.to_list()
    return features


def encode_stress(df):
    df_new = df.copy()
    df_new[['age_0', 'age_1']] = df_new['age'].apply(map_age).apply(pd.Series)
    df_new[['gender_0', 'gender_1']] = df_new['gender'].apply(map_gender).apply(pd.Series)
    return df_new.drop(['age', 'gender'], axis=1)


# HRV features calculation
def ppg_stress_feature(X, fs, win_min, age, gender, 
                           augmentation = 1, num_top_samples: int = 5):
    # List of HRV features and other relevant features
    hrv_features_stress = stress_feature()
    # Generate valid features and select relevant columns

    stress_feat = generate_valid_feature(X, fs, win_min, augmentation, 
                                             num_top_samples)[hrv_features_stress]
    stress_feat['age'] = age
    stress_feat['gender'] = gender
    
    # Encode features
    stress_feat = encode_stress(stress_feat)
    
    return stress_feat