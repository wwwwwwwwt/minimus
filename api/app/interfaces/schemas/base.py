from gzip import READ
from optparse import Option
from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    """
    基础api相应结构
    """
    code: int # 业务状态码
    message: str = Field(default="success")
    data: Optional[T] = Field(default_factory=dict)

    @staticmethod
    def success(data: Optional[T] = None, msg:str = "success") -> "Response[T]":
        """成功响应"""
        return Response(code=200, message=msg, data=data if data is not None else {})

    
    @staticmethod
    def error(code: int, msg:str = "error", data: Optional[T] = None) -> "Response[T]":
        return Response(code=code, message=msg, data=data if data is not None else {})