import config
import os
import signal
import sys

from chat.commands.commandlist import CommandList
from chat.twitchchat import TwitchChat
from chat.voting.inputmanager import InputManager

from nes.emulator import NES

# initializing client to be used at module level
chat = TwitchChat(config.nick, config.password, config.host)

def startup_tasks():
    chat.send_message('Bot online!')

    signal.signal(signal.SIGALRM, on_stream_restart)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    write_pid()


def on_stream_restart(signum, frame):
    chat.send_message('Stream is restarting!')


def shutdown(signum, frame):
    try:
        os.remove(config.pid_file)
    except:
        pass

    chat.send_message('Bot shutting down.')
    chat.close()
    sys.exit(128 + signum)


def write_pid():
    with open(config.pid_file, 'w') as file:
        file.write(str(os.getpid()))


def log_votes(manager):
    '''
    Called whenever a vote is made; logs the top <= 3 choices to a file for displaying on screen.
    :param manager: InputManager object (passed as self in cast_vote)
    '''
    if manager.threshold == 1:
        return

    path = os.path.join(config.data_dir, 'votes.txt')
    choices = manager.options.get_all(key=lambda p: p[1].votes, reverse=True)
    votes = ('{}: {}\n'.format(c.input, c.votes) for c in choices.values()[:3])

    with open(path, 'w') as file:
        file.writelines(votes)


if __name__ == '__main__':
    startup_tasks()
    manager = InputManager(threshold=1, on_decision=NES.send_input, on_vote=log_votes)

    while True:
        message = chat.get_message()
        content = message.content
        date = message.date.strftime('%c')
        print('{} {}: {}'.format(date, message.author.name, content))

        try:
            manager.cast_vote(message.author, content)
        except:
            cmd = CommandList.get(content, chat, message)

            if cmd:
                cmd.run()
