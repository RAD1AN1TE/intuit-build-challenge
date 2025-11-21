# Assignment 1: Producer-Consumer Pattern

Implementation of a producer-consumer pattern with thread synchronization using blocking queues.

## Files

- **`blocking_queue.py`**: Implements `BoundedBlockingQueue` - thread-safe blocking queue using `threading.Condition` for wait/notify mechanism
- **`producer_consumer.py`**: Implements `Producer` and `Consumer` thread classes with sentinel pattern for shutdown signaling
- **`run_assignment_1.py`**: Demo script that runs the producer-consumer simulation
- **`tests/`**: Unit and integration tests for all components

## Running

Run from project root:

```bash
python -m assignment_1.run_assignment_1
```

**Sample Output**:

```
============================================================
Assignment 1: Producer-Consumer Pattern with Thread Synchronization
============================================================

Queue capacity: 3
Source data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]... (showing first 10 of 120 items)

Starting producer and consumer threads...
------------------------------------------------------------
[Producer-1] Produced: 1
[Producer-1] Produced: 2
[Producer-1] Produced: 3
[Consumer-1] Consumed: 1
[Producer-1] Produced: 4
[Consumer-1] Consumed: 2
[Producer-1] Produced: 5
[Consumer-1] Consumed: 3
[Producer-1] Produced: 6
[Producer-1] Produced: 7
[Consumer-1] Consumed: 4
[Consumer-1] Consumed: 5
... (interleaved producer/consumer activity) ...
[Producer-1] Finished producing 120 items
[Consumer-1] Finished consuming 120 items
------------------------------------------------------------

============================================================
Results:
============================================================
Source items:      120
Destination items: 120
Items produced:    120
Items consumed:   120
Execution time:    0.045 seconds

Source data:       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]... (showing first 10 of 120 items)
Destination data:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]... (showing first 10 of 120 items)

SUCCESS: All items transferred correctly!
============================================================
```

For setup and test commands, see root README.

## Test Coverage

Run tests with coverage:

```bash
python -m pytest assignment_1/tests/ --cov=assignment_1 --cov-config=assignment_1/.coveragerc --cov-report=term-missing
```

**Coverage Results**:
- `blocking_queue.py`: 100% coverage (25 statements)
- `producer_consumer.py`: 100% coverage (50 statements)
- **Total**: 100% coverage (75 statements, 29 tests)

## Design Decisions

1. **Custom BoundedBlockingQueue**: Implemented from scratch to demonstrate wait/notify mechanism
2. **Sentinel Pattern**: Uses private `_SENTINEL` object to signal completion
3. **Thread Safety**: Uses locks and conditions for synchronization
