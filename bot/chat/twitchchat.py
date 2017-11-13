import re
import socket
import threading
import time

from chat.message import Message
from chat.user import User
from interfaces.chat import Chat


class TwitchChat(Chat):
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
        
        self._sock = None
        self._sock_lock = threading.Lock()

        self.__connect()

    def __sock_send(self, message, encoding='utf-8'):
        '''
        Sends message over socket in bytes format.
        :param message: Message to send.
        :param encoding: Encoding of string.
        '''
        with self._sock_lock:
            self._sock.send(bytes(message, encoding))

    def __authenticate(self, auth_type, authentication):
        '''
        Sends authentication message to server.
        :param auth_type: One of three types: NICK, PASS, or JOIN
        :param authentication: Content corresponding to auth_type.
        '''
        if auth_type not in ('NICK', 'PASS', 'JOIN'):
            raise ValueError('Invalid auth type.')

        message = '{} {}\r\n'.format(auth_type, authentication)
        self.__sock_send(message)

    def __connect(self):
        '''
        Connects client to server.
        :param replace_current_socket: Whether or not to dispose of the current socket.
        '''
        if self._sock:
            self.close()

        self._sock = socket.socket()
        self._sock.setblocking(True)
        self._sock.connect((TwitchChat.host, TwitchChat.port))

        self.__authenticate('PASS', self._pass)
        self.__authenticate('NICK', self._nick)
        self.__authenticate('JOIN', self._chan)

    def __get_raw_message(self, timeout):
        '''
        Gets a UTF-8 decoded message from the server, responding to pings as needed
        '''
        while timeout:
            raw_message = self._sock.recv(1024).decode('utf-8')

            if raw_message.startswith('PING'):
                self.__sock_send(raw_message.replace('PING', 'PONG'))
                print('Ping received.')
            else:
                return raw_message

    def _parse_message(raw_message):
        '''
        Parses raw message from server and returns a Message object.
        :param raw_message: UTF-8 encoded message from server.
        '''
        result = re.search('^:(\\w+)!\\w+@[\\w.]+ [A-Z]+ #\\w+ :(.+)\\r\\n', raw_message)

        if not result:
            return

        author, content = result.groups()
        author = User(author)
        return Message(author, content)

    def send_message(self, content, max_attempts=2):
        '''
        Sends message to server and sleeps.
        :param content: The message to send.
        :param max_attempts: The maximum number of failed attempts to allow when sending message.
        '''
        message = 'PRIVMSG {} :{}\r\n'.format(self._chan, content)

        for _ in range(max_attempts):
            try:
                self.__sock_send(message)
                time.sleep(TwitchChat.rate)
                break
            except socket.error:
                self.__connect() # re-establish connection and try again

    def get_message(self, timeout=-1):
        '''
        Returns next message from server.
        '''
        start = time.time()
        no_timeout = timeout < 0

        while no_timeout or (time.time() - start) < timeout:
            try:
                raw_message = self.__get_raw_message(timeout)
                message = TwitchChat._parse_message(raw_message)
                
                if message:
                    return message

            except socket.error:
                self.__connect()
            except ValueError:
                pass

    def close(self):
        '''
        Closes server connection.
        '''
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()