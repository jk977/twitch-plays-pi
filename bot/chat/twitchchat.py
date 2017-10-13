import socket
import time
from interfaces.chat import Chat

class TwitchChat(Chat):
    host = 'irc.twitch.tv'
    port = 6667
    rate = 3/2

    def __init__(self, username, oauth, channel):
        if not channel.startswith('#'):
            channel = '#' + channel

        self._sock = socket.socket()
        self._nick = username
        self._pass = 'oauth:' + oauth
        self._chan = channel

        self.__connect()

    def __sock_send(self, message, encoding='utf-8'):
        self._sock.send(bytes(message, encoding))

    def __authenticate(self, auth_type, content):
        if not auth_type in ['NICK', 'PASS', 'JOIN']:
            raise ValueError('Invalid auth type.')

        message = '{} {}\r\n'.format(auth_type, content)
        self.__sock_send(message)

    def __connect(self):
        self._sock.connect((TwitchChat.host, TwitchChat.port))
        self.__authenticate('PASS', self._pass)
        self.__authenticate('NICK', self._nick)
        self.__authenticate('JOIN', self._chan)

    def send_message(self, content):
        message = 'PRIVMSG {} :{}\r\n'.format(self._chan, content)
        self.__sock_send(message)
        time.sleep(TwitchChat.rate)

    def get_message(self, timeout=-1, quiet=False):
        '''
        Returns next message from server.
        :param timeout: How long to wait before timing out, in seconds (less than 0 indicates never).
        :param quiet: Whether or not to raise an exception or exit silently on timeout.
        '''
        start = time.time()

        while (timeout < 0) or (time.time() - start) < timeout:
            message = self._sock.recv(1024).decode('utf-8')

            if message.startswith('PING'):
                self.__sock_send(message.replace('PING', 'PONG'))
                print('Ping received.')
            else:
                return message

        if not quiet:
            raise TimeoutError('No messages received within timeout duration.')

    def close(self):
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()