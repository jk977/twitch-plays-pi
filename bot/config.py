import os

def find_project_root():
    sep = os.path.sep
    reverse_cwd = os.getcwd().split(sep)[::-1]

    try:
        root_index = reverse_cwd.index('bot') # one higher than root
        return sep.join(reverse_cwd[:root_index:-1]) + sep
    except:
        return False

root = find_project_root()

if not os.access(root, os.W_OK):
    raise PermissionError('Project root is not writable.')