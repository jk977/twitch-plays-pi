from interfaces.emuinput import EmuInput

class Button(EmuInput):
    _filename = 'inputs.txt'
    
    @classmethod
    def _parse_button(cls, message):
        result = super()._parse_content(message)
        return result.upper() if (result == 'a' or result == 'b') else result

    def _validate_count(count):
        return count < 10 and count > 0

    def _validate_content(content):
        return content in ['A', 'B', 'start', 'select', 'up', 'down', 'left', 'right']