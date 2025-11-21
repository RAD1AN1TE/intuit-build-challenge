import csv
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


def load_sales_data(csv_path: str = None) -> List[Dict[str, Any]]:
    """Load sales data from CSV file using functional programming approach."""
    if csv_path is None:
        csv_path = Path(__file__).parent / "data" / "sales_data.csv"
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        parsed = _parse_record(reader)
        filtered = _filter_valid_records(parsed)
        return list(filtered)


def _parse_record(reader) -> map:
    """Parse CSV records, converting types and dates. Returns None for invalid records."""
    def parse(row: Dict[str, str]) -> Dict[str, Any] | None:
        try:
            return {
                'date': datetime.strptime(row['date'], '%Y-%m-%d').date(),
                'region': row['region'],
                'category': row['category'],
                'product': row['product'],
                'quantity': int(row['quantity']),
                'unit_price': float(row['unit_price']),
                'amount': float(row['amount'])
            }
        except (ValueError, KeyError):
            return None
    return map(parse, reader)


def _filter_valid_records(records) -> filter:
    """Filter out invalid records (None from parsing errors, negative amounts, zero quantities, etc.)."""
    return filter(lambda r: r is not None and r['amount'] > 0 and r['quantity'] > 0, records)

