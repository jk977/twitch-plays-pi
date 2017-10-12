from interfaces.emuinput import EmuInput

class Button(EmuInput):
    def _validate_count(count):
        return count < 10 and count > 0

    def _validate_content(content):
        return content in ['A', 'B', 'start', 'select', 'up', 'down', 'left', 'right']