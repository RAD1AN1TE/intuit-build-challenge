# Assignment 2: CSV Data Analysis

Implementation of CSV data analysis using functional programming with streams, lambda expressions, and data aggregation.

## Dataset Selection and Construction

**File**: `data/sales_data.csv`

**Dataset Choice**: A custom-constructed sales transaction dataset was created to demonstrate functional programming analysis capabilities.

**Description**: The dataset contains 60 sales transaction records spanning 12 months (January-December 2024), with data distributed across multiple regions, product categories, and time periods.

**Column Definitions**:
- `date`: Transaction date in `YYYY-MM-DD` format (e.g., "2024-01-15")
- `region`: Sales region - one of: North, South, East, West
- `category`: Product category - one of: Electronics, Clothing, Food
- `product`: Product name (e.g., "Laptop", "T-Shirt", "Coffee")
- `quantity`: Number of units sold (positive integer)
- `unit_price`: Price per unit in dollars (positive float)
- `amount`: Total transaction amount in dollars (positive float, calculated as quantity × unit_price)

**Dataset Assumptions and Validation Rules**:
1. **Date Format**: All dates must be in `YYYY-MM-DD` format. Invalid date formats are filtered out during parsing.
2. **Numeric Fields**: All numeric fields (`quantity`, `unit_price`, `amount`) must be valid numbers. Non-numeric values cause the record to be filtered out.
3. **Data Validity**: Records with zero or negative `quantity` or `amount` values are considered invalid and are automatically filtered out.
4. **Data Completeness**: All required columns must be present. Missing columns cause parsing errors and record filtering.
5. **Temporal Coverage**: The dataset represents a complete calendar year (2024) with transactions distributed across all 12 months.
6. **Dimensionality**: The dataset includes multiple grouping dimensions (region, category, product, time) to enable comprehensive aggregation analysis.

**Rationale for Dataset Selection**:
- **Volume**: 60 records provide sufficient data for meaningful aggregation while remaining manageable for analysis
- **Multi-dimensional**: Includes region, category, product, and time dimensions enabling various grouping operations
- **Realistic Patterns**: Contains realistic sales patterns including seasonal trends, product variety, and regional distribution
- **Functional Programming Fit**: Structure supports demonstration of `map`, `filter`, `reduce`, and lambda expressions
- **Error Handling**: Includes edge cases (some records may be filtered) to demonstrate robust data processing

## Files

- **`data_loader.py`**: Loads CSV data using functional programming with `map` and `filter` operations. Handles parsing errors gracefully by filtering out malformed records
- **`csv_analyzer.py`**: Analysis functions using functional programming (total sales, sales by region/category, top products, average, monthly trend)
- **`run_assignment_2.py`**: Demo script that runs all analyses and prints results
- **`data/sales_data.csv`**: Sample sales dataset with 60 records
- **`tests/`**: Unit tests for data loading and analysis functions

## Running

Run from project root:

```bash
python -m assignment_2.run_assignment_2
```

**Sample Output**:

```
======================================================================
Assignment 2: CSV Data Analysis with Functional Programming
======================================================================

Loading sales data from CSV...
Loaded 58 sales records

----------------------------------------------------------------------
1. Total Sales
----------------------------------------------------------------------
Total Sales Amount: $52,363.21

----------------------------------------------------------------------
2. Sales by Region
----------------------------------------------------------------------
  North     : $   18,912.35
  South     : $   12,477.03
  East      : $   10,698.45
  West      : $   10,275.38

----------------------------------------------------------------------
3. Sales by Category
----------------------------------------------------------------------
  Electronics : $   38,949.19
  Clothing    : $    9,002.62
  Food        : $    4,411.40

----------------------------------------------------------------------
4. Top 5 Products by Sales
----------------------------------------------------------------------
  1. Laptop         : $   16,999.83
  2. Smartphone     : $   11,899.83
  3. Headphones     : $    5,249.65
  4. Tablet         : $    4,799.88
  5. Jeans          : $    2,599.48

----------------------------------------------------------------------
5. Average Sale Amount
----------------------------------------------------------------------
Average Sale Amount: $902.81

----------------------------------------------------------------------
6. Monthly Sales Trend
----------------------------------------------------------------------
  2024-01: $    5,949.33
  2024-02: $    2,648.87
  2024-03: $    3,054.24
  2024-04: $    3,699.20
  2024-05: $    4,523.58
  2024-06: $    3,149.44
  2024-07: $    5,843.15
  2024-08: $    4,046.36
  2024-09: $    3,784.14
  2024-10: $    5,087.95
  2024-11: $    2,348.54
  2024-12: $    8,228.41

======================================================================
Analysis Complete!
======================================================================
```

For setup and test commands, see root README.

## Test Coverage

Run tests with coverage:

```bash
python -m pytest assignment_2/tests/ --cov=assignment_2 --cov-config=assignment_2/.coveragerc --cov-report=term-missing
```

**Coverage Results**:
- `csv_analyzer.py`: 100% coverage (31 statements)
- `data_loader.py`: 100% coverage (21 statements)
- **Total**: 100% coverage (52 statements, 17 tests)

## Design Decisions

1. **Functional Programming**: All operations use `map`, `filter`, `reduce`, and lambda expressions. No imperative loops in core logic.
2. **Error Handling**: Parsing errors (malformed dates, non-numeric values) are caught and invalid records are filtered out, ensuring robust data processing.
3. **Performance**: Grouping operations use single-pass O(n) aggregation with `reduce`, mutating the accumulator in place to avoid O(n²) dictionary copying overhead.
4. **Stream Operations**: Data flows through a pipeline of transformations (map → filter) before final aggregation.
