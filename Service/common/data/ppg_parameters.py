from pydantic import BaseModel


class PPGParams(BaseModel):
    """
    PpgParam
    """
    datas: list = []
    freq: int = 125
    count: int = 0
    age: int  = 18
    sex: str = "F"
    win: int = 3 
    augment: int = 2  
