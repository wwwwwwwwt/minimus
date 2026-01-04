from pathlib import Path
from core.config import get_settings
import logging

def set_logging():
    """设置日志配置"""
    settings = get_settings()

    # 获取根日志处理器
    root_logger = logging.getLogger()
   
    # 设置根处理器等级
    log_level = getattr(logging, settings.LOG_LEVEL.upper())
    root_logger.setLevel(log_level)

    # 设置根处理器格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 创建控制台日志
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 创建文件日志（确保目录存在）
    log_file_path = Path(settings.LOG_FILE)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(settings.LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    root_logger.info("日志配置完成，日志等级：%s，日志文件：%s", settings.LOG_LEVEL, settings.LOG_FILE)



def get_logger(name: str):
    """获取日志记录器"""
    return logging.getLogger(name)