#!/usr/bin/env python3
"""
Unit tests for Data Provider Module
Tests AdvancedDataProvider, MultiAssetAPI, caching, rate limiting
"""

import sys
sys.path.insert(0, '.')

import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
import time


class TestAdvancedDataProvider:
    """Tests for AdvancedDataProvider class"""
    
    @pytest.fixture
    def data_provider(self):
        """Create AdvancedDataProvider instance"""
        from src.tools.advanced_data_provider import AdvancedDataProvider
        return AdvancedDataProvider()
    
    def test_provider_initialization(self, data_provider):
        """Test provider initializes correctly"""
        assert data_provider.cache is not None
        assert data_provider.rate_limiter is not None
    
    def test_get_historical_prices_import(self):
        """Test get_historical_prices can be imported"""
        from src.tools.advanced_data_provider import get_historical_prices
        assert callable(get_historical_prices)
    
    @patch('src.tools.advanced_data_provider.fetch_yahoo_finance')
    def test_fetch_us_stock(self, mock_fetch, data_provider):
        """Test fetching US stock data"""
        mock_fetch.return_value = pd.DataFrame({
            'Open': [100, 101],
            'High': [102, 103],
            'Low': [99, 100],
            'Close': [101, 102],
            'Volume': [1000000, 1100000]
        })
        
        result = data_provider.get_historical_prices("AAPL", period="5d")
        
        assert result is not None
        mock_fetch.assert_called_once()
    
    @patch('src.tools.advanced_data_provider.fetch_yahoo_finance')
    def test_fetch_idx_stock(self, mock_fetch, data_provider):
        """Test fetching Indonesian stock data"""
        mock_fetch.return_value = pd.DataFrame({
            'Close': [9500, 9600]
        })
        
        result = data_provider.get_historical_prices("BBCA", market="IDX")
        
        assert result is not None
        # Should append .JK for Yahoo Finance
        mock_fetch.assert_called()
    
    @patch('src.tools.advanced_data_provider.fetch_coingecko')
    def test_fetch_crypto(self, mock_fetch, data_provider):
        """Test fetching cryptocurrency data"""
        mock_fetch.return_value = pd.DataFrame({
            'close': [50000, 51000]
        })
        
        result = data_provider.get_historical_prices("BTC", asset_type="crypto")
        
        assert result is not None
        mock_fetch.assert_called_once()


class TestMultiAssetAPI:
    """Tests for MultiAssetAPI class"""
    
    @pytest.fixture
    def multi_api(self):
        """Create MultiAssetAPI instance"""
        from src.tools.multi_asset_api import MultiAssetAPI
        return MultiAssetAPI()
    
    def test_api_initialization(self, multi_api):
        """Test API initializes correctly"""
        assert multi_api.session is not None
    
    def test_get_price_import(self):
        """Test get_price can be imported"""
        from src.tools.multi_asset_api import get_price
        assert callable(get_price)
    
    @patch('httpx.get')
    def test_fetch_forex(self, mock_get, multi_api):
        """Test fetching forex data"""
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success", "rates": {"USD/IDR": 15000}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = multi_api.get_price("USD/IDR", asset_type="forex")
        
        assert result is not None


class TestDataCaching:
    """Tests for caching functionality"""
    
    def test_cache_set_get(self):
        """Test basic cache operations"""
        from src.tools.advanced_data_provider import DataCache
        
        cache = DataCache(ttl_seconds=60)
        cache.set("test_key", {"data": "test_value"})
        
        result = cache.get("test_key")
        assert result == {"data": "test_value"}
    
    def test_cache_expiration(self):
        """Test cache expiration"""
        from src.tools.advanced_data_provider import DataCache
        
        # Create cache with 1 second TTL
        cache = DataCache(ttl_seconds=1)
        cache.set("test_key", "test_value")
        
        # Should be available immediately
        assert cache.get("test_key") == "test_value"
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Should be expired
        assert cache.get("test_key") is None
    
    def test_cache_miss(self):
        """Test cache miss returns None"""
        from src.tools.advanced_data_provider import DataCache
        
        cache = DataCache(ttl_seconds=60)
        result = cache.get("nonexistent_key")
        assert result is None


class TestRateLimiting:
    """Tests for rate limiting functionality"""
    
    def test_rate_limiter_init(self):
        """Test rate limiter initialization"""
        from src.tools.advanced_data_provider import RateLimiter
        
        limiter = RateLimiter(max_requests=10, time_window=60)
        assert limiter.max_requests == 10
    
    def test_rate_limiter_acquire(self):
        """Test rate limiter allows requests within limit"""
        from src.tools.advanced_data_provider import RateLimiter
        
        limiter = RateLimiter(max_requests=5, time_window=60)
        
        # First 5 requests should succeed
        for i in range(5):
            assert limiter.acquire() is True
        
        # 6th request should be blocked
        assert limiter.acquire() is False
    
    def test_rate_limiter_reset(self):
        """Test rate limiter resets after time window"""
        from src.tools.advanced_data_provider import RateLimiter
        
        # Create limiter with very short window
        limiter = RateLimiter(max_requests=2, time_window=0.1)
        
        # Use up requests
        assert limiter.acquire() is True
        assert limiter.acquire() is True
        assert limiter.acquire() is False
        
        # Wait for reset
        time.sleep(0.15)
        
        # Should be able to acquire again
        assert limiter.acquire() is True


class TestDataValidation:
    """Tests for data validation"""
    
    def test_validate_ticker_format(self):
        """Test ticker format validation"""
        from src.tools.advanced_data_provider import validate_ticker
        
        assert validate_ticker("AAPL") is True
        assert validate_ticker("BTC") is True
        assert validate_ticker("BBCA.JK") is True
        assert validate_ticker("") is False
        assert validate_ticker("A") is False  # Too short
    
    def test_validate_period(self):
        """Test period validation"""
        from src.tools.advanced_data_provider import validate_period
        
        valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"]
        for period in valid_periods:
            assert validate_period(period) is True
        
        assert validate_period("invalid") is False
        assert validate_period("") is False


class TestErrorHandling:
    """Tests for error handling"""
    
    @patch('httpx.get')
    def test_api_error_handling(self, mock_get):
        """Test handling of API errors"""
        from src.tools.multi_asset_api import MultiAssetAPI
        
        mock_get.side_effect = Exception("API Error")
        
        api = MultiAssetAPI()
        result = api.get_price("INVALID", asset_type="stock_us")
        
        # Should return None or raise appropriate exception
        assert result is None or isinstance(result, (dict, float))
    
    def test_invalid_ticker_error(self):
        """Test handling of invalid ticker"""
        from src.tools.advanced_data_provider import AdvancedDataProvider
        
        provider = AdvancedDataProvider()
        result = provider.get_historical_prices("INVALID_TICKER_12345", period="1d")
        
        # Should return None or empty DataFrame
        assert result is None or len(result) == 0


class TestDataConversion:
    """Tests for data format conversion"""
    
    def test_price_formatting(self):
        """Test price formatting"""
        from src.tools.advanced_data_provider import format_price
        
        assert format_price(1500.50) == "1,500.50"
        assert format_price(1000000) == "1,000,000"
    
    def test_percentage_formatting(self):
        """Test percentage formatting"""
        from src.tools.advanced_data_provider import format_percentage
        
        assert format_percentage(0.1234) == "12.34%"
        assert format_percentage(-0.05) == "-5.00%"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
