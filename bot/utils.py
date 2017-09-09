def notify_restarts(chat):
    """Notifies chat when stream is restarting by checking for flag file."""
    try:
        os.remove('../restartfile')
        chat.send_message('Stream is restarting!')
    except FileNotFoundError:
        pass


def extract_username(name):
    if not name:
        return

    return name.lower().replace('@', '').strip()
