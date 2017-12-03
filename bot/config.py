import os


def find_project_root():
    sep = os.path.sep
    reverse_cwd = os.getcwd().split(sep)[::-1]
    try:
        root_index = reverse_cwd.index('bot')
        return sep.join(reverse_cwd[:root_index:-1]) + sep
    except:
        return False


def read_data(filename):
    try:
        with open(os.path.join(bot_dir, filename), 'r') as file:
            value = file.read().strip()
        return value
    except:
        print('Error reading {}.'.format(filename))


users = {}
root = find_project_root()

home = os.path.expanduser('~')
data_dir = os.path.join(home, '.twitch-plays-pi')
bot_dir = os.path.join(data_dir, 'bot')
pid_file = os.path.join(data_dir, 'proc', 'bot.py.id')

if not os.access(root, os.W_OK):
    raise PermissionError('Project root is not writable.')

nick = read_data('nick.dat')
password = read_data('pass.dat')
host = read_data('host.dat')
owner = read_data('owner.dat')

try:
    threshold = int(read_data('threshold.dat'))
    threshold = max(threshold, 1)
except:
    threshold = 1
