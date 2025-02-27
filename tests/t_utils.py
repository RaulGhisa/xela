import os
import subprocess


def start_websocket_server():
    subprocess.Popen(["python", os.path.abspath('./src/websocket_server.py')])


if __name__ == '__main__':
    start_websocket_server()
