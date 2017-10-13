import config

def show_help(chat, message):
    with open(config.root + '/bot/info/help.cfg', 'r') as file:
        help_link = file.read()

    chat.send_message(help_link)

def song(chat, message):
    chat.send_message('Dragon Quest 1 and 2 Symphonic Suites - ' +
                      'https://www.youtube.com/playlist?list=PL2jLKwo6ZTmQ0vKgGwbcp5m2sp7vy9GXY')