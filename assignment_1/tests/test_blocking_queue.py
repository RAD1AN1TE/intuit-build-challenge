import pytest
import threading
import time
from assignment_1.blocking_queue import BoundedBlockingQueue
from assignment_1.producer_consumer import _SENTINEL


class TestBoundedBlockingQueue:
    """Test suite for BoundedBlockingQueue basic operations."""
    
    def test_init_with_valid_capacity(self):
        """Test queue initialization with valid capacity."""
        queue = BoundedBlockingQueue(capacity=5)
        assert queue.capacity == 5
    
    def test_init_with_invalid_capacity(self):
        """Test queue initialization with invalid capacity."""
        with pytest.raises(ValueError):
            BoundedBlockingQueue(capacity=0)
        
        with pytest.raises(ValueError):
            BoundedBlockingQueue(capacity=-1)
    
    def test_put_and_get_single_item(self):
        """Test basic put and get operations."""
        queue = BoundedBlockingQueue(capacity=5)
        
        queue.put(42)
        item = queue.get()
        assert item == 42
    
    def test_put_and_get_multiple_items(self):
        """Test putting and getting multiple items."""
        queue = BoundedBlockingQueue(capacity=10)
        items = [1, 2, 3, 4, 5]
        
        for item in items:
            queue.put(item)
        
        retrieved = []
        for _ in range(len(items)):
            retrieved.append(queue.get())
        
        assert retrieved == items
    
    def test_fifo_ordering(self):
        """Test that queue maintains FIFO (First In First Out) order."""
        queue = BoundedBlockingQueue(capacity=10)
        
        for i in range(10):
            queue.put(i)
        
        for i in range(10):
            assert queue.get() == i
    
    def test_repr(self):
        """Test string representation of the queue."""
        queue = BoundedBlockingQueue(capacity=5)
        repr_str = repr(queue)
        assert "BoundedBlockingQueue" in repr_str
        assert "capacity=5" in repr_str
        
        queue.put(1)
        queue.put(2)
        repr_str = repr(queue)
        assert "size=2" in repr_str


class TestBlockingBehavior:
    """Test blocking behavior when queue is full or empty."""
    
    def test_blocking_when_full(self):
        """Test that put() blocks when queue is full."""
        queue = BoundedBlockingQueue(capacity=2)
        queue.put(1)
        queue.put(2)
        
        # Start a thread that tries to put when full
        put_completed = threading.Event()
        
        def put_item():
            queue.put(3)  # Should block until space available
            put_completed.set()
        
        thread = threading.Thread(target=put_item)
        thread.start()
        
        # Give thread time to start and block
        time.sleep(0.1)
        
        # Thread should still be running (blocked)
        assert thread.is_alive()
        assert not put_completed.is_set()
        
        # Make space available
        queue.get()
        
        # Thread should now complete
        thread.join(timeout=1.0)
        assert put_completed.is_set()
    
    def test_blocking_when_empty(self):
        """Test that get() blocks when queue is empty."""
        queue = BoundedBlockingQueue(capacity=5)
        
        # Start a thread that tries to get when empty
        item_retrieved = []
        get_completed = threading.Event()
        
        def get_item():
            item = queue.get()  # Should block until item available
            item_retrieved.append(item)
            get_completed.set()
        
        thread = threading.Thread(target=get_item)
        thread.start()
        
        # Give thread time to start and block
        time.sleep(0.1)
        
        # Thread should still be running (blocked)
        assert thread.is_alive()
        assert not get_completed.is_set()
        
        # Add item to queue
        queue.put(42)
        
        # Thread should now complete
        thread.join(timeout=1.0)
        assert get_completed.is_set()
        assert item_retrieved[0] == 42


class TestThreadSafety:
    """Test thread safety with multiple producers and consumers."""
    
    def test_multiple_producers(self):
        """Test multiple threads putting items concurrently."""
        queue = BoundedBlockingQueue(capacity=100)
        num_threads = 5
        items_per_thread = 20
        
        def producer(thread_id):
            for i in range(items_per_thread):
                queue.put(f"Thread-{thread_id}-Item-{i}")
        
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=producer, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verify all items can be retrieved
        retrieved = []
        for _ in range(num_threads * items_per_thread):
            retrieved.append(queue.get())
        
        assert len(retrieved) == num_threads * items_per_thread
    
    def test_multiple_consumers(self):
        """Test multiple threads getting items concurrently."""
        queue = BoundedBlockingQueue(capacity=100)
        num_items = 50
        num_consumers = 5
        
        # Fill queue
        for i in range(num_items):
            queue.put(i)
        
        retrieved_items = []
        lock = threading.Lock()
        items_processed = 0
        items_lock = threading.Lock()
        
        def consumer():
            nonlocal items_processed
            while True:
                try:
                    item = queue.get()
                    if item is _SENTINEL:
                        break
                    with lock:
                        retrieved_items.append(item)
                    with items_lock:
                        items_processed += 1
                        if items_processed >= num_items:
                            # Requeue sentinel so remaining consumers can exit
                            for _ in range(num_consumers - 1):
                                queue.put(_SENTINEL)
                            break
                except Exception:
                    break
        
        threads = []
        for _ in range(num_consumers):
            thread = threading.Thread(target=consumer)
            threads.append(thread)
            thread.start()
        
        # Wait for all items to be processed
        for thread in threads:
            thread.join(timeout=5.0)
        
        # All items should be retrieved
        assert len(retrieved_items) == num_items
        assert sorted(retrieved_items) == list(range(num_items))
    
    def test_producer_consumer_concurrent(self):
        """Test producer and consumer working concurrently."""
        queue = BoundedBlockingQueue(capacity=10)
        source_items = list(range(100))
        consumed_items = []
        lock = threading.Lock()
        
        def producer():
            for item in source_items:
                queue.put(item)
            queue.put(_SENTINEL)
        
        def consumer():
            while True:
                item = queue.get()
                if item is _SENTINEL:
                    # Requeue sentinel for other potential consumers
                    queue.put(_SENTINEL)
                    break
                with lock:
                    consumed_items.append(item)
        
        prod_thread = threading.Thread(target=producer)
        cons_thread = threading.Thread(target=consumer)
        
        prod_thread.start()
        cons_thread.start()
        
        prod_thread.join()
        cons_thread.join()
        
        # Verify all items consumed
        assert len(consumed_items) == len(source_items)
        assert sorted(consumed_items) == source_items
    
    def test_no_data_loss(self):
        """Test that no data is lost with concurrent operations."""
        queue = BoundedBlockingQueue(capacity=5)
        num_producers = 3
        items_per_producer = 50
        total_items = num_producers * items_per_producer
        
        consumed_items = []
        lock = threading.Lock()
        items_processed = 0
        items_lock = threading.Lock()
        
        def producer(producer_id):
            for i in range(items_per_producer):
                queue.put((producer_id, i))
        
        def consumer():
            nonlocal items_processed
            while True:
                item = queue.get()
                if item is _SENTINEL:
                    break
                with lock:
                    consumed_items.append(item)
                with items_lock:
                    items_processed += 1
                    if items_processed >= total_items:
                        queue.put(_SENTINEL)
                        break
        
        # Start producers
        prod_threads = []
        for i in range(num_producers):
            thread = threading.Thread(target=producer, args=(i,))
            prod_threads.append(thread)
            thread.start()
        
        # Start consumer
        cons_thread = threading.Thread(target=consumer)
        cons_thread.start()
        
        # Wait for completion
        for thread in prod_threads:
            thread.join()
        cons_thread.join(timeout=10.0)
        
        # Verify no data loss
        assert len(consumed_items) == total_items

