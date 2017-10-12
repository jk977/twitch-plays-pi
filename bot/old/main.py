import config
import utils

from emulator import Emulator
from settings import Settings

from chat.twitchchat import TwitchChat
from chat.commandparser import CommandParser


if __name__ == '__main__':
    Settings.load_settings()
    chat = TwitchChat(config.NICK, config.PASS, config.CHAN)
    chat.send_message('Bot connected!')

    # polls restart file every second and posts stream status if restarting
    config.threads.start_thread(
            period=1,
            target=utils.notify_restarts,
            args=(chat,),
            daemon=True)

    # periodically saves current users to settings file
    config.threads.start_thread(period=10, target=Settings.save_settings)

    # main loop
    while True:
        message = chat.wait_for_message()
        content = message.content
        author = message.author
        print('Received message from {}: {}'.format(author.name, content))

        if author.name == 'tmi':
            # ignores twitch server messages
            continue
        elif Emulator.validate_input(content):
            # sends vote if valid
            input_msg = Emulator.parse_input(content)
            author.vote(config.vm, input_msg)
        else:
            try:
                cmd = CommandParser.parse(chat, message)
                cmd.run()
            except PermissionError as e:
                chat.send_message(str(e))
            except:
                pass
