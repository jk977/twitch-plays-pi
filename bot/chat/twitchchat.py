import re
import socket
import time
from chat.message import Message
from chat.user import User
from interfaces.chat import Chat

class TwitchChat(Chat):
    blacklist = [
     'tmi\\.twitch\\.tv', 'shira_bot$']
    host = 'irc.twitch.tv'
    port = 6667
    rate = 1.5

    def __init__(self, username, oauth, channel):
        if not channel.startswith('#'):
            channel = '#' + channel
        self._nick = username
        self._pass = 'oauth:' + oauth
        self._chan = channel
        self._sock = socket.socket()
        self._sock.setblocking(True)
        self._TwitchChat__connect()

    def __sock_send(self, message, encoding='utf-8'):
        self._sock.send(bytes(message, encoding))

    def __authenticate(self, auth_type, content):
        if auth_type not in ('NICK', 'PASS', 'JOIN'):
            raise ValueError('Invalid auth type.')
        message = '{} {}\r\n'.format(auth_type, content)
        self._TwitchChat__sock_send(message)

    def __connect(self):
        self._sock.connect((TwitchChat.host, TwitchChat.port))
        self._TwitchChat__authenticate('PASS', self._pass)
        self._TwitchChat__authenticate('NICK', self._nick)
        self._TwitchChat__authenticate('JOIN', self._chan)

    def _parse_message(raw_message):
        """
        Parses raw message from server and returns a Message object.
        :param raw_message: UTF-8 decoded message from server.
        """
        author, content = re.search('^:(\\w+)!\\w+@[\\w.]+ [A-Z]+ #\\w+ :(.+)\\r\\n', raw_message).groups()
        author = User(author)
        return Message(author, content)

    def send_message(self, content):
        """
        Sends message to server and sleeps.
        :param content: The message to send.
        """
        message = 'PRIVMSG {} :{}\r\n'.format(self._chan, content)
        try:
            self._TwitchChat__sock_send(message)
        except socket.error:
            self._TwitchChat__sock_send(message)

        time.sleep(TwitchChat.rate)

    def get_message(self, timeout=-1, quiet=False):
        """
        Returns next message from server.
        :param timeout: How long to wait before timing out, in seconds (less than 0 indicates never).
        :param quiet: Whether or not to raise an exception or exit silently on timeout.
        """
        start = time.time()
        while 1:
            if timeout < 0 or time.time() - start < timeout:
                message = self._sock.recv(1024).decode('utf-8')
                author = re.search('^:([\\w.]+)', message)
                author = author.groups()[0] if author else None
                if message.startswith('PING'):
                    self._TwitchChat__sock_send(message.replace('PING', 'PONG'))
                    print('Ping received.')
            elif not any((re.search(user, author) for user in TwitchChat.blacklist)):
                return TwitchChat._parse_message(message)

        if not quiet:
            raise TimeoutError('No messages received within timeout duration.')

    def close(self):
        """
        Closes server connection.
        """
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()