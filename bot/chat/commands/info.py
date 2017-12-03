import config
import os


def show_about(chat, message):
    chat.send_message('This is an open-source Twitch Plays bot hosted on a Raspberry Pi 3. Source can be found at https://github.com/jk977/twitch-plays-pi')


def show_help(chat, message):
    path = os.path.join(config.bot_dir, 'help.dat')

    with open(path, 'r') as file:
        help_link = file.read().strip()

    link = help_link if help_link else '(Link not found. Tell the streamer to fix this!)'
    chat.send_message('View {} for general help. For bot information, type "!about".'.format(help_link))


def song(chat, message):
    chat.send_message('Dragon Quest 1 and 2 Symphonic Suites - ' +
                      'https://www.youtube.com/playlist?list=PL2jLKwo6ZTmQ0vKgGwbcp5m2sp7vy9GXY')


def game_map(chat, message):
    path = os.path.join(config.bot_dir, 'map.dat')

    with open(path, 'r') as file:
        map_link = file.read()

    chat.send_message(map_link)
