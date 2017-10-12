from abc import ABC, abstractproperty, abstractmethod, abstractstaticmethod

class BaseInput(ABC):
    @abstractproperty
    def count(self):
        pass

    @abstractproperty
    def content(self):
        pass
    
    @abstractstaticmethod
    def validate():
        pass