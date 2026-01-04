from fastapi import APIRouter
from .status_routes import router as status_routes

def create_api_router() -> APIRouter:
    """创建API总路由, 涵盖所有API路由"""
    router = APIRouter()
    router.include_router(status_routes)
    return router

routers = create_api_router()