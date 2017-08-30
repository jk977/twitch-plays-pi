# config.py
# contains bot configuration

from choices import Choices

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'shira_bot'
RATE = 2

with open('info/host.cfg', 'r') as file:
    CHAN = file.read().strip() # bot owner; strip in case of unintended whitespace

with open('info/oauth.cfg', 'r') as file:
    PASS = 'oauth:' + file.read().strip()

button_opts = ['A', 'B', 'start', 'select', 'up', 'down', 'left', 'right']
cheat_opts = ['heal', 'killall', 'showgil']

chatters = {}
button_inputs = Choices(choice_format=r'^[1-9][a-zA-Z]+$', threshold=1)
cheat_inputs = Choices(choice_format=r'^[a-zA-Z]+$', threshold=1)
