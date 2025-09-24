import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

def setup_logger(log_file=None, log_level=logging.INFO, max_bytes=10485760, backup_count=5):
    """
    初始化日志记录器，将日志按指定格式输出并记录到文件

    Args:
        log_file (str): 日志文件路径，默认为None，会自动生成以当天日期命名的日志文件
        log_level: 日志级别
        max_bytes (int): 单个日志文件最大字节数
        backup_count (int): 保留的备份日志文件数量

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 创建logger
    logger = logging.getLogger('mcsmapi')
    logger.setLevel(log_level)

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 创建logs目录（如果不存在）
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # 如果未指定日志文件名，则使用当天日期命名
    if log_file is None:
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = log_dir / f'{today}.log'

    # 创建格式化器
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s'
    )

    # 创建文件处理器（带轮转）
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # 添加处理器到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger