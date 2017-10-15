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