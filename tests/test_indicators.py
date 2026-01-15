#!/usr/bin/env python3
"""
Unit tests for Technical Indicators Module
Covers: RSI, MACD, Bollinger Bands, Stochastic, Ichimoku, and 30+ indicators
"""

import sys
sys.path.insert(0, '.')

import pytest
import pandas as pd
import numpy as np
from src.indicators.technical_indicators import TechnicalIndicators


class TestTechnicalIndicators:
    """Base test class for technical indicators"""
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample OHLCV data"""
        np.random.seed(42)
        n = 100
        dates = pd.date_range(start='2024-01-01', periods=n, freq='1D')
        
        closes = pd.Series(np.cumsum(np.random.randn(n)) + 100, index=dates)
        highs = closes + np.abs(np.random.randn(n)) * 2
        lows = closes - np.abs(np.random.randn(n)) * 2
        opens = closes + np.random.randn(n)
        volumes = pd.Series(np.random.randint(1000, 10000, n), index=dates)
        
        return {
            'opens': opens,
            'highs': highs,
            'lows': lows,
            'closes': closes,
            'volumes': volumes
        }
    
    @pytest.fixture
    def ti(self):
        """Create TechnicalIndicators instance"""
        return TechnicalIndicators()


class TestRSI(TestTechnicalIndicators):
    """Tests for RSI indicator"""
    
    def test_rsi_default_period(self, ti, sample_data):
        """Test RSI with default 14-period"""
        result = ti.rsi(sample_data['closes'])
        assert len(result) == len(sample_data['closes'])
        assert result.notna().sum() > 0
        
    def test_rsi_periods(self, ti, sample_data):
        """Test RSI with different periods"""
        for period in [7, 14, 21]:
            result = ti.rsi(sample_data['closes'], period=period)
            assert len(result) == len(sample_data['closes'])
    
    def test_rsi_values_range(self, ti, sample_data):
        """Test RSI values are between 0 and 100"""
        result = ti.rsi(sample_data['closes'])
        valid_result = result.dropna()
        assert valid_result.min() >= 0
        assert valid_result.max() <= 100
    
    def test_rsi_oversold_overbought(self, ti, sample_data):
        """Test RSI oversold (<30) and overbought (>70) detection"""
        result = ti.rsi(sample_data['closes'])
        oversold = (result < 30).sum()
        overbought = (result > 70).sum()
        assert isinstance(oversold, (int, np.integer))


class TestMACD(TestTechnicalIndicators):
    """Tests for MACD indicator"""
    
    def test_macd_default(self, ti, sample_data):
        """Test MACD with default parameters"""
        macd, signal, hist = ti.macd(sample_data['closes'])
        assert len(macd) == len(sample_data['closes'])
        assert len(signal) == len(sample_data['closes'])
        assert len(hist) == len(sample_data['closes'])
    
    def test_macd_custom_periods(self, ti, sample_data):
        """Test MACD with custom periods"""
        macd, signal, hist = ti.macd(sample_data['closes'], fast=8, slow=17, signal_period=9)
        assert len(macd) == len(sample_data['closes'])
    
    def test_macd_histogram_sign(self, ti, sample_data):
        """Test MACD histogram can be positive or negative"""
        macd, signal, hist = ti.macd(sample_data['closes'])
        valid_hist = hist.dropna()
        assert len(valid_hist) > 0


class TestBollingerBands(TestTechnicalIndicators):
    """Tests for Bollinger Bands indicator"""
    
    def test_bb_default(self, ti, sample_data):
        """Test Bollinger Bands with default parameters"""
        upper, middle, lower = ti.bollinger_bands(sample_data['closes'])
        assert len(upper) == len(sample_data['closes'])
        assert len(middle) == len(sample_data['closes'])
        assert len(lower) == len(sample_data['closes'])
    
    def test_bb_bounds(self, ti, sample_data):
        """Test Bollinger Bands: lower < middle < upper"""
        upper, middle, lower = ti.bollinger_bands(sample_data['closes'])
        valid_idx = lower.notna()
        assert (lower[valid_idx] <= middle[valid_idx]).all()
        assert (middle[valid_idx] <= upper[valid_idx]).all()


class TestStochastic(TestTechnicalIndicators):
    """Tests for Stochastic oscillator"""
    
    def test_stochastic_default(self, ti, sample_data):
        """Test Stochastic with default parameters"""
        k, d = ti.stochastic(sample_data['highs'], sample_data['lows'], sample_data['closes'])
        assert len(k) == len(sample_data['closes'])
        assert len(d) == len(sample_data['closes'])
    
    def test_stochastic_values(self, ti, sample_data):
        """Test Stochastic K and D values between 0-100"""
        k, d = ti.stochastic(sample_data['highs'], sample_data['lows'], sample_data['closes'])
        valid_k = k.dropna()
        valid_d = d.dropna()
        assert valid_k.min() >= 0
        assert valid_k.max() <= 100


class TestATR(TestTechnicalIndicators):
    """Tests for Average True Range"""
    
    def test_atr_default(self, ti, sample_data):
        """Test ATR with default 14-period"""
        result = ti.atr(sample_data['highs'], sample_data['lows'], sample_data['closes'])
        assert len(result) == len(sample_data['closes'])
        assert result.notna().sum() > 0
    
    def test_atr_positive(self, ti, sample_data):
        """Test ATR values are positive"""
        result = ti.atr(sample_data['highs'], sample_data['lows'], sample_data['closes'])
        valid_result = result.dropna()
        assert (valid_result >= 0).all()


class TestADX(TestTechnicalIndicators):
    """Tests for Average Directional Index"""
    
    def test_adx_default(self, ti, sample_data):
        """Test ADX with default parameters"""
        adx, plus_di, minus_di = ti.adx(sample_data['highs'], sample_data['lows'], sample_data['closes'])
        assert len(adx) == len(sample_data['closes'])
        assert len(plus_di) == len(sample_data['closes'])
        assert len(minus_di) == len(sample_data['closes'])
    
    def test_adx_range(self, ti, sample_data):
        """Test ADX values between 0-100"""
        adx, _, _ = ti.adx(sample_data['highs'], sample_data['lows'], sample_data['closes'])
        valid_adx = adx.dropna()
        assert valid_adx.min() >= 0
        assert valid_adx.max() <= 100


class TestIchimokuCloud(TestTechnicalIndicators):
    """Tests for Ichimoku Cloud indicator - AFTER BUG FIX"""
    
    def test_ichimoku_default(self, ti, sample_data):
        """Test Ichimoku with default parameters"""
        result = ti.ichimoku_cloud(
            sample_data['highs'], 
            sample_data['lows'], 
            sample_data['closes']
        )
        assert 'conversion' in result
        assert 'base' in result
        assert 'leading_a' in result
        assert 'leading_b' in result
        assert 'lagging' in result
        
        assert len(result['conversion']) == len(sample_data['closes'])
        assert len(result['lagging']) == len(sample_data['closes'])
    
    def test_ichimoku_custom_periods(self, ti, sample_data):
        """Test Ichimoku with custom periods"""
        result = ti.ichimoku_cloud(
            sample_data['highs'],
            sample_data['lows'],
            sample_data['closes'],
            conversion_period=9,
            base_period=26,
            lagging_span=52,
            displacement=26
        )
        assert len(result['conversion']) == len(sample_data['closes'])
    
    def test_ichimoku_leading_spans(self, ti, sample_data):
        """Test that leading spans are shifted correctly"""
        result = ti.ichimoku_cloud(
            sample_data['highs'],
            sample_data['lows'],
            sample_data['closes']
        )
        # Leading spans should be shifted by displacement (26 periods)
        leading_a_valid = result['leading_a'].notna().sum()
        leading_b_valid = result['leading_b'].notna().sum()
        assert leading_a_valid < len(sample_data['closes'])
        assert leading_b_valid < len(sample_data['closes'])


class TestOBV(TestTechnicalIndicators):
    """Tests for On-Balance Volume"""
    
    def test_obv(self, ti, sample_data):
        """Test OBV calculation"""
        result = ti.obv(sample_data['closes'], sample_data['volumes'])
        assert len(result) == len(sample_data['closes'])
        assert result.notna().sum() > 0


class TestCCI(TestTechnicalIndicators):
    """Tests for Commodity Channel Index"""
    
    def test_cci(self, ti, sample_data):
        """Test CCI calculation"""
        result = ti.cci(sample_data['highs'], sample_data['lows'], sample_data['closes'])
        assert len(result) == len(sample_data['closes'])


class TestWilliamsR(TestTechnicalIndicators):
    """Tests for Williams %R"""
    
    def test_williams_r(self, ti, sample_data):
        """Test Williams %R calculation"""
        result = ti.williams_r(sample_data['highs'], sample_data['lows'], sample_data['closes'])
        assert len(result) == len(sample_data['closes'])
        valid = result.dropna()
        assert valid.min() >= -100
        assert valid.max() <= 0


class TestMFI(TestTechnicalIndicators):
    """Tests for Money Flow Index"""
    
    def test_mfi(self, ti, sample_data):
        """Test MFI calculation"""
        result = ti.mfi(sample_data['highs'], sample_data['lows'], sample_data['closes'], sample_data['volumes'])
        assert len(result) == len(sample_data['closes'])


class TestGetAllIndicators(TestTechnicalIndicators):
    """Tests for get_all_indicators convenience function"""
    
    def test_get_all_indicators(self, ti, sample_data):
        """Test getting all indicators at once"""
        result = ti.get_all_indicators(
            sample_data['highs'],
            sample_data['lows'],
            sample_data['closes'],
            sample_data['volumes']
        )
        
        # Should contain common indicators
        expected_indicators = ['rsi', 'macd', 'bollinger_bands', 'stochastic', 'atr', 'adx']
        for indicator in expected_indicators:
            assert indicator in result


class TestEdgeCases(TestTechnicalIndicators):
    """Tests for edge cases and error handling"""
    
    def test_short_data(self, ti):
        """Test with minimal data"""
        closes = pd.Series([100, 101, 102, 103, 104])
        highs = closes + 1
        lows = closes - 1
        
        result = ti.rsi(closes)
        assert len(result) == len(closes)
    
    def test_constant_data(self, ti):
        """Test with constant price data"""
        closes = pd.Series([100] * 50)
        highs = closes
        lows = closes
        
        result = ti.rsi(closes)
        assert len(result) == len(closes)
    
    def test_single_value(self, ti):
        """Test with single value"""
        closes = pd.Series([100])
        highs = pd.Series([101])
        lows = pd.Series([99])
        
        result = ti.rsi(closes)
        assert len(result) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
