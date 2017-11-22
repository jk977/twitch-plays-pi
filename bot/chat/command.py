class Command:
    '''
    Represents runnable chat command with stored keyword args.
    '''
    def __init__(self, command, kwargs):
        if not callable(command):
            raise TypeError('Command must be callable.')

        self._command = command
        self._kwargs = kwargs

    def run(self):
        return self._command(**self._kwargs)