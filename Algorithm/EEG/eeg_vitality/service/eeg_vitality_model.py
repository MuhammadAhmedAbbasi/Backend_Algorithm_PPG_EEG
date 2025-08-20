import glob
import numpy as np
import os
import onnxruntime as ort

current_path = os.path.dirname(os.path.abspath(__file__))

# 定义神经网络模型
class eeg_vitality_model():
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

    # Given fp1 and fp2 data, the model predicts
    # Return value: If true, it means fatigue, otherwise it means normal person
    def predict(self, fp1_list: list, fp2_list: list) -> bool:
        fp1_fft = np.abs(np.fft.fft(fp1_list))[0:64].astype(np.float32)
        fp1_fft = fp1_fft / np.sum(fp1_fft)
        fp2_fft = np.abs(np.fft.fft(fp2_list))[0:64].astype(np.float32)
        fp2_fft = fp2_fft / np.sum(fp2_fft)
        x = np.concatenate([fp1_fft, fp2_fft], axis = 0).astype(np.float32).reshape(1, -1)
        
        inputs = {self.ort_session.get_inputs()[0].name: x}
        outputs = self.ort_session.run(None, inputs)
        return (outputs[0] >= 0.5).astype(int)[0]