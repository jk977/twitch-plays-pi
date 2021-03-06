from . import *

class Serializable(ABC):
    '''
    Interface for serializable classes.
    '''
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def serialize(self):
        pass

    @abstractstaticmethod
    def deserialize(serialized):
        pass