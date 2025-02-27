import copy
import enum
import json
import threading
import logging
import time
import websocket


websocket.setdefaulttimeout(1)  # you should avoid increasing it.


class XelaClientState(enum.Enum):
    NOT_CONNECTED = 'not connected'
    CONNECTED = 'connected'
    COLLECTING_DATA = 'collecting data'
    STOPPED = 'stopped'
    CLOSED = 'closed'

    def is_ready(self):
        return self == self.CONNECTED

    def is_stopped(self):
        return self == self.STOPPED

    def is_collecting_data(self):
        return self == self.COLLECTING_DATA


class XelaClient:
    TIME_TO_WAIT_AFTER_ERROR = 3
    TIME_TO_WAIT_AFTER_SUCCESS = 0.1
    TIME_TO_WAIT_WHILE_DEVICE_NOT_SUPPOSED_TO_OPEN = 1

    def __init__(self, ip: str, port: int = 5000):
        self._name: str = 'xelaclient'
        self._ip: str = ip
        self._port: int = port

        self._access_lock = threading.RLock()
        self._thread = threading.Thread(target=self._run, name=self._name, daemon=True)
        self._stop_event = threading.Event()
        self._start_data_collection_event = threading.Event()

        self._websocket_app: websocket.WebSocketApp = None
        self._websocket_thread: threading.Thread = None  # set up WebSockets

        self._messages: list = []

        self._state: XelaClientState = XelaClientState.CLOSED

        self._sleep_time_before_next_perform = self.TIME_TO_WAIT_AFTER_SUCCESS

    def _run(self):
        while not self._stop_event.is_set():
            try:
                match self._state:
                    case XelaClientState.CLOSED:
                        self._change_state(XelaClientState.NOT_CONNECTED)

                    case XelaClientState.NOT_CONNECTED:
                        try:
                            self._websocket_app = websocket.WebSocketApp("ws://{}:{}".format(self._ip, self._port), on_message=self._on_ws_message)
                            self._websocket_thread = threading.Thread(target=self._websocket_app.run_forever, name='websocketapp')
                            self._websocket_thread.start()
                            while not self._websocket_thread.is_alive():
                                time.sleep(0.01)

                            self._change_state(XelaClientState.CONNECTED)
                            self._sleep_time_before_next_perform = self.TIME_TO_WAIT_AFTER_SUCCESS

                        except Exception:
                            logging.exception('Failed to create the websocket, retrying...')
                            self._sleep_time_before_next_perform = self.TIME_TO_WAIT_AFTER_ERROR

                    case XelaClientState.CONNECTED:  # connected and not collecting data
                        if self._start_data_collection_event.is_set():
                            self._messages = []
                            self._change_state(XelaClientState.COLLECTING_DATA)

                    case XelaClientState.COLLECTING_DATA:  # connected and collecting data
                        if not self._start_data_collection_event.is_set():
                            self._change_state(XelaClientState.CONNECTED)

                    case XelaClientState.STOPPED:
                        pass

            except Exception:
                logging.exception(f'Unhandled exception in "{self._name}" loop!')

            if self._sleep_time_before_next_perform > 0:
                self._stop_event.wait(self._sleep_time_before_next_perform)  # wait instead of sleep to be able to stop the thread
        try:
            self._clean_up()
        except Exception:
            logging.exception(f'Failed to clean-up device "{self._name}"!')

    def _clean_up(self):
        if self._websocket_thread is not None:
            logging.info('Cleaning up the websocket app...')
            self._websocket_app.close()
            logging.info('Joining the websocket thread...')
            self._websocket_thread.join()
            self._websocket_thread = None
            self._websocket_app = None

        self._messages = []
        self._change_state(XelaClientState.STOPPED)

    def _change_state(self, state: XelaClientState):
        self._state = state

    def _on_ws_message(self, _, msg: str):
        if self._state == XelaClientState.COLLECTING_DATA:
            data = json.loads(msg)  # less time on lock if JSON parsing here
            with self._access_lock:
                self._messages.append(data)
        else:
            pass  # do not save anything if not in data collection state

    def start(self):
        logging.info(f'Starting "{self._name}"...')
        self._stop_event.clear()
        self._thread.start()

    def is_ready(self):
        return self._state.is_ready()

    def is_stopped(self):
        return self._state.is_stopped()

    def stop_and_clean_up(self):
        self._stop_event.set()

    def join(self):
        self.stop_and_clean_up()
        logging.info(f'Waiting for "{self._name}" thread to stop...')
        self._thread.join()
        logging.info(f'"{self._name}" thread stopped.')

    def start_data_collection(self):
        logging.info('Starting data collection...')
        if self._state.is_ready():
            self._start_data_collection_event.set()
        else:
            logging.error('Cannot start data collection, XELA sensor is not connected.')

    def stop_data_collection(self):
        logging.info('Stopped data collection...')
        if self._state.is_collecting_data():
            self._start_data_collection_event.clear()
        else:
            logging.error('Cannot stop data collection, data is not being collected.')

    def get_data(self):
        return copy.deepcopy(self._messages)
