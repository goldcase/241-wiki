import os, datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from time import sleep

class GitChangeHandler(PatternMatchingEventHandler):
    def process(self):
        print "Handling event."
        # Challenge some assumptions about the current directory.
        if not os.path.exists("gh-pages"):
            os.chdir(os.pardir)
        print os.getcwd()
        os.system("python md.py")
        sleep(5)
        os.chdir("gh-pages")
        os.system("git add .")
        os.system("git commit -m 'Detected change at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".'")
        os.system("git push origin gh-pages")
        os.chdir(os.pardir)
        print os.getcwd()

    def on_modified(self, event):
        self.process()

    def on_created(self, event):
        self.process()

    def on_deleted(self, event):
        self.process()

def pull_directory():
    print "Pulling " + str(os.getcwd())
    # A hack.
    if os.path.exists("md-files"):
        os.chdir("md-files")
    os.system("git pull origin master")
    os.chdir(os.pardir)

if __name__ == '__main__':
    #os.chdir("md-files")
    observer = Observer()
    observer.schedule(GitChangeHandler(), path="md-files", recursive=True)
    observer.start()

    try:
        while True:
            pull_directory()
            sleep(30)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
