import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import os

class FileChangeHandler(PatternMatchingEventHandler):
    def __init__(self, command):
        super().__init__(patterns=["*.py"], ignore_directories=True)
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(self.command, shell=True)

    def on_modified(self, event):
        print(f"Arquivo {event.src_path} foi modificado; reiniciando aplicação...")
        self.start_process()

def start_watcher():
    command = "briefcase dev"
    event_handler = FileChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    start_watcher()
