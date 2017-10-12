import threading
from time import sleep
from threads.stoppablethread import StoppableThread


# initializing test variables

def test():
    pass

def after(thread):
    print('Calling {}\'s after'.format(thread.name))
    with threads_lock:
        threads.remove(thread)
        print(thread.name + ' finished. {} threads still in list.'.format(len(threads)))


t1 = StoppableThread(target=test, after=after, timeout=1, period=0.5)
t2 = StoppableThread(target=test, after=after, timeout=2, period=0.9)
t3 = StoppableThread(target=test, after=after, timeout=5, period=2)
t4 = StoppableThread(target=test, after=after)
t5 = StoppableThread(target=test, after=after)
t6 = StoppableThread(target=test, after=after)

threads = [t1,t2,t3,t4,t5,t6]
threads_lock = threading.Lock()

print('---------------------')
print('Threads\n')

for i in range(5):
    print('t{}: {}'.format(i+1, threads[i].name))

print('---------------------\n')


def live_thread_count():
    """Returns -1 if no threads are alive, 0 if some are alive, or 1 if all threads are alive"""
    with threads_lock:
        return len([t for t in threads if t.is_alive()])


def start_all_threads():
 with threads_lock:
    for t in threads:
        print('Starting ' + t.name)
        t.start()
    print()


def stop_all_threads():
    with threads_lock:
        for t in threads:
            print('Stopping ' + t.name)
            t.stop()
        print()


def test_threads():
    # start threads and let some finish
    start_all_threads()
    sleep(4)

    # first two looping threads should be timed out at this point
    try:
        loops_done = not (t1.is_alive() or t2.is_alive())
        assert(loops_done)
        print('First two threads finished.')
        assert(t3.is_alive())
        print('Third loop alive.')

    except AssertionError:
        print('\nAssertion failed.\n')
        stop_all_threads()
        return False

    # third loop should still be alive
    stop_all_threads()
    print('Waiting for loop 3 to stop...')
    sleep(2)

    live_threads = live_thread_count()

    if live_threads > 0:
        print('{} thread(s) still active.'.format(live_threads))

    return live_threads == 0 and len(threads) == 0


if __name__ == '__main__':
    if test_threads():
        print('Test successful!')
    else:
        print('Test failed.')
