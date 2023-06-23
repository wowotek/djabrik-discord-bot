from datetime import datetime


DEBUG_MODE = False

def __get_time():
    t = datetime.now()

    return t.isoformat().split(".")[0]

def debug(*args, **kwargs):
    if DEBUG_MODE: print(f"[{__get_time()}][DEBUG]", *args, **kwargs)

def info(*args, **kwargs):
    print(f"[{__get_time()}] [INFO]", *args, **kwargs)