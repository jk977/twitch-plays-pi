from interfaces.chat import Chat

class DummyChat(Chat):
    '''
    Dummy class for use in unit testing.
    '''
    def __init__(self):
        self.message = 'Hello, world!'

    def send_message(self, message):
        return message

    def get_message(self):
        return self.message

    def close(self):
        return True