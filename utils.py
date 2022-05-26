from threading import get_ident


def log(msg):
    print(f"\nThread {get_ident()}: {msg}\n\n -------------------------------")
