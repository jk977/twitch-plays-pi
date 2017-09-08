import config


def stop_all_threads():
    """Stops created threads."""
    for thread in config.threads:
        thread.stop()


def finalize_thread(thread):
    """Removes thread from thread list after thread finishes."""
    with config.threads_lock:
        try:
            config.threads.remove(thread)
        except:
            pass


def extract_username(name):
    if not name:
        return

    return name.lower().replace('@', '').strip()
