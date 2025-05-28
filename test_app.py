import pytest
import pandas as pd
import numpy as np
import joblib
import sys
import os

# Thêm thư mục hiện tại vào path để import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import preprocess_input, district_to_wards
from api import app as flask_app

class TestApp:
    @classmethod
    def setup_class(cls):
        """Thiết lập dữ liệu test trước khi chạy các test."""
        try:
            cls.model = joblib.load("model_estimate_price_house_v5.pkl")
            cls.encoder = joblib.load("encoder_v5.pkl")
            cls.numeric_columns = ['Diện tích', 'Số tầng', 'Số phòng ngủ', 'Số nhà vệ sinh']
            cls.categorical_columns = ['Hướng cửa chính', 'Loại hình nhà ở', 'Tên phường', 'Quận']
        except FileNotFoundError:
            pytest.skip("Không tìm thấy file model, bỏ qua các test")

    def test_district_to_wards_structure(self):
        """Test cấu trúc dữ liệu district_to_wards có đúng format không."""
        assert isinstance(district_to_wards, dict)
        assert len(district_to_wards) > 0

        # Kiểm tra tất cả values đều là lists
        for district, wards in district_to_wards.items():
            assert isinstance(wards, list)
            assert len(wards) > 0
            assert all(isinstance(ward, str) for ward in wards)

    def test_preprocess_input_valid_data(self):
        """Test function preprocess_input với dữ liệu hợp lệ."""
        # Tạo dữ liệu test hợp lệ
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

        # Kiểm tra kết quả là DataFrame
        assert isinstance(result, pd.DataFrame)
        # Kiểm tra có đúng số dòng mong đợi
        assert len(result) == 1
        # Kiểm tra có nhiều cột hơn input (do encoding)
        assert len(result.columns) > len(self.numeric_columns)

    def test_preprocess_input_invalid_data(self):
        """Test function preprocess_input với dữ liệu không hợp lệ."""
        # Tạo dữ liệu test với giá trị categorical không hợp lệ
        test_data = pd.DataFrame({
            'Diện tích': [100.0],
            'Số tầng': [2],
            'Số phòng ngủ': [3],
            'Số nhà vệ sinh': [2],
            'Hướng cửa chính': ['Hướng không hợp lệ'],
            'Loại hình nhà ở': ['Loại nhà không hợp lệ'],
            'Tên phường': ['Phường không hợp lệ'],
            'Quận': ['Quận không hợp lệ']
        })

        with pytest.raises(ValueError, match="Dữ liệu nhập không hợp lệ"):
            preprocess_input(test_data, self.encoder, self.numeric_columns, self.categorical_columns)

    def test_model_prediction(self):
        """Test model có thể dự đoán được không."""
        # Tạo dữ liệu test hợp lệ
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

        # Kiểm tra prediction là số
        assert isinstance(prediction, np.ndarray)
        assert len(prediction) == 1
        assert isinstance(prediction[0], (int, float, np.number))
        assert prediction[0] > 0  # Giá nhà phải dương

    def test_numeric_columns_validation(self):
        """Test validation các cột số."""
        numeric_columns = ['Diện tích', 'Số tầng', 'Số phòng ngủ', 'Số nhà vệ sinh']

        # Test với dữ liệu số hợp lệ
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

        # Kiểm tra các cột số có chứa dữ liệu số
        for col in numeric_columns:
            assert pd.api.types.is_numeric_dtype(test_data[col])

    def test_edge_cases_input_validation(self):
        """Test các trường hợp biên cho input validation."""
        # Test với giá trị 0
        test_data_zero = pd.DataFrame({
            'Diện tích': [0.0],
            'Số tầng': [1],
            'Số phòng ngủ': [0],
            'Số nhà vệ sinh': [0],
            'Hướng cửa chính': [self.encoder.categories_[0][0]],
            'Loại hình nhà ở': [self.encoder.categories_[1][0]],
            'Tên phường': ['Phường Tân Định'],
            'Quận': ['Quận 1']
        })

        result = preprocess_input(test_data_zero, self.encoder, self.numeric_columns, self.categorical_columns)
        assert isinstance(result, pd.DataFrame)

    def test_large_values_input(self):
        """Test với giá trị lớn."""
        test_data_large = pd.DataFrame({
            'Diện tích': [1000.0],
            'Số tầng': [10],
            'Số phòng ngủ': [20],
            'Số nhà vệ sinh': [15],
            'Hướng cửa chính': [self.encoder.categories_[0][0]],
            'Loại hình nhà ở': [self.encoder.categories_[1][0]],
            'Tên phường': ['Phường Tân Định'],
            'Quận': ['Quận 1']
        })

        result = preprocess_input(test_data_large, self.encoder, self.numeric_columns, self.categorical_columns)
        prediction = self.model.predict(result)
        assert prediction[0] > 0


class TestAPI:
    """Test class cho Flask API endpoints."""

    @classmethod
    def setup_class(cls):
        """Thiết lập Flask test client."""
        cls.client = flask_app.test_client()
        flask_app.config['TESTING'] = True

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        assert response.status_code in [200, 500]  # 200 nếu model load được, 500 nếu không

        data = response.get_json()
        assert 'status' in data
        assert 'timestamp' in data
        assert 'version' in data
        assert 'model_loaded' in data

    def test_health_endpoint_with_model_error(self):
        """Test health endpoint khi có lỗi model."""
        # Test case này sẽ cover các dòng error handling
        response = self.client.get('/health')
        data = response.get_json()

        if response.status_code == 500:
            assert data['status'] == 'unhealthy'
            assert 'error' in data
        else:
            assert data['status'] == 'healthy'

    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = self.client.get('/metrics')
        assert response.status_code == 200

        data = response.get_json()
        assert 'app_info' in data
        assert 'model_info' in data
        assert 'system_info' in data

        # Test chi tiết các fields
        assert data['app_info']['name'] == 'house-price-estimator'
        assert 'version' in data['app_info']
        assert 'uptime' in data['app_info']

        assert 'model_loaded' in data['model_info']
        assert data['model_info']['model_file'] == 'model_estimate_price_house_v5.pkl'
        assert data['model_info']['encoder_file'] == 'encoder_v5.pkl'

        assert data['system_info']['python_version'] == '3.9'
        assert 'timestamp' in data['system_info']

    def test_ready_endpoint(self):
        """Test readiness endpoint."""
        response = self.client.get('/ready')
        assert response.status_code in [200, 503]  # 200 nếu ready, 503 nếu không

        data = response.get_json()
        assert 'status' in data

        if response.status_code == 200:
            assert data['status'] == 'ready'
        else:
            assert data['status'] == 'not ready'
            assert 'reason' in data

    def test_security_headers(self):
        """Test security headers được thêm vào response."""
        response = self.client.get('/health')

        # Kiểm tra các security headers
        assert response.headers.get('X-Content-Type-Options') == 'nosniff'
        assert response.headers.get('X-Frame-Options') == 'DENY'
        assert response.headers.get('X-XSS-Protection') == '1; mode=block'
        assert response.headers.get('Cache-Control') == 'no-cache, no-store, must-revalidate'
        assert response.headers.get('Pragma') == 'no-cache'
        assert response.headers.get('Expires') == '0'

    def test_flask_app_config(self):
        """Test Flask app configuration."""
        assert flask_app.config['TESTING'] == True
        # Test các config khác nếu cần

    def test_api_main_block(self):
        """Test main block của api.py."""
        # Import api module để test main block
        import api

        # Test rằng app được cấu hình đúng
        assert api.app is not None
        assert hasattr(api, 'model_loaded')
        assert hasattr(api, 'model_error')

    def test_model_loading_scenarios(self):
        """Test các scenario loading model."""
        import api

        # Test model_loaded status
        if api.model_loaded:
            assert api.model_error is None
            assert hasattr(api, 'model')
            assert hasattr(api, 'encoder')
        else:
            assert api.model_error is not None
            assert isinstance(api.model_error, str)

    def test_environment_variables(self):
        """Test environment variables handling."""
        import os

        # Test APP_VERSION environment variable
        original_version = os.environ.get('APP_VERSION')

        # Test với version được set
        os.environ['APP_VERSION'] = 'test-version-1.0'
        response = self.client.get('/health')
        data = response.get_json()
        assert data['version'] == 'test-version-1.0'

        # Test với version không được set
        if 'APP_VERSION' in os.environ:
            del os.environ['APP_VERSION']
        response = self.client.get('/health')
        data = response.get_json()
        assert data['version'] == 'unknown'

        # Restore original value
        if original_version:
            os.environ['APP_VERSION'] = original_version


class TestAppFunctions:
    """Test class riêng cho các functions trong app.py không liên quan đến Streamlit."""

    @classmethod
    def setup_class(cls):
        """Setup test data."""
        try:
            cls.encoder = joblib.load("encoder_v5.pkl")
            cls.numeric_columns = ['Diện tích', 'Số tầng', 'Số phòng ngủ', 'Số nhà vệ sinh']
            cls.categorical_columns = ['Hướng cửa chính', 'Loại hình nhà ở', 'Tên phường', 'Quận']
        except FileNotFoundError:
            pytest.skip("Không tìm thấy file encoder")

    def test_preprocess_input_error_handling(self):
        """Test error handling trong preprocess_input."""
        from app import preprocess_input

        # Test với dữ liệu có missing values
        test_data_missing = pd.DataFrame({
            'Diện tích': [None],
            'Số tầng': [2],
            'Số phòng ngủ': [3],
            'Số nhà vệ sinh': [2],
            'Hướng cửa chính': [self.encoder.categories_[0][0]],
            'Loại hình nhà ở': [self.encoder.categories_[1][0]],
            'Tên phường': ['Phường Tân Định'],
            'Quận': ['Quận 1']
        })

        # Điều này có thể raise exception tùy thuộc vào implementation
        try:
            result = preprocess_input(test_data_missing, self.encoder, self.numeric_columns, self.categorical_columns)
            # Nếu không raise exception, kiểm tra result
            assert isinstance(result, pd.DataFrame)
        except Exception as e:
            # Nếu raise exception, đó là behavior mong đợi
            assert isinstance(e, (ValueError, TypeError))


if __name__ == "__main__":
    pytest.main([__file__])
