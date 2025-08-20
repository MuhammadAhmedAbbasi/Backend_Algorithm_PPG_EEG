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

def insomnia_feature():
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


def encode_insomnia(df):
    df_new = df.copy()
    
    # Apply age and gender mapping
    age_encoded = df_new['age'].apply(map_age).apply(pd.Series)
    gender_encoded = df_new['gender'].apply(map_gender).apply(pd.Series)
    
    # Concatenate encoded features and drop original columns
    df_new = pd.concat([df_new, age_encoded, gender_encoded], axis=1)
    df_new = df_new.drop(['age', 'gender'], axis=1)
    
    return df_new


# HRV features calculation
def ppg_insomnia_feature(X, fs, win_min, age, gender, 
                           augmentation = 1, num_top_samples: int = 5):
    # List of HRV features and other relevant features
    hrv_features_insomnia = insomnia_feature()
    # Generate valid features and select relevant columns

    insomnia_feat = generate_valid_feature(X, fs, win_min, augmentation, 
                                             num_top_samples)[hrv_features_insomnia]
    insomnia_feat['age'] = age
    insomnia_feat['gender'] = gender
    
    # Encode features
    insomnia_feat = encode_insomnia(insomnia_feat)
    
    return insomnia_feat