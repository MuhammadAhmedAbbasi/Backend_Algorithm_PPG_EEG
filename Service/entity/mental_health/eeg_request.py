from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class EegStartRequest(BaseModel):
    '''
    eeg命令请求
    
    Properties:
        process_data_verbose (bool): 是否输出数据处理过程的详细信息
    '''
    process_data_verbose: bool  # 是否输出数据处理过程的详细信息

class EegStopRequest(BaseModel):
    '''
    eeg命令请求
        session_id: str  # 会话id
    '''
    session_id: str  # 会话id


class EegUploadRequest(BaseModel):
    '''
    eeg请求
    
    Properties:
        session_id: str  # 会话id
        eeg_data: List[int]  # eeg 原始数据，目前要求长度为150*3
    '''
    session_id: str  # 会话id
    eeg_data: List[int]  # eeg 原始数据，目前要求长度为150*3
    
