from fastapi import APIRouter
import logging
from app.interfaces.schemas.base import Response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/status", tags=["状态模块"])

@router.get(path="/healthz", response_model=Response,
            summary="健康检查",
            description="用于检测系统的运行状态")
async def healthz() -> Response:
    """健康检查"""
    logger.info("健康检查")
    # todo 检查redis postgres 等组件的运行状态
    return Response.success(data={"status": "ok"})