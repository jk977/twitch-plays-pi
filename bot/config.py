# config.py
# contains bot configuration

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'shira_bot'
RATE = 3/2

with open('info/host.cfg', 'r') as file:
    CHAN = file.read().strip() # bot owner; strip in case of unintended whitespace

with open('info/oauth.cfg', 'r') as file:
    PASS = 'oauth:' + file.read().strip()

chatters = {}
button_opts = ['A', 'B', 'start', 'select', 'up', 'down', 'left', 'right']
cheat_opts = ['heal', 'killall']
button_inputs = {}
cheat_inputs = {}
vote_threshold = 1 # threshold for sending input to emulator
