# Scheduler service for running periodic tasks.

import logging
import threading
import time
from datetime import datetime
from typing import Callable

logger = logging.getLogger(__name__)


class Scheduler:
    # Simple task scheduler for periodic operations.
    
    def __init__(self):
        self.tasks = []
        self.running = False
        self.thread = None
    
    def add_task(self, func: Callable, interval_seconds: int, name: str):
        task = {
            "func": func,
            "interval": interval_seconds,
            "name": name,
            "last_run": None
        }
        self.tasks.append(task)
        logger.info(f"Task '{name}' scheduled every {interval_seconds}s")
    
    def start(self):
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("Scheduler started")
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Scheduler stopped")
    
    def _run(self):
        while self.running:
            now = time.time()
            
            for task in self.tasks:
                should_run = (
                    task["last_run"] is None or
                    now - task["last_run"] >= task["interval"]
                )
                
                if should_run:
                    try:
                        logger.debug(f"Running task: {task['name']}")
                        task["func"]()
                        task["last_run"] = now
                    except Exception as e:
                        logger.error(f"Task '{task['name']}' failed: {e}")
            
            time.sleep(1)



