import logging
import time
from xela_client import XelaClient


class MockXelaClient(XelaClient):
    def __init__(self, ip='localhost', port=8765):
        super().__init__(ip, port)

    def start_data_collection(self):
        msg_to_send = '{"type":"start"}'
        logging.info(f'Sending "{msg_to_send}"...')

        # nasty stuff, but you need to wait for the server to start
        while True:
            try:
                self._websocket_app.send(msg_to_send)
                break
            except Exception:
                time.sleep(0.1)
                continue

        super().start_data_collection()
