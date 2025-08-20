import glob
import numpy as np
import os
import onnxruntime as ort

class eeg_depression_model():
    def __init__(self):
        onnx_model_path = self.get_onnxfile()
        self.ort_session = ort.InferenceSession(onnx_model_path)

    # 加载 ONNX 模型
    def get_onnxfile(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        onnx_files = glob.glob(os.path.join(current_dir, '*.onnx'))
        
        # selected latest generated onnx model.
        if onnx_files:
            onnx_files.sort()
            last_onnx_file = onnx_files[-1]
            return last_onnx_file

    # 预测函数
    def predict(self, fp1_list: list, fp2_list: list) -> bool:
        fp1_list = np.abs(np.fft.fft(fp1_list))[0:64].astype(np.float32)
        fp1_list = fp1_list / np.sum(fp1_list)
        fp2_list = np.abs(np.fft.fft(fp2_list))[0:64].astype(np.float32)
        fp2_list = fp2_list / np.sum(fp2_list)
        x = np.concatenate([fp1_list, fp2_list], axis = 0).astype(np.float32).reshape(1, -1)
        
        inputs = {self.ort_session.get_inputs()[0].name: x}
        outputs = self.ort_session.run(None, inputs)
        return (outputs[0] >= 0.5).astype(int)[0]