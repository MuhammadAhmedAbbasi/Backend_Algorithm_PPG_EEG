import os
import pandas as pd
from datetime import datetime

from Algorithm.PPG.common.ppg_feature_processor import generate_valid_feature

def map_age(age):
    if age < 13:
        return [1, 0]
    elif age >= 13:
        return [0, 1] 
    
def map_gender(gender):
    return [1, 0] if gender == 'Female' else [0, 1]


def anxiety_feature():
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

# map_gender will be called and extrax columns for age, gender will be dropped
def encode_anxiety(df):
    df_new = df.copy()
    df_new[['age_0', 'age_1']] = df_new['age'].apply(map_age).apply(pd.Series)
    df_new[['gender_0', 'gender_1']] = df_new['gender'].apply(map_gender).apply(pd.Series)
    return df_new.drop(['age', 'gender'], axis=1)

# HRV features, age, gender will be calculated, and also process_anxiety is performed
def ppg_anxiety_feature(X, fs, win_min, age, gender, 
                        augmentation = 1, num_top_sample: int = 5):
    hrv_features_anxiety = anxiety_feature()
    anxiety_feat = generate_valid_feature(X, fs, win_min, augmentation, 
                                             num_top_sample)[hrv_features_anxiety]
    anxiety_feat['age'] = age
    anxiety_feat['gender'] = gender
    anxiety_feat = encode_anxiety(anxiety_feat)
    return anxiety_feat
