import config
import re

from stoppablethread import StoppableThread


def stop_all_threads():
    """Stops created threads."""
    stoppables = [t for t in config.threads if isinstance(t, StoppableThread)]
    for thread in stoppables:
        thread.stop()


def finalize_thread(thread):
    """Removes thread from thread list after thread finishes."""
    with config.threads_lock:
        try:
            config.threads.remove(thread)
        except:
            pass


def format_button_input(message):
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
    elif button not in config.button_opts or not re.match('[1-9]', mult):
        return

    return mult + button


def read_button_input(message, user):
    vote = format_button_input(message)

    if not vote:
        return

    vote_count = user.vote(config.vm, vote)

    # TODO allow VoteManager to take a callback that's called
    # when threshold exceeded instead of exposing it here 
    if vote_count >= config.vm.threshold:
        t = StoppableThread(after=finalize_thread, target=send_input, args=('inputs.txt', vote))
        config.threads.append(t)
        t.start()

        config.vm.reset()


def read_cheat_input(cheat, user):
    if cheat not in config.cheat_opts:
        return

    vote_count = user.vote(config.vm, cheat)

    # see the todo above
    if vote_count >= config.vm.threshold:
        t = StoppableThread(after=finalize_thread, target=send_input, args=('cheats.txt', cheat))
        config.threads.append(t)
        t.start()

        config.vm.reset()
        

def send_input(filename, contents):
    for i in range(10):
        try:
            with open('../' + filename, 'w+') as file:
                file.write(contents)
                print('>>>Sent ' + contents + ' to emulator.')
                break
        except:
            sleep(1)


def extract_username(name):
    if not name:
        return

    return name.lower().replace('@', '').strip()
