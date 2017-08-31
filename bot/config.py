# config.py
# contains bot configuration

from user import User
from votes.votemanager import VoteManager

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'shira_bot'
RATE = 3/2

with open('info/host.cfg', 'r') as file:
    CHAN = file.read().strip() # bot owner; strip in case of unintended whitespace

with open('info/oauth.cfg', 'r') as file:
    PASS = 'oauth:' + file.read().strip()

button_opts = ['A', 'B', 'start', 'select', 'up', 'down', 'left', 'right']
cheat_opts = ['heal', 'killall', 'showgil']

users = {}
vm = VoteManager(threshold=1)
