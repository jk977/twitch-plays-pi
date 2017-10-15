# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/config.py
# Compiled at: 2017-10-14 01:17:59
# Size of source mod 2**32: 643 bytes
import os

def find_project_root():
    sep = os.path.sep
    reverse_cwd = os.getcwd().split(sep)[::-1]
    try:
        root_index = reverse_cwd.index('bot')
        return sep.join(reverse_cwd[:root_index:-1]) + sep
    except:
        return False


users = {}
root = find_project_root()
info_dir = os.path.join(root, 'bot', 'info')
if not os.access(root, os.W_OK):
    raise PermissionError('Project root is not writable.')
with open(os.path.join(info_dir, 'owner.cfg'), 'r') as file:
    owner = file.read().strip()
with open(os.path.join(info_dir, 'oauth.cfg'), 'r') as file:
    password = file.read().strip()