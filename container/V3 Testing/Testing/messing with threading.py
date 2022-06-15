import threading
import sys
import time

def main():
    try:
        event = threading.Event()
        thread = threading.Thread(target=f, args=(event,))
        thread.start()
        # event.wait()  # wait without blocking KeyboardInterrupt
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")
        event.set()  # notify the child thread to exit
        sys.exit(1)


def f(event):
    while not event.is_set():
        time.sleep(1)
        print("hello!")


if __name__ == '__main__':
    main()