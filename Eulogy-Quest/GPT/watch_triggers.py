#!/usr/bin/env python3
#
# This file: akk-stack/Eulogy-Quest/GPT/watch_triggers.py
# also note: Eulogy-quest's .venv is at Eulogy-quest/
# (watchdog is installed in the .venv)
#
# ai-gen start (ChatGPT-4o-mini-high, 0)
#
import time
import logging
from queue import Queue, Full
from threading import Thread
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import subprocess
import os
from pathlib import Path

# ───── Configuration ─────
# locate this script, then walk back up to the akk-stack root
SCRIPT_PATH    = Path(__file__).resolve()
GPT_DIR        = SCRIPT_PATH.parent            # .../Eulogy-Quest/GPT
AKK_STACK_ROOT = GPT_DIR.parent.parent         # .../akk-stack

# where the EQEmu quest files actually live
QUEST_DIR      = AKK_STACK_ROOT / "server" / "quests"
WATCH_DIR      = QUEST_DIR / "tutorialb"

# create-quest.py lives next to this watcher
QUEST_SCRIPT   = GPT_DIR / "create-quest.py"
QUEUE_MAXSIZE  = 5
COOLDOWN_SEC   = 20
# ─────────────────────────

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Timestamp of the last run
last_run_time = 0

def extract_name(trigger_path):
    """Extract 'First Last' from 'Eulogyquest_First_Last.trigger'."""
    filename = os.path.basename(trigger_path)
    core = filename[len("Eulogyquest_"):-len(".trigger")]
    return core.replace("_", " ")

def run_quest_script(name):
    """Invoke your quest-creation script with the given name."""
    result = subprocess.run(
        ["python3", QUEST_SCRIPT, name],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        logging.error("Quest script failed: %s", result.stderr.strip())
        return False
    logging.info("Quest script succeeded: %s", result.stdout.strip())
    return True

def cleanup_trigger(trigger_path):
    """Delete the trigger file after successful processing."""
    try:
        os.remove(trigger_path)
        logging.info("Removed trigger file %s", trigger_path)
    except Exception as e:
        logging.warning("Could not remove trigger file %s: %s", trigger_path, e)

def worker_loop(q):
    """Worker thread: dequeues triggers, applies cooldown, runs quests."""
    global last_run_time
    while True:
        trigger_path = q.get()
        now = time.time()
        elapsed = now - last_run_time
        if elapsed < COOLDOWN_SEC:
            wait = COOLDOWN_SEC - elapsed
            logging.info("Cooldown active—waiting %.1f seconds", wait)
            time.sleep(wait)

        name = extract_name(trigger_path)
        logging.info("Starting quest-generation for '%s'", name)
        success = run_quest_script(name)
        if success:
            cleanup_trigger(trigger_path)
        last_run_time = time.time()
        q.task_done()

class TriggerHandler(PatternMatchingEventHandler):
    """Watchdog handler: enqueues new/modified/moved trigger files."""
    def __init__(self, q):
        super().__init__(patterns=["*Eulogyquest_*.trigger"], ignore_directories=True)
        self.q = q

    def on_created(self, event):
        self.enqueue(event.src_path)

    def on_modified(self, event):
        self.enqueue(event.src_path)

    def on_moved(self, event):
        if event.dest_path.endswith(".trigger"):
            self.enqueue(event.dest_path)

    def enqueue(self, path):
        logging.info("Handler invoked for path: %s", path)
        try:
            self.q.put_nowait(path)
            logging.info("Enqueued trigger %s", path)
        except Full:
            logging.warning("Queue full—dropping trigger %s", path)

def main():
    q = Queue(maxsize=QUEUE_MAXSIZE)
    Thread(target=worker_loop, args=(q,), daemon=True).start()

    observer = Observer()
    observer.schedule(TriggerHandler(q), WATCH_DIR, recursive=False)
    
    logging.info(f"Watching for triggers in: {WATCH_DIR}")
    logging.info(f"Quest script at:         {QUEST_SCRIPT}")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()

# ai-gen end