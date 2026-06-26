import logging
import os
import time
import datetime
from logging.handlers import RotatingFileHandler

from conf import setting

log_path = setting.FILE_PATH["LOG"]

# 自动创建日志目录
os.makedirs(log_path, exist_ok=True)

# Linux/Windows兼容
logfile_name = os.path.join(
    log_path,
    f"test.{time.strftime('%Y%m%d')}.log"
)


class RecordLog:
    """日志模块"""

    def __init__(self):
        self.handle_overdue_log()

    def handle_overdue_log(self):
        """删除30天以前的日志"""

        before_date = (
            datetime.datetime.now()
            - datetime.timedelta(days=30)
        ).timestamp()

        # 日志目录不存在直接返回
        if not os.path.exists(log_path):
            return

        for file in os.listdir(log_path):

            filepath = os.path.join(log_path, file)

            # 跳过目录
            if not os.path.isfile(filepath):
                continue

            try:
                file_create_time = os.path.getctime(filepath)

                if file_create_time < before_date:
                    os.remove(filepath)

            except FileNotFoundError:
                continue

    def output_logging(self):

        logger = logging.getLogger(__name__)

        if not logger.handlers:

            logger.setLevel(setting.LOG_LEVEL)

            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d '
                '-[%(module)s:%(funcName)s] - %(message)s'
            )

            fh = RotatingFileHandler(
                filename=logfile_name,
                mode='a',
                maxBytes=5242880,
                backupCount=7,
                encoding='utf-8'
            )

            fh.setLevel(setting.LOG_LEVEL)
            fh.setFormatter(log_format)

            logger.addHandler(fh)

            sh = logging.StreamHandler()
            sh.setLevel(setting.STREAM_LOG_LEVEL)
            sh.setFormatter(log_format)

            logger.addHandler(sh)

        return logger


apilog = RecordLog()
logs = apilog.output_logging()
