import pytest
import pandas as pd
import numpy as np
import joblib
import sys
import os

# Add the current directory to the path to import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import preprocess_input, district_to_wards

class TestApp:
    @classmethod
    def setup_class(cls):
        """Setup test fixtures before running tests."""
        try:
            cls.model = joblib.load("model_estimate_price_house_v5.pkl")
            cls.encoder = joblib.load("encoder_v5.pkl")
            cls.numeric_columns = ['Diện tích', 'Số tầng', 'Số phòng ngủ', 'Số nhà vệ sinh']
            cls.categorical_columns = ['Hướng cửa chính', 'Loại hình nhà ở', 'Tên phường', 'Quận']
        except FileNotFoundError:
            pytest.skip("Model files not found, skipping tests")

    def test_district_to_wards_structure(self):
        """Test that district_to_wards has the expected structure."""
        assert isinstance(district_to_wards, dict)
        assert len(district_to_wards) > 0
        
        # Check that all values are lists
        for district, wards in district_to_wards.items():
            assert isinstance(wards, list)
            assert len(wards) > 0
            assert all(isinstance(ward, str) for ward in wards)

    def test_preprocess_input_valid_data(self):
        """Test preprocess_input with valid data."""
        # Create sample valid data
        test_data = pd.DataFrame({
            'Diện tích': [100.0],
            'Số tầng': [2],
            'Số phòng ngủ': [3],
            'Số nhà vệ sinh': [2],
            'Hướng cửa chính': [self.encoder.categories_[0][0]],
            'Loại hình nhà ở': [self.encoder.categories_[1][0]],
            'Tên phường': ['Phường Tân Định'],
            'Quận': ['Quận 1']
        })
        
        result = preprocess_input(test_data, self.encoder, self.numeric_columns, self.categorical_columns)
        
        # Check that result is a DataFrame
        assert isinstance(result, pd.DataFrame)
        # Check that it has the expected number of rows
        assert len(result) == 1
        # Check that it has more columns than input (due to encoding)
        assert len(result.columns) > len(self.numeric_columns)

    def test_preprocess_input_invalid_data(self):
        """Test preprocess_input with invalid categorical data."""
        # Create sample data with invalid categorical values
        test_data = pd.DataFrame({
            'Diện tích': [100.0],
            'Số tầng': [2],
            'Số phòng ngủ': [3],
            'Số nhà vệ sinh': [2],
            'Hướng cửa chính': ['Invalid Direction'],
            'Loại hình nhà ở': ['Invalid Type'],
            'Tên phường': ['Invalid Ward'],
            'Quận': ['Invalid District']
        })
        
        with pytest.raises(ValueError, match="Dữ liệu nhập không hợp lệ"):
            preprocess_input(test_data, self.encoder, self.numeric_columns, self.categorical_columns)

    def test_model_prediction(self):
        """Test that model can make predictions."""
        # Create sample valid data
        test_data = pd.DataFrame({
            'Diện tích': [100.0],
            'Số tầng': [2],
            'Số phòng ngủ': [3],
            'Số nhà vệ sinh': [2],
            'Hướng cửa chính': [self.encoder.categories_[0][0]],
            'Loại hình nhà ở': [self.encoder.categories_[1][0]],
            'Tên phường': ['Phường Tân Định'],
            'Quận': ['Quận 1']
        })
        
        X_processed = preprocess_input(test_data, self.encoder, self.numeric_columns, self.categorical_columns)
        prediction = self.model.predict(X_processed)
        
        # Check that prediction is a number
        assert isinstance(prediction, np.ndarray)
        assert len(prediction) == 1
        assert isinstance(prediction[0], (int, float, np.number))
        assert prediction[0] > 0  # Price should be positive

    def test_numeric_columns_validation(self):
        """Test validation of numeric columns."""
        numeric_columns = ['Diện tích', 'Số tầng', 'Số phòng ngủ', 'Số nhà vệ sinh']
        
        # Test with valid numeric data
        test_data = pd.DataFrame({
            'Diện tích': [100.0],
            'Số tầng': [2],
            'Số phòng ngủ': [3],
            'Số nhà vệ sinh': [2],
            'Hướng cửa chính': [self.encoder.categories_[0][0]],
            'Loại hình nhà ở': [self.encoder.categories_[1][0]],
            'Tên phường': ['Phường Tân Định'],
            'Quận': ['Quận 1']
        })
        
        # Check that numeric columns contain numeric data
        for col in numeric_columns:
            assert pd.api.types.is_numeric_dtype(test_data[col])

if __name__ == "__main__":
    pytest.main([__file__])
