import config
import os
import utils

from emulator import Emulator
from settings import Settings

from chat.twitchchat import TwitchChat
from chat.commandparser import CommandParser


def notify_restarts(chat):
    """Notifies chat when stream is restarting by checking for flag file."""
    try:
        os.remove('../restartfile')
        chat.send_message('Stream is restarting!')
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    Settings.load_settings()
    chat = TwitchChat(config.NICK, config.PASS, config.CHAN)
    chat.send_message('Bot connected!')

    # polls restart file every second and posts stream status if restarting
    stream_thread = StoppableThread(
            period=1,
            target=notify_restarts,
            args=(chat,),
            after=utils.finalize_thread,
            daemon=True)

    stream_thread.start()
    config.threads.append(stream_thread)

    # periodically saves current users to settings file
    settings_thread = StoppableThread(
            period=10,
            target=Settings.save_settings,
            after=utils.finalize_thread)

    settings_thread.start()
    config.threads.append(settings_thread)

    # main loop
    while True:
        message = chat.wait_for_message()
        content = message.content
        author = message.author
        print('Received message from {}: {}'.format(author.name, message.content))

        if author.name == 'tmi':
            # ignores twitch server messages
            continue
        elif Emulator.validate_input(content):
            # sends vote if valid
            config.vm.add_vote(author, content)
        else:
            try:
                cmd = CommandParser.parse(chat, message)
                cmd.run()
            except PermissionError as e:
                chat.send_message(str(e))
            except:
                pass
