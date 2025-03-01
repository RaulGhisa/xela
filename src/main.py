import logging
import signal
import subprocess
import sys
import time
from utils.logger_setup import setup_logger
from xela_driver import XelaDriver

XELA_SERVER_PATH = r'/home/psxrg6/Documents/kits/xela_suite_linux/xela_server'


def start_xela_server(path: str = XELA_SERVER_PATH):
    subprocess.Popen([
        "gnome-terminal",  # Change to your terminal (konsole, xterm, etc.)
        "--",
        "bash",
        "-c",
        f"{path} --ip 172.123.123.123; exec bash"  # The 'exec bash' keeps the terminal open
    ])


def signal_handler(sig, frame, driver: XelaDriver):
    logging.info("\nShutting down gracefully...")
    driver.join()
    sys.exit(0)


if __name__ == '__main__':
    setup_logger()
    xela_driver = XelaDriver(ip='xxxxxxxxxx', port=5000)

    signal.signal(signal.SIGINT, lambda x, y: signal_handler(x, y, xela_driver))  # Ctrl+C
    signal.signal(signal.SIGTERM, lambda x, y: signal_handler(x, y, xela_driver))  # termination request

    start_xela_server()
    time.sleep(5)  # TODO: wait for the serve to broadcast something, do not sleep here

    xela_driver.start()

    while not xela_driver.is_ready():
        time.sleep(0.1)

    signal.pause()
