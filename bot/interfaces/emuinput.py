from . import *
from numbers import Number
from interfaces.serializable import Serializable

class EmuInput(Serializable):
    '''
    Base class for nes inputs. Children classes must define functions _validate_content and
    _validate_count to return true when the respective fields are valid, and may optionally
    define a delimiter other than '*'.
    '''
    delimiter = '*'

    @abstractstaticmethod
    def _validate_content(content):
        pass

    @abstractstaticmethod
    def _validate_count(count):
        pass

    def __init__(self, content, count = 1):
        content = str(content)
        count = int(count)

        if not isinstance(count, Number):
            raise TypeError('Expected number, got {} "{}".'.format(type(count).__name__, count))
        
        self._content = content
        self._count = count

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.count == other.count and self.content == other.content

    def serialize(self):
        '''
        Serializes input to send to nes.
        '''
        return self.delimiter.join(str(x) for x in [self.count, self.content])

    @classmethod
    def _parse_content(cls, message):
        '''
        Retrieves content portion of input.
        :param cls: Current class.
        :param message: Message to parse.
        '''
        return message.split(cls.delimiter)[1]

    @classmethod
    def _parse_count(cls, message):
        '''
        Retrieves count portion of input.
        :param cls: Current class.
        :param message: Message to parse.
        :returns: int
        '''
        return int(message.split(cls.delimiter)[0])

    @classmethod
    def deserialize(cls, serialized):
        '''
        Deserializes serialized input.
        :param cls: Current class.
        :param serialized: The serialized input.
        :returns: EmuInput object
        '''
        if not cls.validate(serialized):
            return

        count, content = serialized.split(cls.delimiter)
        count = int(count)
        return cls(content, count)

    @classmethod
    def validate(cls, message):
        '''
        Verifies that an input is properly formatted.
        :param cls: Current class.
        :param message: Message to validate.
        :returns: bool
        '''
        try:
            content = cls._parse_content(message)
            count = cls._parse_count(message)
            return cls._validate_count(count) and cls._validate_content(content)
        except:
            return False

    @property
    def content(self):
        return self._content

    @property
    def count(self):
        return self._count