import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        super().__init__()
        self.script_name = script_name
        self.process = None
        self.run_script()

    def on_modified(self, event):
        if event.src_path.endswith(self.script_name):
            print(f"Change detected in {self.script_name}. Restarting script...")
            self.restart_script()

    def run_script(self):
        if self.process:
            self.process.terminate()
            self.process.wait()  
        self.process = subprocess.Popen(["python3", self.script_name])

    def restart_script(self):
        self.process.terminate()
        self.process.wait()  
        self.run_script()

if __name__ == "__main__":
    script_name = "patient/patientNew.py"  # Ensure this path is accurate
    event_handler = FileChangeHandler(script_name)

    observer = Observer()
    observer.schedule(event_handler, path="./patient", recursive=False)  # Adjust path if needed for folder
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
