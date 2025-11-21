import threading
import time
from assignment_1.blocking_queue import BoundedBlockingQueue
from assignment_1.producer_consumer import Producer, Consumer


def main():
    """Run producer-consumer demo with configured queue capacity and data volume.
    
    Demonstrates concurrent data transfer between producer and consumer threads
    using a bounded blocking queue. Prints summary of items transferred and timing.
    """
    line_width = 60
    
    print("=" * line_width)
    print("Assignment 1: Producer-Consumer Pattern with Thread Synchronization")
    print("=" * line_width)
    print()
    
    # Configuration: small queue capacity to demonstrate blocking behavior
    queue_capacity = 3
    source_data = list(range(1, 121))  # 120 items to process
    
    print(f"Queue capacity: {queue_capacity}")
    print(f"Source data: {source_data[:10]}... (showing first 10 of {len(source_data)} items)")
    print()
    
    queue = BoundedBlockingQueue(capacity=queue_capacity)
    destination = []
    destination_lock = threading.Lock()
    
    producer = Producer(source_data=source_data, queue=queue, name="Producer-1")
    consumer = Consumer(queue=queue, destination=destination, 
                       destination_lock=destination_lock, name="Consumer-1")
    
    print("Starting producer and consumer threads...")
    print("-" * line_width)
    
    start_time = time.time()
    
    producer.start()
    consumer.start()
    
    producer.join()
    consumer.join()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("-" * line_width)
    print()
    print("=" * line_width)
    print("Results:")
    print("=" * line_width)
    print(f"Source items:      {len(source_data)}")
    print(f"Destination items: {len(destination)}")
    print(f"Items produced:    {producer.items_produced}")
    print(f"Items consumed:   {consumer.items_consumed}")
    print(f"Execution time:    {elapsed_time:.3f} seconds")
    print()
    print(f"Source data:       {source_data[:10]}... (showing first 10 of {len(source_data)} items)")
    print(f"Destination data:  {destination[:10]}... (showing first 10 of {len(destination)} items)")
    print()
    
    if destination == source_data:
        print("SUCCESS: All items transferred correctly!")
    else:
        print("ERROR: Data mismatch detected!")
        print(f"  Missing items: {set(source_data) - set(destination)}")
        print(f"  Extra items: {set(destination) - set(source_data)}")
    
    print("=" * line_width)


if __name__ == "__main__":
    main()

