import re
import socket
import time

from chat.message import Message
from chat.user import User
from interfaces.chat import Chat


class TwitchChat(Chat):
    blacklist = ['tmi\.twitch\.tv', 'shira_bot$']
    host = 'irc.twitch.tv'
    port = 6667
    rate = 1.5

    def __init__(self, username, oauth, channel):
        '''
        Creates IRC client for Twitch chat at specified channel.
        :param username: Username to log in with.
        :param oauth: OAuth token to authenticate with.
        :param channel: Channel to connect to.
        '''
        if not channel.startswith('#'):
            channel = '#' + channel
            
        self._nick = username
        self._pass = 'oauth:' + oauth
        self._chan = channel
        self.__connect()

    def __sock_send(self, message, encoding='utf-8'):
        self._sock.send(bytes(message, encoding))

    def __authenticate(self, auth_type, content):
        if auth_type not in ('NICK', 'PASS', 'JOIN'):
            raise ValueError('Invalid auth type.')

        message = '{} {}\r\n'.format(auth_type, content)
        self.__sock_send(message)

    def __connect(self):
        self._sock = socket.socket()
        self._sock.setblocking(True)
        self._sock.connect((TwitchChat.host, TwitchChat.port))

        self.__authenticate('PASS', self._pass)
        self.__authenticate('NICK', self._nick)
        self.__authenticate('JOIN', self._chan)

    def _parse_message(raw_message):
        '''
        Parses raw message from server and returns a Message object.
        :param raw_message: UTF-8 encoded message from server.
        '''
        author, content = re.search('^:(\\w+)!\\w+@[\\w.]+ [A-Z]+ #\\w+ :(.+)\\r\\n', raw_message).groups()
        author = User(author)
        return Message(author, content)

    def send_message(self, content):
        '''
        Sends message to server and sleeps.
        :param content: The message to send.
        '''
        message = 'PRIVMSG {} :{}\r\n'.format(self._chan, content)

        try:
            self.__sock_send(message)
        except socket.error as e:
            if type(e) != socket.timeout:
                self.close()
                self.__connect()

            self.__sock_send(message)

        time.sleep(TwitchChat.rate)

    def get_message(self, timeout=None):
        '''
        Returns next message from server.
        :param timeout: How long to wait before timing out, in seconds (None indicates never).
        '''
        start = time.time()

        while (timeout is None) or (time.time() - start) < timeout:
            remaining = timeout - (time.time() - start) if timeout else None
            self._sock.settimeout(remaining)

            try:
                message = self._sock.recv(1024).decode('utf-8')
            except socket.timeout:
                self._sock.setblocking(True)
                raise
            except socket.error:
                self.close()
                self.__connect()
                continue

            author = re.search('^:([\\w.]+)', message)
            author = author.groups()[0] if author else None

            if message.startswith('PING'):
                self.__sock_send(message.replace('PING', 'PONG'))
                print('Ping received.')

            elif not any(re.search(user, author) for user in TwitchChat.blacklist):
                self._sock.setblocking(True)
                return TwitchChat._parse_message(message)

    def close(self):
        '''
        Closes server connection.
        '''
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()