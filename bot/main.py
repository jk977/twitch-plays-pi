import config

from chat.commands.commandlist import CommandList
from chat.twitchchat import TwitchChat
from chat.voting.inputmanager import InputManager

from nes.emulator import NES


if __name__ == '__main__':
    chat = TwitchChat(config.nick, config.password, config.owner)
    manager = InputManager(threshold=1, on_decision=NES.send_input)
    
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