#!/usr/bin/env python3

import asyncio
import time
import websockets
import logging
import json
from datetime import datetime

import utils.data_generator as data_generator


DATA_FILE_PATH = r'resources/all_grid_run__20250221T114712.json'


class WebSocketServer:
    def __init__(self, host="localhost", port=8765):
        """Initialize the WebSocket server with the given host and port."""
        self.host = host
        self.port = port
        self.connected_clients = set()
        self.client_counter = 0
        self._start_sending_data = False
        self.logger = logging.getLogger('websocket_server')

        # self._data: list = self._get_data_from_json()
        self._data: list = data_generator.get_mock_data()

    # def _get_data_from_json(self):
    #     with open(DATA_FILE_PATH) as file:
    #         data = json.load(file)

    #     return data

    def _get_next_msg_to_send(self):
        if len(self._data) == 0:
            self._data = data_generator.get_mock_data()
        return self._data.pop(0)

    async def handle_client(self, websocket):
        """Handle a client connection."""
        self.client_counter += 1
        client_id = f"client_{self.client_counter}"

        # Add client to the set of connected clients
        self.connected_clients.add(websocket)
        self.logger.info(f"New client connected: {client_id} (Total: {len(self.connected_clients)})")

        try:
            # Process messages
            async for message in websocket:
                self.logger.info(f"Received message from {client_id}: {message}")

                try:
                    # Parse the message as JSON
                    data = json.loads(message)

                    # Handle the message based on its type
                    await self.process_message(websocket, client_id, data)

                except json.JSONDecodeError:
                    # Handle plain text messages with simple echo
                    await websocket.send(json.dumps({
                        "type": "echo_response",
                        "original_message": message,
                        "timestamp": datetime.now().isoformat()
                    }))

        except websockets.exceptions.ConnectionClosed as e:
            self.logger.info(f"Connection closed for {client_id}: {e}")

        finally:
            # Remove client from set of connected clients
            self.connected_clients.remove(websocket)
            self.logger.info(f"Client {client_id} disconnected (Total: {len(self.connected_clients)})")

    async def process_message(self, websocket, client_id, data):
        """Process a message based on its type."""
        message_type = data.get("type", "")

        if message_type == "start":
            # start dumping the real collected data
            self._start_sending_data = True
            while self._start_sending_data:
                try:
                    await websocket.send(json.dumps(
                        self._get_next_msg_to_send()
                    ))
                    time.sleep(1/133)
                except IndexError:
                    self._start_sending_data = False
                    return

        elif message_type == "stop":
            self._start_sending_data = False

        else:
            await websocket.send(json.dumps({
                "type": "error",
                "message": f"Unknown request type: {message_type}",
                "timestamp": datetime.now().isoformat()
            }))

    async def start(self):
        """Start the WebSocket server."""
        server = await websockets.serve(self.handle_client, self.host, self.port)
        self.logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")

        # Keep the server running
        return server

    @classmethod
    async def create_and_start(cls, host="localhost", port=8765):
        """Factory method to create and start a server in one step."""
        server_instance = cls(host, port)
        server = await server_instance.start()
        return server_instance, server


# Example usage
async def main():
    server_instance, server = await WebSocketServer.create_and_start()

    try:
        # Keep the server running until interrupted
        await server.wait_closed()
    except KeyboardInterrupt:
        server_instance.logger.info("Server shutting down")


if __name__ == "__main__":
    asyncio.run(main())
