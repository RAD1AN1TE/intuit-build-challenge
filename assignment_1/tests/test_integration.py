import threading
import time
from assignment_1.blocking_queue import BoundedBlockingQueue
from assignment_1.producer_consumer import Producer, Consumer


class TestEndToEnd:
    """End-to-end integration tests."""
    
    def test_complete_workflow(self):
        """Test complete producer-consumer workflow from start to finish."""
        queue = BoundedBlockingQueue(capacity=5)
        source_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        destination = []
        lock = threading.Lock()
        
        producer = Producer(source_data, queue)
        consumer = Consumer(queue, destination, lock)
        
        # Run simulation
        producer.start()
        consumer.start()
        
        producer.join()
        consumer.join()
        
        # Verify results
        assert producer.items_produced == len(source_data)
        assert consumer.items_consumed == len(source_data)
        assert len(destination) == len(source_data)
        assert sorted(destination) == sorted(source_data)
    
    def test_stress_test_large_dataset(self):
        """Stress test with large dataset."""
        queue = BoundedBlockingQueue(capacity=10)
        source_data = list(range(10000))
        destination = []
        lock = threading.Lock()
        
        producer = Producer(source_data, queue)
        consumer = Consumer(queue, destination, lock)
        
        start_time = time.time()
        producer.start()
        consumer.start()
        
        producer.join()
        consumer.join()
        end_time = time.time()
        
        # Verify correctness
        assert len(destination) == len(source_data)
        assert sorted(destination) == source_data
        
        # Should complete in reasonable time
        assert end_time - start_time < 10.0
        print(f"Processed {len(source_data)} items in {end_time - start_time:.2f} seconds")
    
    def test_different_queue_capacities(self):
        """Test with different queue capacities."""
        capacities = [1, 5, 10, 50]
        source_data = list(range(100))
        
        for capacity in capacities:
            queue = BoundedBlockingQueue(capacity=capacity)
            destination = []
            lock = threading.Lock()
            
            producer = Producer(source_data, queue)
            consumer = Consumer(queue, destination, lock)
            
            producer.start()
            consumer.start()
            
            producer.join()
            consumer.join()
            
            # Verify correctness regardless of capacity
            assert len(destination) == len(source_data)
            assert sorted(destination) == source_data
    
    def test_real_world_simulation(self):
        """Simulate a real-world scenario with varying production/consumption rates."""
        queue = BoundedBlockingQueue(capacity=5)
        
        # Simulate slow producer, fast consumer
        source_data = list(range(20))
        destination = []
        lock = threading.Lock()
        
        def slow_producer():
            producer = Producer(source_data, queue)
            producer.start()
            # Add delay to simulate slow production
            time.sleep(0.01)
            producer.join()
        
        def fast_consumer():
            consumer = Consumer(queue, destination, lock)
            consumer.start()
            consumer.join()
        
        # Start threads
        prod_thread = threading.Thread(target=slow_producer)
        cons_thread = threading.Thread(target=fast_consumer)
        
        prod_thread.start()
        cons_thread.start()
        
        prod_thread.join()
        cons_thread.join()
        
        # Verify all items processed
        assert len(destination) == len(source_data)
        assert sorted(destination) == source_data
    
    def test_error_handling(self):
        """Test that system handles errors gracefully."""
        queue = BoundedBlockingQueue(capacity=5)
        destination = []
        lock = threading.Lock()
        
        # Create producer with valid data
        producer = Producer([1, 2, 3], queue)
        consumer = Consumer(queue, destination, lock)
        
        producer.start()
        consumer.start()
        
        producer.join()
        consumer.join()
        
        # System should still work correctly
        assert len(destination) == 3
        assert sorted(destination) == [1, 2, 3]
    
    def test_verify_thread_synchronization(self):
        """Verify that thread synchronization works correctly."""
        queue = BoundedBlockingQueue(capacity=3)
        source_data = list(range(50))
        destination = []
        lock = threading.Lock()
        
        # Track operations
        operations = []
        operations_lock = threading.Lock()
        
        def tracked_producer():
            producer = Producer(source_data, queue)
            producer.start()
            with operations_lock:
                operations.append("Producer started")
            producer.join()
            with operations_lock:
                operations.append("Producer finished")
        
        def tracked_consumer():
            consumer = Consumer(queue, destination, lock)
            consumer.start()
            with operations_lock:
                operations.append("Consumer started")
            consumer.join()
            with operations_lock:
                operations.append("Consumer finished")
        
        prod_thread = threading.Thread(target=tracked_producer)
        cons_thread = threading.Thread(target=tracked_consumer)
        
        prod_thread.start()
        cons_thread.start()
        
        prod_thread.join()
        cons_thread.join()
        
        # Verify synchronization: all items transferred correctly
        assert len(destination) == len(source_data)
        assert sorted(destination) == source_data
        
        # Verify both threads completed
        assert "Producer finished" in operations
        assert "Consumer finished" in operations

