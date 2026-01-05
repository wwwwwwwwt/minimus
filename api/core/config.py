from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """应用配置类"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # 环境变量会自动从字段名映射（如 ENV -> ENV）
    ENV: str = Field(default="development", description="运行环境")
    LOG_LEVEL: str = Field(default="INFO", description="日志级别")
    LOG_FILE: str = Field(default="logs/minimus.log", description="日志文件路径")
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/minimus",
        description="数据库连接 URL"
    )
    REDIS_HOST: str = Field(default="localhost", description="Redis 主机地址")
    REDIS_PORT: int = Field(default=6379, description="Redis 端口")
    REDIS_DB: int = Field(default=0, description="Redis 数据库")



# 创建全局配置实例
@lru_cache
def get_settings() -> Settings:
    """获取配置实例"""
    return Settings()

