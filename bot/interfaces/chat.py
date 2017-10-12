from . import *

class Chat(ABC):
    '''
    Interface for sending and receiving messages.
    '''
    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def get_message(self):
        pass

    @abstractmethod
    def close(self):
        pass