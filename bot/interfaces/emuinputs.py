from . import *
from interfaces.validator import Validator


class EmuInputs(Validator):
    '''
    Base class for type-safe containers containing EmuInput children classes. Note that children
    must implement __init__ and deserialize in addition to the two abstract properties below.
    '''
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        for i in range(len(self.inputs)):
            if self.inputs[i] != other.inputs[i]:
                return False

        return True

    @abstractproperty
    def destination(self):
        pass

    @abstractproperty
    def inputs(self):
        pass

    @classmethod
    def _truncate(cls, inputs, limit):
        '''
        Truncates inputs list if necessary to make the sum of input counts less than or equal to limit.
        :param cls: Current class.
        :param inputs: List of inputs to truncate.
        :param limit: Maximum allowed count sum in outputted input list.
        '''
        out = []
        total = 0
        
        if limit == 0:
            return out
        elif limit < 0:
            raise ValueError('Limit must be a positive number.')

        for i in inputs:
            elem_cls = type(i)

            if total + i.count > limit:
                count = limit - total
                out.append(elem_cls(i.content, count))
                break
            else:
                total += i.count
                out.append(i)

        return out

    def serialize(self):
        return ' '.join((i.serialize() for i in self.inputs))