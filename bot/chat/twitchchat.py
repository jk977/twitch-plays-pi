import re
import socket
import threading

from time import sleep
from chat.message import Message


class TwitchChat:
    rate_limit = 3/2 # seconds per message

    def __init__(self, username, password, channel):
        self._name = username
        self._pass = password

        self._host = 'irc.twitch.tv'
        self._port = 6667
        self._chan = channel

        self._sock = socket.socket()
        self._lock = threading.Lock()

        self._connect()


    def _connect(self):
        self._sock.connect((self._host, self._port))
        self._sock.send('PASS {}\r\n'.format(self._pass).encode('utf-8'))
        self._sock.send('NICK {}\r\n'.format(self._name).encode('utf-8'))
        self._sock.send('JOIN #{}\r\n'.format(self._chan).encode('utf-8'))


    def send_message(self, content):
        with self._lock:
            print('Sent in {}: {}'.format(self._chan, content))
            self._sock.send(bytes('PRIVMSG #' + self._chan + ' :' + content + '\r\n', 'utf-8'))
            sleep(TwitchChat.rate_limit)


    def wait_for_message(self):
        CHAT_MSG = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')

        while True:
            response = self._sock.recv(1024).decode('utf-8')

            if response.startswith('PING :tmi.twitch.tv'):
                self._sock.send(bytes(response.replace('PING', 'PONG'), 'utf-8'))
            else:
                return Message(response)


    def ban(self, user):
        self.send_message('.ban {}'.format(user))


    def timeout(self, user, seconds=600):
        self.send_message('.timeout {}'.format(user, seconds))


    def close(self):
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()
