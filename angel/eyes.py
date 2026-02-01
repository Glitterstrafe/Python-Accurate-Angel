from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer


class TheAllSeeingEye(FileSystemEventHandler):
    def __init__(self, callback, debounce_interval=2.0, ignore_patterns=None):
        self.callback = callback
        self.debounce_interval = debounce_interval
        self.ignore_patterns = ignore_patterns or []
        self.timer = None
        self.last_event_path = None

    def _is_ignored(self, path):
        for pattern in self.ignore_patterns:
            clean_pattern = pattern.replace("*", "")
            if clean_pattern in path:
                return True
        return False

    def _process_event(self):
        """Trigger the callback after silence."""
        if self.last_event_path:
            self.callback(self.last_event_path)

    def on_modified(self, event):
        if event.is_directory or self._is_ignored(event.src_path):
            return

        # Reset timer on new keystroke
        if self.timer:
            self.timer.cancel()

        self.last_event_path = event.src_path
        self.timer = Timer(self.debounce_interval, self._process_event)
        self.timer.start()


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
