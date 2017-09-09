import threading
from threads.stoppablethread import StoppableThread


class StoppablePool:
    """Collection of stoppable threads."""
    def __init__(self):
        self._threads = []
        self._lock = threading.Lock()

    def start_thread(self, *args, **kwargs):
        """Starts thread, passing all arguments to thread object."""
        with self._lock:
            t = StoppableThread(*args, **kwargs)
            self._threads.append(t)
            t.start()

    def stop_thread(self, name):
        """Stops thread with given name."""
        with self._lock:
            for thread in [t for t in self._threads if t.name == name]:
                thread.stop()

    def stop_all_threads(self):
        with self._lock:
            for thread in self._threads:
                thread.stop()
