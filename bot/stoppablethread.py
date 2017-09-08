# TODO use multiprocessing instead of threading

import threading
from time import sleep, time


class StoppableThread(threading.Thread):
    """Thread class that loops the target function until stop() is called."""
    def __init__(self, period=-1, timeout=-1, after=None, **kwargs):
        """
        Initializes class instance.

        :param period: how often to repeat the target function (seconds). Set to less than 0 to not loop
        :param timeout: if loop is True, time to wait before stopping loop (seconds); doesn't timeout if value <= 0
        :param after: function to call after thread finishes (if it takes an argument, self is passed)
        :param kwargs: keywords args for threading.Thread constructor
        :raises TypeError: if parameter has incorrect type
        """
        if after and not callable(after):
            raise TypeError('"after" is not callable')

        self._after = after
        self._stop_event = threading.Event()
        self._period = period
        self._timeout = timeout
        super().__init__(**kwargs)

    def __timeout(self):
        start = time()
        while True:
            if self._timeout <= 0:
                yield False
            else:
                elapsed = time() - start
                yield elapsed >= self._timeout

    def run(self):
        timeout = self.__timeout()
        while not (self._stop_event.is_set() or next(timeout)):
            self._target(*self._args, **self._kwargs)
            if self._period < 0:
                break
            else:
                sleep(self._period)

        if self._after:
            try:
                self._after(self)
            except TypeError:
                self._after()

    def stop(self):
        self._stop_event.set()
