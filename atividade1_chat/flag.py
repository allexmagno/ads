from threading import Event, Lock

def init():
    global event, lock

    event = Event()
    lock = Lock()