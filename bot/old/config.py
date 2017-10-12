from emulator import Emulator
from threads.stoppablepool import StoppablePool
from votes.votemanager import VoteManager

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'shira_bot'

with open('info/host.cfg', 'r') as file:
    CHAN = file.read().strip() # bot owner; strip in case of whitespace

with open('info/oauth.cfg', 'r') as file:
    PASS = 'oauth:' + file.read().strip()

# tracks all threads used by bot
threads = StoppablePool()

# TODO make threshold a piecewise function that returns:
#   - 1 for active chatters < 10
#   - % of active chatters for active chatters >= 10

# used in vote tracking
users = {}
vm = VoteManager(threshold=1, on_decision=Emulator.send)
