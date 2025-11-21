import pytest
from pathlib import Path
from datetime import date
from assignment_2.data_loader import load_sales_data


class TestDataLoader:
    """Test suite for data loading functionality."""
    
    def test_load_sales_data_default_path(self):
        """Test loading data with default path."""
        records = load_sales_data()
        
        assert len(records) > 0
        assert isinstance(records, list)
        
        # Check first record structure
        first_record = records[0]
        assert 'date' in first_record
        assert 'region' in first_record
        assert 'category' in first_record
        assert 'product' in first_record
        assert 'quantity' in first_record
        assert 'unit_price' in first_record
        assert 'amount' in first_record
    
    def test_load_sales_data_custom_path(self, tmp_path):
        """Test loading data with custom path."""
        # Create test CSV
        csv_file = tmp_path / "test_sales.csv"
        csv_file.write_text(
            "date,region,category,product,quantity,unit_price,amount\n"
            "2024-01-15,North,Electronics,Laptop,2,999.99,1999.98\n"
        )
        
        records = load_sales_data(str(csv_file))
        
        assert len(records) == 1
        assert records[0]['product'] == 'Laptop'
        assert records[0]['amount'] == 1999.98
    
    def test_load_sales_data_type_conversion(self):
        """Test that data types are correctly converted."""
        records = load_sales_data()
        
        assert isinstance(records[0]['date'], date)
        assert isinstance(records[0]['quantity'], int)
        assert isinstance(records[0]['unit_price'], float)
        assert isinstance(records[0]['amount'], float)
        assert isinstance(records[0]['region'], str)
    
    def test_load_sales_data_filters_invalid(self, tmp_path):
        """Test that invalid records are filtered out."""
        # Create CSV with invalid records
        csv_file = tmp_path / "test_sales.csv"
        csv_file.write_text(
            "date,region,category,product,quantity,unit_price,amount\n"
            "2024-01-15,North,Electronics,Laptop,2,999.99,1999.98\n"
            "2024-01-16,South,Clothing,Shirt,0,19.99,0.00\n"
            "2024-01-17,East,Food,Snack,-5,2.99,-14.95\n"
        )
        
        records = load_sales_data(str(csv_file))
        
        # Should only have 1 valid record
        assert len(records) == 1
        assert records[0]['product'] == 'Laptop'
    
    def test_load_sales_data_all_records_valid(self):
        """Test that all loaded records have valid data."""
        records = load_sales_data()
        
        for record in records:
            assert record['amount'] > 0
            assert record['quantity'] > 0
            assert record['unit_price'] > 0
            assert record['date'] is not None
    
    def test_load_sales_data_handles_malformed_rows(self, tmp_path):
        """Test that malformed CSV rows (bad dates, non-numeric values) are filtered out."""
        csv_file = tmp_path / "test_sales.csv"
        csv_file.write_text(
            "date,region,category,product,quantity,unit_price,amount\n"
            "2024-01-15,North,Electronics,Laptop,2,999.99,1999.98\n"
            "invalid-date,South,Clothing,Shirt,5,19.99,99.95\n"
            "2024-01-17,East,Food,Snack,abc,2.99,5.98\n"
            "2024-01-18,West,Electronics,Phone,,399.99,799.98\n"
        )
        
        records = load_sales_data(str(csv_file))
        
        # Should only have 1 valid record (first one)
        assert len(records) == 1
        assert records[0]['product'] == 'Laptop'

