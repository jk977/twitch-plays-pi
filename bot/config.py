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
home = os.path.expanduser('~')
data_dir = os.path.join(home, '.twitch-plays-pi', 'bot')

if not os.access(root, os.W_OK):
    raise PermissionError('Project root is not writable.')

with open(os.path.join(data_dir, 'nick.dat'), 'r') as file:
    nick = file.read().strip()

with open(os.path.join(data_dir, 'pass.dat'), 'r') as file:
    password = file.read().strip()

with open(os.path.join(data_dir, 'host.dat'), 'r') as file:
    host = file.read().strip()

with open(os.path.join(data_dir, 'owner.dat'), 'r') as file:
    owner = file.read().strip()