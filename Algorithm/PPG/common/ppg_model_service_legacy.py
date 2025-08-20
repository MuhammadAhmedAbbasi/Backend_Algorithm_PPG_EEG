import numpy as np
import os
import onnxruntime as ort
import pandas as pd

from datetime import datetime
from numpy import float32

'''
## fix：2024-5-24 11:25:59
    - 模型自动加载最新日期

'''
class ModelService_legacy:
    win_minutes = 1
    win_augment = 1
    def __init__(self, service_base) -> None:
        self.service_base = service_base
        self.initialize()
        
    def predict(self, Input:np.ndarray):
        '''
        预测函数, 返回0和1表示二分类结果
        '''
        Input = self.feat_selection_normalize(Input)
        predict_batches = []
        for i in range(Input.shape[0]):
            line = Input[i,:].reshape(1, -1).astype(float32)
            input_name = self.ort_session.get_inputs()[0].name
            inputs = {input_name: line}
            model_predict = self.ort_session.run(None, inputs)[0]
            predict_batches.append(model_predict)
        predictions_array = np.array(predict_batches)
        predictions_avg = np.mean(predictions_array, axis=0)
        predicted_classes = np.argmax(predictions_avg)
        return int(predicted_classes)

    def predict_by_chunk(self, Input:np.ndarray):
        '''
        预测函数, 返回0和1表示二分类结果
        '''
        Input = self.feat_selection_normalize(Input)
        predict_batches = []
        for i in range(Input.shape[0]):
            line = Input[i,:].reshape(1, -1).astype(float32)
            input_name = self.ort_session.get_inputs()[0].name
            inputs = {input_name: line}
            model_predict = self.ort_session.run(None, inputs)[0]
            predict_batches.append(model_predict)
        return [int(np.argmax(i)) for i in predict_batches] #注意，这里虽然是二分类，但是为了前端显示（0无2有）因此修改为2

    
    def initialize(self):
        files = os.listdir(self.service_base)

        onnx_files = [file for file in files if file.endswith('.onnx')]
        if onnx_files:
            onnx_files.sort()
            model_onnx_path = os.path.join(self.service_base, onnx_files[-1])
        else:
            model_onnx_path = None

        csv_files = [file for file in files if file.endswith('.csv')]
        if csv_files:
            csv_files.sort()
            model_norm_path = os.path.join(self.service_base, csv_files[-1])
        else:
            model_norm_path = None
        #加载归一化参数
        self.feat_norm_params = pd.read_csv(model_norm_path)
        #加载模型
        self.ort_session = ort.InferenceSession(model_onnx_path, providers = ['CPUExecutionProvider'])

    def feat_selection(self):
        return self.feat_norm_params.columns
    
    def feat_selection_normalize(self, X:pd.DataFrame):
        X_normlized = X.loc[:, self.feat_selection()]
        #输入：特征
        for col in X_normlized.columns:
            u, s = self.feat_norm_params[col]
            X_normlized.loc[:, col] =  X_normlized[col].apply(lambda x:(x - u) / s)

        return X_normlized.values

    @staticmethod
    def get_window_info():
        return ModelService_legacy.win_minutes, ModelService_legacy.win_augment

    @staticmethod
    def set_window_info(win_minutes, win_augment):
        ModelService_legacy.win_minutes = win_minutes
        ModelService_legacy.win_augment = win_augment

