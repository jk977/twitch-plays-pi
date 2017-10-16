from interfaces.serializable import Serializable

class Validator(Serializable):
    '''
    Base class for serializable classes that can validate inputs by attempting to deserialize them.
    '''
    @classmethod
    def validate(cls, message):
        try:
            cls.deserialize(message)
            return True
        except:
            return False