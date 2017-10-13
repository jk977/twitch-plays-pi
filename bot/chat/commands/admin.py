import sys

def admin_cmd(func):
    '''
    Decorator that prevents function execution if message author isn't admin.
    '''
    def wrapper(chat, message):
        if message.author.admin:
            return func(chat, message)

    return wrapper

@admin_cmd
def test_cmd(chat, message):
    return message

@admin_cmd
def restart(chat, message):
    chat.close()
    sys.exit(0)