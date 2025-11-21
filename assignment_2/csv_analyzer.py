from typing import List, Dict, Any, Tuple
from functools import reduce


def total_sales(records: List[Dict[str, Any]]) -> float:
    """Calculate total sales amount."""
    return reduce(lambda acc, r: acc + r['amount'], records, 0.0)


def _group_by_field(records: List[Dict[str, Any]], field: str) -> Dict[str, float]:
    """Group sales by a field and calculate total for each value using functional programming."""
    def accumulate(acc: Dict[str, float], record: Dict[str, Any]) -> Dict[str, float]:
        key = record[field]
        acc[key] = acc.get(key, 0.0) + record['amount']
        return acc
    return reduce(accumulate, records, {})


def sales_by_region(records: List[Dict[str, Any]]) -> Dict[str, float]:
    """Group sales by region and calculate total for each region."""
    return _group_by_field(records, 'region')


def sales_by_category(records: List[Dict[str, Any]]) -> Dict[str, float]:
    """Group sales by category and calculate total for each category."""
    return _group_by_field(records, 'category')


def top_products(records: List[Dict[str, Any]], n: int = 5) -> List[Tuple[str, float]]:
    """Find top N products by total sales amount."""
    product_totals = _group_by_field(records, 'product')
    return sorted(product_totals.items(), key=lambda x: x[1], reverse=True)[:n]


def average_sale_amount(records: List[Dict[str, Any]]) -> float:
    """Calculate average sale amount."""
    if not records:
        return 0.0
    return total_sales(records) / len(records)


def monthly_sales_trend(records: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate monthly sales trend using functional programming."""
    def get_month_key(record: Dict[str, Any]) -> str:
        date_obj = record['date']
        return f"{date_obj.year}-{date_obj.month:02d}"
    
    def accumulate(acc: Dict[str, float], record: Dict[str, Any]) -> Dict[str, float]:
        key = get_month_key(record)
        acc[key] = acc.get(key, 0.0) + record['amount']
        return acc
    
    monthly_totals = reduce(accumulate, records, {})
    return dict(sorted(monthly_totals.items()))

