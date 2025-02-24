import logging
import logging.handlers
import os
import sys
import traceback

LOG_FILE_PATH = os.path.abspath(os.path.join('logs', 'xela_log'))
LOG_LEVEL = logging.DEBUG


def logger_exception_hook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    exc_info = (exc_type, exc_value, exc_traceback)
    exception_stack_text = "".join(traceback.format_exception(*exc_info, limit=None, chain=True))
    print('# Exception hook::' + '\n' + exception_stack_text)


class CustomLoggerFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\u001b[92m"
    magneta = "\u001b[35m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s.%(msecs)03d [%(levelname)-10s]:  %(message)s  [%(threadName)s] [%(module)s: %(funcName)s]"  # + "{%(name)s}"  # to shwo logger name, to disable it

    FORMATS = {
        logging.DEBUG: magneta + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: bold_red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


def _setup_logger_file(log_file_path: str):
    log_file_dir = os.path.dirname(log_file_path)
    if log_file_dir:
        os.makedirs(log_file_dir, exist_ok=True)

    file_log_formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d [%(levelname)-10s]:  %(message)s  [%(threadName)s] [%(module)s: %(funcName)s] ",
        datefmt="%Y-%m-%d %H:%M:%S")

    need_roll = os.path.isfile(log_file_path)
    file_handler = logging.handlers.RotatingFileHandler(log_file_path, backupCount=100)

    if need_roll:
        file_handler.doRollover()

    file_handler.setFormatter(file_log_formatter)
    file_handler.setLevel(level=LOG_LEVEL)

    logging.getLogger().addHandler(file_handler)


def setup_misc_loggers():
    pass


def setup_logger():
    # NOTE - idk if this is proper way to do, but without it we have duplicate logs in file and console
    if logging.getLogger().hasHandlers():
        logging.getLogger().handlers.clear()

    # main logger needs to accept logs with smallest logLevel processed in handlers
    logging.getLogger().setLevel(LOG_LEVEL)

    _setup_logger_file(LOG_FILE_PATH)

    console_log_formatter = CustomLoggerFormatter(
        "%(asctime)s.%(msecs)03d [%(levelname)-10s]:  %(message)s  [%(threadName)s] [%(module)s: %(funcName)s] ",
        datefmt="%H:%M:%S")
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOG_LEVEL)
    stream_handler.setFormatter(console_log_formatter)
    logging.getLogger().addHandler(stream_handler)

    sys.excepthook = logger_exception_hook

    setup_misc_loggers()
