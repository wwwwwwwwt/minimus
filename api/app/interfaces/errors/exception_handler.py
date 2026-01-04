from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import logging
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.interfaces.schemas.base import Response
from app.application.errors.exceptions import AppException

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):
    """注册异常处理"""
    
    async def request_validation_error_handler(request: Request, exc: RequestValidationError):
        """请求验证异常处理"""
        logger.error(f"请求验证异常处理: {exc}", exc_info=True)
        return JSONResponse(
            content=Response.error(msg=str(exc.errors()), code=400).model_dump(), 
            status_code=400
        )

    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Starlette HTTP异常处理（包括404等）"""
        logger.error(f"Starlette HTTP异常处理: {exc.status_code} - {exc.detail}", exc_info=True)
        return JSONResponse(
            content=Response.error(msg=str(exc.detail), code=exc.status_code).model_dump(), 
            status_code=exc.status_code
        )

    async def http_exception_handler(request: Request, exc: HTTPException):
        """HTTP异常处理"""
        logger.error(f"HTTP异常处理: {exc}", exc_info=True)
        return JSONResponse(
            content=Response.error(msg=exc.detail, code=exc.status_code).model_dump(), 
            status_code=exc.status_code
        )

    async def app_exception_handler(request: Request, exc: AppException):
        """应用异常处理"""
        logger.error(f"应用异常处理被调用 - 异常类型: {type(exc)}, 消息: {exc.msg}, 状态码: {exc.status_code}", exc_info=True)
        return JSONResponse(
            content=Response.error(msg=exc.msg, code=exc.code).model_dump(), 
            status_code=exc.status_code
        )

    async def exception_handler(request: Request, exc: Exception):
        """异常处理, 捕获所有未注册的异常"""
        logger.error(f"通用异常处理被调用 - 异常类型: {type(exc)}, 异常: {exc}", exc_info=True)
        return JSONResponse(
            content=Response.error(msg="Internal Server Error", code=500).model_dump(), 
            status_code=500
        )

    # 注册异常处理器
    # StarletteHTTPException 会捕获所有 HTTP 错误，包括 404
    app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, exception_handler)
    
    logger.info("异常处理器注册完成")
