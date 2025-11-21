from assignment_2.data_loader import load_sales_data
from assignment_2.csv_analyzer import (
    total_sales,
    sales_by_region,
    sales_by_category,
    top_products,
    average_sale_amount,
    monthly_sales_trend
)


def main():
    """Run CSV data analysis demo demonstrating functional programming."""
    line_width = 70
    
    print("=" * line_width)
    print("Assignment 2: CSV Data Analysis with Functional Programming")
    print("=" * line_width)
    print()
    
    # Load data
    print("Loading sales data from CSV...")
    records = load_sales_data()
    print(f"Loaded {len(records)} sales records")
    print()
    
    # Analysis 1: Total Sales
    print("-" * line_width)
    print("1. Total Sales")
    print("-" * line_width)
    total = total_sales(records)
    print(f"Total Sales Amount: ${total:,.2f}")
    print()
    
    # Analysis 2: Sales by Region
    print("-" * line_width)
    print("2. Sales by Region")
    print("-" * line_width)
    region_sales = sales_by_region(records)
    for region, amount in sorted(region_sales.items(), key=lambda x: x[1], reverse=True):
        amount_str = f"${amount:,.2f}"
        print(f"  {region:10s}: {amount_str:>13s}")
    print()
    
    # Analysis 3: Sales by Category
    print("-" * line_width)
    print("3. Sales by Category")
    print("-" * line_width)
    category_sales = sales_by_category(records)
    for category, amount in sorted(category_sales.items(), key=lambda x: x[1], reverse=True):
        amount_str = f"${amount:,.2f}"
        print(f"  {category:12s}: {amount_str:>13s}")
    print()
    
    # Analysis 4: Top Products
    print("-" * line_width)
    print("4. Top 5 Products by Sales")
    print("-" * line_width)
    top = top_products(records, n=5)
    for i, (product, amount) in enumerate(top, 1):
        amount_str = f"${amount:,.2f}"
        print(f"  {i}. {product:15s}: {amount_str:>13s}")
    print()
    
    # Analysis 5: Average Sale Amount
    print("-" * line_width)
    print("5. Average Sale Amount")
    print("-" * line_width)
    avg = average_sale_amount(records)
    amount_str = f"${avg:,.2f}"
    print(f"Average Sale Amount: {amount_str:>13s}")
    print()
    
    # Analysis 6: Monthly Sales Trend
    print("-" * line_width)
    print("6. Monthly Sales Trend")
    print("-" * line_width)
    monthly = monthly_sales_trend(records)
    for month, amount in monthly.items():
        amount_str = f"${amount:,.2f}"
        print(f"  {month:8s}: {amount_str:>13s}")
    print()
    
    print("=" * line_width)
    print("Analysis Complete!")
    print("=" * line_width)


if __name__ == "__main__":
    main()

