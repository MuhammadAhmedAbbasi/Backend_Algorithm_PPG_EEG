from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class StatusCode(Enum):
    SUCCESS = 0
    ERROR = 1


class ApiResult(BaseModel, Generic[T]):
    code: StatusCode  # 响应码
    message: Optional[str]  # 响应消息
    data: Optional[T] = None  # 响应数据

    @staticmethod
    def Success(data: Optional[T] = None, message: str = "") -> "ApiResult[T]":
        """
        create success response

        Args:
            data (T): response data
            message (str): response message
        """
        result = ApiResult(code=StatusCode.SUCCESS, data=data, message=message)

        return result

    @staticmethod
    def Error(message: str) -> "ApiResult[T]":
        """
        create error response

        Args:
            message (str): response message
        """
        result = ApiResult(code=StatusCode.ERROR, message=message, data=None)

        return result
