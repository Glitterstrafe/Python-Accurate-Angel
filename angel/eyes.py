from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer
import os


class TheAllSeeingEye(FileSystemEventHandler):
    def __init__(self, callback, debounce_interval=2.0, ignore_patterns=None):
        self.callback = callback
        self.debounce_interval = debounce_interval
        self.ignore_patterns = ignore_patterns or []
        self.timer = None
        self.last_event_path = None

    def _is_ignored(self, path):
        # Ignore directories and temp files
        if os.path.isdir(path):
            return True

        # Check config ignore patterns
        for pattern in self.ignore_patterns:
            clean_pattern = pattern.replace("*", "")
            if clean_pattern in path:
                return True

        # Explicit ignore for the database/log files to prevent loops
        if "angel_chronicles" in path or "angel_state" in path:
            return True

        return False

    def _trigger_debounce(self, file_path):
        """Standardized trigger logic for ANY event type."""
        if self._is_ignored(file_path):
            return

        # Cancel existing timer to reset the clock (debounce)
        if self.timer:
            self.timer.cancel()

        self.last_event_path = file_path
        self.timer = Timer(self.debounce_interval, lambda: self.callback(self.last_event_path))
        self.timer.start()

    def on_modified(self, event):
        self._trigger_debounce(event.src_path)

    def on_moved(self, event):
        # Atomic saves often look like moves (dest_path is the real file)
        self._trigger_debounce(event.dest_path)

    def on_created(self, event):
        # New files should also trigger the angel
        self._trigger_debounce(event.src_path)


class VisionSystem:
    def __init__(self, path, callback, config):
        self.observer = Observer()
        self.handler = TheAllSeeingEye(
            callback,
            config['vision']['debounce_seconds'],
            config['vision']['ignore_patterns']
        )
        self.path = path

    def open_eyes(self):
        self.observer.schedule(self.handler, self.path, recursive=True)
        self.observer.start()

    def close_eyes(self):
        self.observer.stop()
        self.observer.join()
