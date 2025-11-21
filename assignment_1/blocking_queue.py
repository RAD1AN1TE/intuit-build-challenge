import threading
from collections import deque
from typing import Any


class BoundedBlockingQueue:
    """Thread-safe blocking queue that blocks when full or empty."""
    
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        
        self.capacity = capacity
        self.queue = deque()
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
    
    def put(self, item: Any) -> None:
        """Add item to queue. Blocks if queue is full."""
        with self.not_full:
            while len(self.queue) >= self.capacity:
                self.not_full.wait()
            self.queue.append(item)
            self.not_empty.notify()
    
    def get(self) -> Any:
        """Remove and return item from queue. Blocks if queue is empty."""
        with self.not_empty:
            while not self.queue:
                self.not_empty.wait()
            item = self.queue.popleft()
            self.not_full.notify()
            return item
    
    def __repr__(self) -> str:
        """String representation of the queue."""
        with self.lock:
            return f"BoundedBlockingQueue(capacity={self.capacity}, size={len(self.queue)})"

