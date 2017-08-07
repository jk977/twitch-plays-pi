# config.py
# contains bot configuration

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'shira_bot'

with open('info/host.cfg', 'r') as file:
    CHAN = file.read() # bot owner

with open('info/oauth.cfg', 'r') as file:
    PASS = 'oauth:' + file.read()

chatters = {}
button_opts = ['A', 'B', 'start', 'select', 'up', 'down', 'left', 'right']
button_inputs = {}
button_threshold = 1 # threshold for sending input to emulator
