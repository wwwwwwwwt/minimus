from fastapi import FastAPI
import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from .infrastructure.logging import set_logging
from .interfaces.endpoints.routes import routers
from .interfaces.errors.exception_handler import register_exception_handlers
from .infrastructure.storage.redis import get_redis_client
# 1.加载全局配置
settings = get_settings()

# 2.设置日志配置
set_logging()
logger = logging.getLogger(__name__)
logger.info("Minimus API is starting...")

# 3.定义FastApi路由tag标签
openapi_tags = [
    {
        "name": "状态模块",
        "descripetion" : "包含 **健康检查** 等 API 接口， 用于检测系统的运行状态"
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """异步生命周期上下文管理"""
    logger.info("Minimus API is starting...")

    # todo
    # 8.注册Redis客户端
    redis_client = get_redis_client()
    await redis_client.init()

    try:
        # lifespam节点/分界
        yield
    finally:
        await redis_client.close()
        logger.info("Minimus API is shutting down...")

# 4.创建FastAPI应用实例
app = FastAPI(
    title="Minimus 通用智能体",
    description="A minimal API project",
    lifespan=lifespan,
    openapi_tags=openapi_tags,
    version="0.1.0"
)

# 5.配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 7.注册异常处理
register_exception_handlers(app)

# 6.包含所有API路由
app.include_router(routers, prefix="/api")




@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)