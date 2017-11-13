import config
import os
import signal

from chat.commands.commandlist import CommandList
from chat.twitchchat import TwitchChat
from chat.voting.inputmanager import InputManager

from nes.emulator import NES

# initializing client to be used at module level
chat = TwitchChat(config.nick, config.password, config.host)

def log_votes(manager):
    '''
    Called whenever a vote is made; logs the top <= 3 choices to a file for displaying on screen.
    :param manager: InputManager object (passed as self in cast_vote)
    '''
    if manager.threshold == 1:
        return

    path = os.path.join(config.root, 'game', 'votes.txt')
    choices = manager.options.get_all(key=lambda p: p[1].votes, reverse=True)
    votes = ('{}: {}\n'.format(c.input, c.votes) for c in choices.values()[:3])

    with open(path, 'w') as file:
        file.writelines(votes)


def notify_restart(signal, frame):
    '''
    Sends notification message to twitch when receiving SIGALRM
    '''
    chat.send_message('Stream is restarting!')

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, notify_restart)
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
