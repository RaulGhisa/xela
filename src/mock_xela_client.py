import asyncio
import json
import logging
import threading
import time
from websocket_server import WebSocketServer
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


if __name__ == '__main__':
    # async def start_websocket_server():
    #     server_instance, server = await WebSocketServer.create_and_start()

    #     try:
    #         # Keep the server running until interrupted
    #         await server.wait_closed()
    #     except KeyboardInterrupt:
    #         server_instance.logger.info("Server shutting down")

    # ws_server = threading.Thread(target=lambda: asyncio.run(start_websocket_server()), name='ws_server')
    # ws_server.start()

    mock_xela = MockXelaClient()
    mock_xela.start()

    while not mock_xela.is_ready():
        time.sleep(0.01)

    mock_xela.start_data_collection()

    time.sleep(1)

    mock_xela.stop_data_collection()

    data = mock_xela.get_data()

    mock_xela.stop_and_clean_up()

    while not mock_xela.is_stopped():
        time.sleep(0.01)

    pass
