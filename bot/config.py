from emulator import Emulator

from threads.stoppablepool import StoppablePool
from votes.votemanager import VoteManager


# IRC configuration
# =================

HOST = 'irc.twitch.tv'
PORT = 6667
NICK = 'shira_bot'
RATE = 2

with open('info/host.cfg', 'r') as file:
    CHAN = file.read().strip() # bot owner; strip in case of unintended whitespace

with open('info/oauth.cfg', 'r') as file:
    PASS = 'oauth:' + file.read().strip()


# Bot configuration
# =================

threads = StoppablePool()

# used in vote tracking
users = {}
vm = VoteManager(threshold=1, on_decision=Emulator.send)
