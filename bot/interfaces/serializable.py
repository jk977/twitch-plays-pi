from . import *

class Serializable(ABC):
    '''
    Interface for serializable classes.
    '''
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def serialize(self):
        pass

    @abstractstaticmethod
    def deserialize(serialized):
        pass