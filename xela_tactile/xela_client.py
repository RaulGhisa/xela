import enum
import threading


class XelaClientState(enum.Enum):
    NOT_CONNECTED = 'not connected'
    CONNECTED = 'connected'
    CLOSING = 'closing'
    CLOSED = 'closed'


class XelaClient:
    def __init__(self, ip: str, port: int = 5000):
        self._name = 'xelaclient'
        self._last_msg: dict | None = None
        self._access_lock = threading.RLock()
        self._thread = threading.Thread(target=self._run, name=self._name, daemon=True)
        self._should_stop = threading.Event()
        self._measurements: list = []

    def _run(self):
        while not self._should_stop.is_set():
            try:
                pass
            except Exception:
                log.exception(f'Unhandled exception in {self._name} loop!')
            if self._sleep_time_before_next_perform > 0:
                self._should_stop_event.wait(self._sleep_time_before_next_perform)  # wait instead of sleep to be able to stop the thread
        try:
            self._clean_up()
        except Exception:
            log.exception(f'Failed to clean-up device "{self._name}"!')
