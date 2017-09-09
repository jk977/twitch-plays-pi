import config
import re
import utils


class Emulator:
    _button_file = '../inputs.txt'
    _cheat_file = '../cheats.txt'

    buttons = ['A', 'B', 'start', 'select', 'up', 'down', 'left', 'right']
    cheats = ['heal', 'killall', 'showgil', 'attack', 'run']


    def validate_input(message):
        """Returns true if message is valid emulator input"""
        try:
            Emulator.parse_button(message)
        except ValueError:
            try:
                Emulator.parse_cheat(message)
            except ValueError:
                return False

        return True


    def send(message):
        """Sends message to emulator if button or cheat."""
        try:
            message = Emulator.parse_button(message)
            Emulator._send_button(message)
        except ValueError:
            try:
                message = Emulator.parse_cheat(message)
                Emulator._send_cheat(message)
            except ValueError:
                pass


    def parse_button(message):
        """Formats input to be sent to lua script"""
        # stores alternate mappings for buttons
        mappings = {
            ('r', '➡️', '☞', '👉'): 'right',  # right arrow and 2 pointing right emojis
            ('l', '⬅️', '☜', '👈'): 'left',   # left arrow and 2 pointing left emojis
            ('u', '⬆️', '☝', '👆'): 'up',     # up arrow and 2 pointing up emojis
            ('d', '⬇️', '👇'): 'down',        # down arrow and pointing down emojis
            ('🅱️', '👎', '🙅'): 'b',           # b, no good, and thumbs down emojis
            ('🅰️', '👌', '👍'): 'a'            # a, ok hand, and thumbs up emojis
        }

        has_leading_num = bool(re.search('^[1-9]', message))
        has_trailing_num = bool(re.search('[1-9]$', message))

        if has_leading_num:
            mult = message[0]
            button = message[1:]
        elif has_trailing_num:
            mult = message[-1]
            button = message[:-1]
        else:
            mult = '1'
            button = message

        button = button.strip().lower()

        for key in mappings:
            if button in key:
                button = mappings[key]

        # capitalizes 'a' and 'b' due to FCEUX input format
        if button in ['a', 'b']:
            button = button.upper()
        elif button not in Emulator.buttons or not re.match('[1-9]', mult):
            raise ValueError('Invalid button.')

        return mult + button


    def parse_cheat(message):
        message = message.strip().lower()

        if message not in Emulator.cheats:
            raise ValueError('Invalid cheat.')

        return message


    def _send_to_file(filename, contents):
        for _ in range(10):
            try:
                with open(filename, 'w+') as file:
                    file.write(contents)
                    print('>>>Sent {} to emulator.'.format(contents))
                    break
            except:
                sleep(1)


    def _send_button(button):
        config.threads.start_thread(target=Emulator._send_to_file, args=(Emulator._button_file, button))

    def _send_cheat(cheat):
        config.threads.start_thread(target=Emulator._send_to_file, args=(Emulator._cheat_file, cheat))


