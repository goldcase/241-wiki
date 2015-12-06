import os, datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from time import sleep

class GitChangeHandler(PatternMatchingEventHandler):

    def on_any_event(self, event):
        print "Handling event"

if __name__ == '__main__':
    observer = Observer()
    observer.schedule(GitChangeHandler(), path="md-files", recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
