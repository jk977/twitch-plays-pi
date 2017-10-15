import config

from chat.commands.commandlist import CommandList
from chat.twitchchat import TwitchChat
from chat.voting.inputmanager import InputManager

from nes.choice import EmuChoice
from nes.emulator import NES


if __name__ == '__main__':
    chat = TwitchChat(config.nick, config.password, config.owner)
    manager = InputManager(threshold=1, on_decision=NES.send_input)
    
    while True:
        message = chat.get_message()
        content = message.content
        date = message.date.strftime('%H:%M:%S')
        print('{}\t{}: {}'.format(date, message.author.name, content))
        
        try:
            choice = EmuChoice(content)
            manager.cast_vote(message.author, choice.name)
        except:
            if CommandList.validate(content):
                cmd = CommandList.get(content, chat, message)
                cmd.run()