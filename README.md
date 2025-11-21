# Intuit Build Challenge

Implementation of two coding assignments demonstrating concurrent programming and functional data analysis.

## Setup

```bash
pip install -r requirements.txt
```

Or install dependencies individually:
```bash
pip install pytest pytest-cov
```

## Running Assignments

```bash
# Assignment 1: Producer-Consumer Pattern
python -m assignment_1.run_assignment_1

# Assignment 2: CSV Data Analysis
python -m assignment_2.run_assignment_2
```

## Running Tests

```bash
# All tests
python -m pytest assignment_1/tests/ assignment_2/tests/ -v

# With coverage
python -m pytest assignment_1/tests/ --cov=assignment_1 --cov-config=assignment_1/.coveragerc --cov-report=term-missing
python -m pytest assignment_2/tests/ --cov=assignment_2 --cov-config=assignment_2/.coveragerc --cov-report=term-missing
```

**Test Coverage Summary**:
- **Assignment 1**: 100% coverage (75 statements, 29 tests)
  - `blocking_queue.py`: 100%
  - `producer_consumer.py`: 100%
- **Assignment 2**: 100% coverage (52 statements, 17 tests)
  - `csv_analyzer.py`: 100%
  - `data_loader.py`: 100%

## Project Structure

```
intuit-build-challenge/
├── assignment_1/          # Producer-Consumer Pattern
│   ├── blocking_queue.py
│   ├── producer_consumer.py
│   ├── run_assignment_1.py
│   └── tests/
├── assignment_2/          # CSV Data Analysis
│   ├── data_loader.py
│   ├── csv_analyzer.py
│   ├── run_assignment_2.py
│   ├── data/
│   └── tests/
├── requirements.txt       # Python dependencies
└── README.md
```

For detailed documentation, see each assignment's README.

