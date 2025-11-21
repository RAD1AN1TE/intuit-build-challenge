import pytest
from datetime import date
from assignment_2.csv_analyzer import (
    total_sales,
    sales_by_region,
    sales_by_category,
    top_products,
    average_sale_amount,
    monthly_sales_trend
)


class TestCSVAnalyzer:
    """Test suite for CSV analysis functions."""
    
    @pytest.fixture
    def sample_records(self):
        """Sample sales records for testing."""
        return [
            {
                'date': date(2024, 1, 15),
                'region': 'North',
                'category': 'Electronics',
                'product': 'Laptop',
                'quantity': 2,
                'unit_price': 999.99,
                'amount': 1999.98
            },
            {
                'date': date(2024, 1, 20),
                'region': 'South',
                'category': 'Clothing',
                'product': 'T-Shirt',
                'quantity': 10,
                'unit_price': 19.99,
                'amount': 199.90
            },
            {
                'date': date(2024, 2, 10),
                'region': 'North',
                'category': 'Clothing',
                'product': 'Jacket',
                'quantity': 3,
                'unit_price': 89.99,
                'amount': 269.97
            },
            {
                'date': date(2024, 2, 15),
                'region': 'South',
                'category': 'Electronics',
                'product': 'Tablet',
                'quantity': 4,
                'unit_price': 399.99,
                'amount': 1599.96
            }
        ]
    
    def test_total_sales(self, sample_records):
        """Test total sales calculation."""
        total = total_sales(sample_records)
        expected = 1999.98 + 199.90 + 269.97 + 1599.96
        assert abs(total - expected) < 0.01
    
    def test_total_sales_empty(self):
        """Test total sales with empty records."""
        assert total_sales([]) == 0.0
    
    def test_sales_by_region(self, sample_records):
        """Test sales grouping by region."""
        region_sales = sales_by_region(sample_records)
        
        assert 'North' in region_sales
        assert 'South' in region_sales
        assert abs(region_sales['North'] - (1999.98 + 269.97)) < 0.01
        assert abs(region_sales['South'] - (199.90 + 1599.96)) < 0.01
    
    def test_sales_by_category(self, sample_records):
        """Test sales grouping by category."""
        category_sales = sales_by_category(sample_records)
        
        assert 'Electronics' in category_sales
        assert 'Clothing' in category_sales
        assert abs(category_sales['Electronics'] - (1999.98 + 1599.96)) < 0.01
        assert abs(category_sales['Clothing'] - (199.90 + 269.97)) < 0.01
    
    def test_top_products(self, sample_records):
        """Test top products by sales."""
        top = top_products(sample_records, n=2)
        
        assert len(top) == 2
        assert top[0][0] == 'Laptop'  # Highest sales
        assert top[1][0] == 'Tablet'   # Second highest
    
    def test_top_products_more_than_available(self, sample_records):
        """Test top products when requesting more than available."""
        top = top_products(sample_records, n=10)
        
        assert len(top) == 4  # Only 4 unique products
    
    def test_average_sale_amount(self, sample_records):
        """Test average sale amount calculation."""
        avg = average_sale_amount(sample_records)
        expected = (1999.98 + 199.90 + 269.97 + 1599.96) / 4
        assert abs(avg - expected) < 0.01
    
    def test_average_sale_amount_empty(self):
        """Test average sale amount with empty records."""
        assert average_sale_amount([]) == 0.0
    
    def test_monthly_sales_trend(self, sample_records):
        """Test monthly sales trend calculation."""
        monthly = monthly_sales_trend(sample_records)
        
        assert '2024-01' in monthly
        assert '2024-02' in monthly
        assert abs(monthly['2024-01'] - (1999.98 + 199.90)) < 0.01
        assert abs(monthly['2024-02'] - (269.97 + 1599.96)) < 0.01
    
    def test_monthly_sales_trend_sorted(self, sample_records):
        """Test that monthly trend is sorted by month."""
        monthly = monthly_sales_trend(sample_records)
        months = list(monthly.keys())
        
        assert months == sorted(months)


class TestCSVAnalyzerIntegration:
    """Integration tests with real data."""
    
    def test_all_analyses_with_real_data(self):
        """Test all analysis functions with real CSV data."""
        from assignment_2.data_loader import load_sales_data
        records = load_sales_data()
        
        total = total_sales(records)
        assert total > 0
        
        region_sales = sales_by_region(records)
        assert len(region_sales) > 0
        
        category_sales = sales_by_category(records)
        assert len(category_sales) > 0
        
        top = top_products(records, n=5)
        assert len(top) > 0
        
        avg = average_sale_amount(records)
        assert avg > 0
        
        monthly = monthly_sales_trend(records)
        assert len(monthly) > 0

