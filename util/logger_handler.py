import logging
import os
from datetime import datetime

from util.path_tool import get_asb_path

# 日志保存的根目录
LOG_ROOT = get_asb_path("logs")

# 确保日志目录存在 exist_ok=True: 如果目录存在则不创建
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志的格式
DEFAULT_LOGGING_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s -%(filename)s:%(lineno)d - %(message)s"
)

def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file: str = None
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOGGING_FORMAT)

    logger.addHandler(console_handler)

    # 文件handler
    if not log_file:  # 日志文件存放路径
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
    file_hander = logging.FileHandler(log_file, encoding="utf-8")
    file_hander.setLevel(file_level)
    file_hander.setFormatter(DEFAULT_LOGGING_FORMAT)
    logger.addHandler(file_hander)
    return logger


# 快捷获取日志器
logger = get_logger()

if __name__ == '__main__':
    logger.error("错误信息")
    logger.warning("警告信息")
    logger.info("日志信息")
    logger.debug("调试信息")
