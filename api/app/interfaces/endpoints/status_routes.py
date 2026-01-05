from fastapi import APIRouter
import logging
from app.interfaces.schemas.base import Response
from app.application.errors.exceptions import BadRequestError, NotFoundError
from app.infrastructure.storage.redis import get_redis_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/status", tags=["状态模块"])

@router.get(path="/healthz", response_model=Response,
            summary="健康检查",
            description="用于检测系统的运行状态")
async def healthz() -> Response:
    """健康检查"""
    logger.info("健康检查")
    # todo 检查redis postgres 等组件的运行状态
    redis_client = get_redis_client()

    is_alive = await redis_client.is_alive()
    if not is_alive:
        return Response.error(code=500, message="Redis is not alive")


    return Response.success(data={"status": "ok"})

