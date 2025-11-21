import threading
import time
from assignment_1.blocking_queue import BoundedBlockingQueue
from assignment_1.producer_consumer import Producer, Consumer, _SENTINEL


class TestProducer:
    """Test suite for Producer class."""
    
    def test_producer_creates_items(self):
        """Test that producer successfully creates items."""
        queue = BoundedBlockingQueue(capacity=10)
        source_data = [1, 2, 3, 4, 5]
        
        producer = Producer(source_data=source_data, queue=queue)
        producer.start()
        producer.join(timeout=5.0)
        
        assert producer.items_produced == len(source_data)
        # Verify all items and sentinel are in queue
        items = []
        for _ in range(len(source_data) + 1):
            items.append(queue.get())
        assert len(items) == len(source_data) + 1
    
    def test_producer_handles_empty_source(self):
        """Test producer with empty source."""
        queue = BoundedBlockingQueue(capacity=5)
        source_data = []
        
        producer = Producer(source_data=source_data, queue=queue)
        producer.start()
        producer.join(timeout=5.0)
        
        assert producer.items_produced == 0
        # Should only have sentinel
        item = queue.get()
        assert item is _SENTINEL
    
    def test_producer_error_handling(self):
        """Test producer error handling."""
        # Create a queue that will cause an error scenario
        queue = BoundedBlockingQueue(capacity=1)
        
        # Create a producer with data that might cause issues
        # We'll simulate an error by using a custom iterable that raises
        class ErrorSource:
            def __init__(self):
                self.count = 0
            
            def __iter__(self):
                return self
            
            def __next__(self):
                self.count += 1
                if self.count == 1:
                    return 1
                elif self.count == 2:
                    raise ValueError("Simulated error")
                raise StopIteration
        
        source_data = ErrorSource()
        producer = Producer(source_data=source_data, queue=queue)
        producer.start()
        producer.join(timeout=5.0)
        
        # Producer should handle error and put sentinel
        item = queue.get()
        assert item == 1  # First item should be produced
        sentinel = queue.get()
        assert sentinel is _SENTINEL  # Sentinel should be put even on error
    
    def test_producer_error_with_queue_failure(self):
        """Test producer error handling when queue.put also fails."""
        # Create a mock queue that fails on put
        class FailingQueue:
            def put(self, item):
                raise RuntimeError("Queue put failed")
        
        queue = FailingQueue()
        source_data = [1, 2, 3]
        
        # This will trigger the inner except block (lines 60-61)
        producer = Producer(source_data=source_data, queue=queue)
        producer.start()
        producer.join(timeout=5.0)
        
        # Producer should handle the error gracefully
        assert producer.items_produced == 0  # No items produced due to queue failure
    


class TestConsumer:
    """Test suite for Consumer class."""
    
    def test_consumer_processes_items(self):
        """Test that consumer successfully processes items."""
        queue = BoundedBlockingQueue(capacity=10)
        destination = []
        lock = threading.Lock()
        
        # Put items in queue
        for i in range(5):
            queue.put(i)
        queue.put(_SENTINEL)
        
        consumer = Consumer(queue=queue, destination=destination, 
                          destination_lock=lock)
        consumer.start()
        consumer.join(timeout=5.0)
        
        assert consumer.items_consumed == 5
        assert sorted(destination) == [0, 1, 2, 3, 4]
    
    def test_consumer_handles_empty_queue(self):
        """Test consumer behavior with empty queue (should block)."""
        queue = BoundedBlockingQueue(capacity=5)
        destination = []
        lock = threading.Lock()
        
        consumer = Consumer(queue=queue, destination=destination,
                          destination_lock=lock)
        consumer.start()
        
        # Consumer should be waiting
        time.sleep(0.1)
        assert consumer.is_alive()
        assert len(destination) == 0
        
        # Add item and sentinel
        queue.put(42)
        queue.put(_SENTINEL)
        
        consumer.join(timeout=1.0)
        assert consumer.items_consumed == 1
        assert destination == [42]
    
    def test_consumer_thread_safe_destination(self):
        """Test that consumer uses lock for thread-safe destination access."""
        queue = BoundedBlockingQueue(capacity=10)
        destination = []
        lock = threading.Lock()
        
        # Fill queue with items and sentinel
        for i in range(5):
            queue.put(i)
        queue.put(_SENTINEL)
        
        consumer = Consumer(queue=queue, destination=destination,
                          destination_lock=lock)
        consumer.start()
        consumer.join(timeout=2.0)
        
        # Verify all items in destination
        assert len(destination) == 5
        assert sorted(destination) == list(range(5))
    
    def test_consumer_error_handling(self):
        """Test consumer error handling."""
        # Create a queue that will raise an error on get
        class FailingQueue:
            def get(self):
                raise RuntimeError("Queue get failed")
        
        queue = FailingQueue()
        destination = []
        lock = threading.Lock()
        
        # This will trigger the exception handler (lines 103-104)
        consumer = Consumer(queue=queue, destination=destination,
                          destination_lock=lock)
        consumer.start()
        consumer.join(timeout=5.0)
        
        # Consumer should handle the error gracefully
        assert consumer.items_consumed == 0
        assert len(destination) == 0
    


class TestProducerConsumerIntegration:
    """Integration tests for Producer and Consumer working together."""
    
    def test_basic_producer_consumer(self):
        """Test basic producer-consumer workflow."""
        queue = BoundedBlockingQueue(capacity=5)
        source_data = [1, 2, 3, 4, 5]
        destination = []
        lock = threading.Lock()
        
        producer = Producer(source_data=source_data, queue=queue)
        consumer = Consumer(queue=queue, destination=destination,
                          destination_lock=lock)
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=5.0)
        consumer.join(timeout=5.0)
        
        # Verify all items transferred
        assert producer.items_produced == len(source_data)
        assert consumer.items_consumed == len(source_data)
        assert sorted(destination) == sorted(source_data)
    
    def test_queue_blocking_behavior(self):
        """Test that queue properly blocks when full/empty."""
        queue = BoundedBlockingQueue(capacity=3)  # Small capacity
        source_data = list(range(10))  # More items than capacity
        destination = []
        lock = threading.Lock()
        
        producer = Producer(source_data, queue)
        consumer = Consumer(queue, destination, lock)
        
        # Start consumer first (will block waiting for items)
        consumer.start()
        time.sleep(0.1)
        
        # Start producer
        producer.start()
        
        producer.join(timeout=5.0)
        consumer.join(timeout=5.0)
        
        # Verify all items transferred despite small queue
        assert len(destination) == len(source_data)
        assert sorted(destination) == source_data
    
    def test_none_values_can_be_transported(self):
        """Test that None values can be transported as legitimate data."""
        queue = BoundedBlockingQueue(capacity=5)
        # Source data containing None values
        source_data = [1, None, 3, None, 5]
        destination = []
        lock = threading.Lock()
        
        producer = Producer(source_data=source_data, queue=queue)
        consumer = Consumer(queue=queue, destination=destination,
                          destination_lock=lock)
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=5.0)
        consumer.join(timeout=5.0)
        
        # Verify all items including None values are transferred
        assert len(destination) == len(source_data)
        assert destination == source_data  # Preserve order including None
        assert None in destination  # None values are present

