from datetime import datetime
import json
import logging
import os
import signal
import subprocess
import sys
import time
from utils import system_utils
from utils.logger_setup import setup_logger
from xela_driver import XelaDriver

XELA_SERVER_PATH = r'/home/psxrg6/Documents/kits/xela_suite_linux/xela_server'
XELA_VIZ_PATH = r'/home/psxrg6/Documents/kits/xela_suite_linux/xela_viz'
XELA_SERVER_IP = '10.15.131.231'


def start_xela_server(server_path: str = XELA_SERVER_PATH, viz_path: str = XELA_VIZ_PATH):
    system_utils.find_and_kill_process(process_name='xela_server')
    system_utils.find_and_kill_process(process_name='xela_viz')
    subprocess.Popen([
        # "gnome-terminal",
        # "--",
        "bash",
        "-c",
        f"{server_path} --ip {XELA_SERVER_IP} -f {os.path.abspath('./setup_scripts/xServ.ini')}; exec bash"  # The 'exec bash' keeps the terminal open
    ])
    subprocess.Popen([
        # "gnome-terminal",
        # "--",
        "bash",
        "-c",
        f"{viz_path}; exec bash"  # The 'exec bash' keeps the terminal open
    ])


def signal_handler(sig, frame, driver: XelaDriver):
    logging.info("\nShutting down gracefully...")
    driver.join()
    sys.exit(0)


if __name__ == '__main__':
    setup_logger()
    xela_driver = XelaDriver(ip=XELA_SERVER_IP, port=5000)

    signal.signal(signal.SIGINT, lambda x, y: signal_handler(x, y, xela_driver))  # Ctrl+C
    signal.signal(signal.SIGTERM, lambda x, y: signal_handler(x, y, xela_driver))  # termination request

    start_xela_server()
    time.sleep(5)  # TODO: wait for the server to broadcast something, do not sleep here

    xela_driver.start()

    while not xela_driver.is_ready():
        time.sleep(0.1)

    xela_driver.start_data_collection()

    time.sleep(30)

    xela_driver.stop_data_collection()

    xela_data = xela_driver.get_data()
    with open(os.path.abspath(fr'./out/{datetime.now().strftime("%Y%m%dT%H%M%S")}.json'), 'w') as f:
        json.dump(xela_data, f)

    signal.pause()
