import config
import os

from chat.commands.commandlist import CommandList
from chat.twitchchat import TwitchChat
from chat.voting.inputmanager import InputManager

from nes.emulator import NES


def log_votes(manager):
    if manager.threshold == 1:
        return
    
    path = os.path.join(config.root, 'game', 'votes.txt')
    choices = manager.options.get_all(key=lambda p: p[1].votes, reverse=True)
    votes = ['{}: {}'.format(c.input, c.votes) for c in choices.values()]
    print(votes)
    
    with open(path, 'w') as file:
        file.writelines(votes)


if __name__ == '__main__':
    chat = TwitchChat(config.nick, config.password, config.owner)
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