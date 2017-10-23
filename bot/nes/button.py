import os

from interfaces.emuinput import EmuInput
from numbers import Number


class Button(EmuInput):
    destination = os.path.join(EmuInput.path, 'inputs.txt')

    @classmethod
    def _parse_content(cls, message):
        '''
        Overrides parent method to accomodate for FCEUX Lua interface button
        format and allow shortcuts.
        '''
        message = Button._substitute(message)
        result = super()._parse_content(message)
        return result.upper() if result in ('a', 'b') else result
    
    def _substitute(message):
        '''
        Makes shortcut substitutions for input string and returns new string.
        :param message: Message to perform substitutions on.
        '''
        button_map = {
            ('^', '⬆️'): 'up',
            ('v', '⬇'): 'down',
            ('<', '⬅️'): 'left',
            ('>', '➡'): 'right'
        }

        for s_list in button_map:
            for shortcut in s_list:
                message = message.replace(shortcut, button_map[s_list])
                
        return message


    def _validate_count(count):
        return isinstance(count, Number) and count > 0

    def _validate_content(content):
        return content.lower() in ('a', 'b', 'start', 'select', 'up', 'down', 'left', 'right')