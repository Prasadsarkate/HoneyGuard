import os
import time
import yaml
import threading
from typing import Dict, Set, Tuple, List
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
)
from src.core.forensics import collect_basic
from src.core.alert_manager import send_alert
from src.utils.logger import log_event


# -------------------------
# Helpers
# -------------------------

def _settings():
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def _emit(action: str, path: str, extra: dict | None = None):
    """Send a unified alert + log for any FS action."""
    info = collect_basic(path)
    if extra:
        try:
            info.update(extra)  # type: ignore
        except Exception:
            pass
    msg = f"🔴 {action.upper()} detected → {path}"
    send_alert(msg, info)
    level = "WARNING" if action.lower() in {"deleted", "moved", "modified", "opened", "created"} else "INFO"
    log_event(f"{action.upper()} :: {path} :: {extra or {}}", level)

def _normalize_paths(paths: List[str]) -> List[str]:
    return [os.path.abspath(p) for p in paths]

def _list_files(target: str) -> Set[str]:
    """Return files to track for 'open/read' detection."""
    if os.path.isfile(target):
        return {target}
    out: Set[str] = set()
    if os.path.isdir(target):
        try:
            for name in os.listdir(target):
                fp = os.path.join(target, name)
                if os.path.isfile(fp):
                    out.add(fp)
        except Exception:
            pass
    return out


# -------------------------
# Access-time watcher (OPEN/READ detection)
# -------------------------

class AtimeWatcher(threading.Thread):
    """Detect file OPEN/READ events using access-time (atime)."""

    def __init__(self, targets: List[str], interval: float = 1.0):
        super().__init__(daemon=True)
        self.interval = interval
        self.targets = _normalize_paths(targets)
        self._stop = threading.Event()
        self.meta: Dict[str, Tuple[float, float, int]] = {}
        self._prime()

    def _prime(self):
        files = set()
        for t in self.targets:
            files |= _list_files(t)
        for f in files:
            try:
                st = os.stat(f)
                self.meta[f] = (st.st_atime, st.st_mtime, st.st_size)
            except FileNotFoundError:
                continue

    def update_watchlist_for_dir(self, directory: str):
        if not os.path.isdir(directory):
            return
        current = _list_files(directory)
        for f in current:
            if f not in self.meta:
                try:
                    st = os.stat(f)
                    self.meta[f] = (st.st_atime, st.st_mtime, st.st_size)
                except FileNotFoundError:
                    continue
        for f in list(self.meta.keys()):
            if f.startswith(os.path.abspath(directory) + os.sep) and f not in current:
                self.meta.pop(f, None)

    def stop(self):
        self._stop.set()

    def run(self):
        while not self._stop.is_set():
            time.sleep(self.interval)
            for f in list(self.meta.keys()):
                try:
                    st = os.stat(f)
                except FileNotFoundError:
                    self.meta.pop(f, None)
                    continue
                last_at, last_mt, last_sz = self.meta[f]
                if st.st_atime > last_at and st.st_mtime == last_mt:
                    _emit("opened/read", f, {"size": st.st_size})
                self.meta[f] = (st.st_atime, st.st_mtime, st.st_size)


# -------------------------
# Watchdog handler for file events
# -------------------------

class HoneyFileHandler(FileSystemEventHandler):
    def __init__(self, atime_watcher: AtimeWatcher | None = None):
        super().__init__()
        self.atime_watcher = atime_watcher

    def on_created(self, event: FileCreatedEvent):
        if event.is_directory:
            if self.atime_watcher:
                self.atime_watcher.update_watchlist_for_dir(event.src_path)
            return
        _emit("created", event.src_path, {"event": "created"})

    def on_deleted(self, event: FileDeletedEvent):
        if event.is_directory:
            if self.atime_watcher:
                self.atime_watcher.update_watchlist_for_dir(event.src_path)
            return
        _emit("deleted", event.src_path, {"event": "deleted"})

    def on_modified(self, event: FileModifiedEvent):
        if event.is_directory:
            return
        try:
            st = os.stat(event.src_path)
            extra = {"event": "modified", "size": st.st_size}
        except Exception:
            extra = {"event": "modified"}
        _emit("modified", event.src_path, extra)

    def on_moved(self, event: FileMovedEvent):
        if event.is_directory:
            if self.atime_watcher:
                self.atime_watcher.update_watchlist_for_dir(os.path.dirname(event.src_path))
                self.atime_watcher.update_watchlist_for_dir(os.path.dirname(event.dest_path))
            return
        extra = {"event": "moved", "src": event.src_path, "dest": event.dest_path}
        _emit("moved", event.dest_path, extra)


# -------------------------
# Entrypoint
# -------------------------

def start_monitoring():
    cfg = _settings()
    paths = cfg.get("paths", [])
    if not isinstance(paths, list):
        paths = [paths]
    if not paths:
        log_event("No paths configured in settings.yaml under 'paths'. Nothing to monitor.", "ERROR")
        return

    atime_watcher = AtimeWatcher(paths, interval=1.0)
    atime_watcher.start()

    observer = Observer()
    handler = HoneyFileHandler(atime_watcher)

    for p in paths:
        observer.schedule(handler, p, recursive=False)
        log_event(f"Monitoring started on {os.path.abspath(p)}", "INFO")

    observer.start()
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        atime_watcher.stop()
        observer.stop()
        observer.join()
