import threading
import sys
from typing import List, Any, Optional
from assignment_1.blocking_queue import BoundedBlockingQueue

_print_lock = threading.Lock()
_SENTINEL = object()  # Private sentinel token placed in queue to signal shutdown


def thread_safe_print(*args, **kwargs):
    """Thread-safe print to prevent output interleaving."""
    with _print_lock:
        print(*args, **kwargs)
        sys.stdout.flush()


class Producer(threading.Thread):
    """Producer thread that places items from source into queue.
    
    Signals completion by enqueueing _SENTINEL after all data items.
    """
    
    def __init__(self, source_data: List[Any], queue: BoundedBlockingQueue, 
                 name: Optional[str] = None):
        super().__init__(name=name or "Producer")
        self.source_data = source_data
        self.queue = queue
        self.items_produced = 0
    
    def run(self) -> None:
        """Execute producer thread logic."""
        try:
            for item in self.source_data:
                self.queue.put(item)
                self.items_produced += 1
                thread_safe_print(f"[{self.name}] Produced: {item}")
            
            self.queue.put(_SENTINEL)  # Signal completion
            thread_safe_print(f"[{self.name}] Finished producing {self.items_produced} items")
            
        except Exception as e:
            thread_safe_print(f"[{self.name}] Error in producer: {e}")
            try:
                self.queue.put(_SENTINEL)
            except Exception:
                pass


class Consumer(threading.Thread):
    """Consumer thread that reads items from queue and stores in destination.
    
    Exits when _SENTINEL is dequeued, indicating producer completion.
    """
    
    def __init__(self, queue: BoundedBlockingQueue, destination: List[Any],
                 destination_lock: threading.Lock, name: Optional[str] = None):
        super().__init__(name=name or "Consumer")
        self.queue = queue
        self.destination = destination
        self.destination_lock = destination_lock
        self.items_consumed = 0
    
    def run(self) -> None:
        """Execute consumer thread logic."""
        try:
            while True:
                item = self.queue.get()
                if item is _SENTINEL:  # Shutdown signal received
                    break
                
                with self.destination_lock:
                    self.destination.append(item)
                
                self.items_consumed += 1
                thread_safe_print(f"[{self.name}] Consumed: {item}")
            
            thread_safe_print(f"[{self.name}] Finished consuming {self.items_consumed} items")
            
        except Exception as e:
            thread_safe_print(f"[{self.name}] Error in consumer: {e}")

