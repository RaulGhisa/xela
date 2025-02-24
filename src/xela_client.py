import enum
import threading
import logging


class XelaClientState(enum.Enum):
    NOT_CONNECTED = 'not connected'
    CONNECTED = 'connected'
    COLLECTING_DATA = 'collecting data'
    CLOSING = 'closing'
    CLOSED = 'closed'


class XelaClient:
    TIME_TO_WAIT_AFTER_ERROR = 3
    TIME_TO_WAIT_AFTER_SUCCESS = 0.1
    TIME_TO_WAIT_WHILE_DEVICE_NOT_SUPPOSED_TO_OPEN = 1

    def __init__(self, ip: str, port: int = 5000):
        self._name = 'xelaclient'
        self._last_msg: dict | None = None
        self._access_lock = threading.RLock()
        self._thread = threading.Thread(target=self._run, name=self._name, daemon=True)
        self._stop_event = threading.Event()
        self._measurements: list = []
        self._state: XelaClientState = XelaClientState.CLOSED

        self._sleep_time_before_next_perform = 0
        self._sleep_time_to_wait_after_error = 3

    def _run(self):
        while not self._stop_event.is_set():
            try:
                match self._state:
                    case XelaClientState.CLOSED:
                        pass  # idk exactly if I need to do something here
                    case XelaClientState.NOT_CONNECTED:
                        pass
                    case XelaClientState.CONNECTED:
                        pass
                    case XelaClientState.COLLECTING_DATA:
                        pass
                    case XelaClientState.CLOSING:
                        pass
                    case _:
                        raise Exception(f'State "{self._state}" not valid.')
            except Exception:
                logging.exception(f'Unhandled exception in "{self._name}" loop!')
            if self._sleep_time_before_next_perform > 0:
                self._stop_event.wait(self._sleep_time_before_next_perform)  # wait instead of sleep to be able to stop the thread
        try:
            self._clean_up()
        except Exception:
            logging.exception(f'Failed to clean-up device "{self._name}"!')

    def _clean_up(self):
        pass

    def _change_state(self, state: XelaClientState):
        self._state = state

    def start(self):
        logging.info(f'Starting "{self._name}"...')
        self._stop_event.clear()
        self._thread.start()

    def stop_and_clean_up(self):
        self._stop_event.set()

    def join(self):
        self.stop_and_clean_up()
        logging.info(f'Waiting for "{self._name}" thread to stop...')
        self._thread.join()
        logging.info(f'"{self._name}" thread stopped.')
