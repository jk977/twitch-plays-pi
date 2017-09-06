import config
import os
import utils

from settings import Settings
from stoppablethread import StoppableThread

from chat.twitchchat import TwitchChat
from chat.user import User
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
        author = message.author
        print('Received message from {}: {}'.format(author, message.content))


       # adds user to list if not present
        if message.author not in config.users:
            is_owner = author == config.CHAN
            config.users[author] = User(name=author, owner=is_owner)

        user = config.users[author]
        cmd = CommandParser.parse(chat, message, user)

        try:
            cmd.run()
        except PermissionError as e:
            send_msg(sock, str(e))
        except AttributeError:
            pass

        if not user.is_banned:
            utils.read_button_input(message.content, user)
