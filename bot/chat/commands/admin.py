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
    '''
    Command to verify that the decorator works. Used in unit tests.
    '''
    return message

@admin_cmd
def restart(chat, message):
    chat.send_message('Bot is restarting. Inputs won\'t work until the bot is online.')
    chat.close()
    sys.exit(0)
