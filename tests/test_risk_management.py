#!/usr/bin/env python3
"""
Unit tests for Risk Management Module
Tests VaR, CVaR, Stress Testing, Risk Limits
"""

import sys
sys.path.insert(0, '.')

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch


class TestRiskManagementFramework:
    """Tests for RiskManagementFramework class"""
    
    @pytest.fixture
    def sample_returns(self):
        """Generate sample returns data"""
        np.random.seed(42)
        n = 252  # 1 year of daily returns
        
        # Generate returns with realistic properties
        returns = pd.Series(np.random.randn(n) * 0.015)  # ~15% annualized vol
        return returns
    
    @pytest.fixture
    def risk_framework(self):
        """Create RiskManagementFramework instance"""
        from src.risk.risk_management import RiskManagementFramework
        return RiskManagementFramework(initial_capital=1000000)
    
    def test_framework_initialization(self, risk_framework):
        """Test framework initializes correctly"""
        assert risk_framework.initial_capital == 1000000
        assert risk_framework.risk_limits == {}
    
    def test_add_risk_limit(self, risk_framework):
        """Test adding risk limits"""
        from src.risk.risk_management import RiskMetric
        
        risk_framework.add_risk_limit(RiskMetric.VAR, 0.02)
        risk_framework.add_risk_limit(RiskMetric.MAX_DRAWDOWN, 0.20)
        
        assert len(risk_framework.risk_limits) == 2


class TestVaRCalculation:
    """Tests for Value at Risk calculations"""
    
    @pytest.fixture
    def sample_returns(self):
        """Sample returns for VaR testing"""
        np.random.seed(42)
        return pd.Series(np.random.randn(252) * 0.015)
    
    def test_historical_var(self, sample_returns):
        """Test Historical VaR calculation"""
        from src.risk.risk_management import RiskManagementFramework
        
        framework = RiskManagementFramework()
        var = framework.calculate_var(sample_returns, method="historical")
        
        assert isinstance(var, float)
        assert var < 0  # VaR is typically expressed as positive loss
    
    def test_parametric_var(self, sample_returns):
        """Test Parametric (Normal) VaR calculation"""
        from src.risk.risk_management import RiskManagementFramework
        
        framework = RiskManagementFramework()
        var = framework.calculate_var(sample_returns, method="parametric")
        
        assert isinstance(var, float)
        assert var > 0
    
    def test_monte_carlo_var(self, sample_returns):
        """Test Monte Carlo VaR calculation"""
        from src.risk.risk_management import RiskManagementFramework
        
        framework = RiskManagementFramework()
        var = framework.calculate_var(sample_returns, method="monte_carlo")
        
        assert isinstance(var, float)
        assert var > 0
    
    def test_var_confidence_levels(self, sample_returns):
        """Test VaR at different confidence levels"""
        from src.risk.risk_management import RiskManagementFramework
        
        framework = RiskManagementFramework()
        
        var_95 = framework.calculate_var(sample_returns, confidence=0.95)
        var_99 = framework.calculate_var(sample_returns, confidence=0.99)
        
        # VaR at 99% should be higher (more extreme loss) than 95%
        assert var_99 >= var_95


class TestCVaRCalculation:
    """Tests for Conditional VaR (Expected Shortfall) calculations"""
    
    @pytest.fixture
    def sample_returns(self):
        """Sample returns for CVaR testing"""
        np.random.seed(42)
        return pd.Series(np.random.randn(252) * 0.015)
    
    def test_cvar_calculation(self, sample_returns):
        """Test CVaR calculation"""
        from src.risk.risk_management import RiskManagementFramework
        
        framework = RiskManagementFramework()
        cvar = framework.calculate_cvar(sample_returns)
        
        assert isinstance(cvar, float)
        assert cvar > 0
        # CVaR should be greater than VaR (average of tail losses)
        var = framework.calculate_var(sample_returns)
        assert cvar >= var


class TestStressTesting:
    """Tests for stress testing functionality"""
    
    @pytest.fixture
    def sample_returns(self):
        """Sample returns for stress testing"""
        np.random.seed(42)
        return pd.Series(np.random.randn(252) * 0.015)
    
    def test_stress_test_scenarios(self, sample_returns):
        """Test stress testing with market scenarios"""
        from src.risk.risk_management import RiskManagementFramework
        
        framework = RiskManagementFramework()
        
        scenarios = {
            '2008_Crisis': (-0.40, 2.0),  # 40% drop, 2x volatility
            'COVID_Crash': (-0.30, 1.5),
            'Bull_Market': (0.20, 0.8),
        }
        
        results = framework.stress_test(sample_returns, scenarios)
        
        assert len(results) == 3
        assert '2008_Crisis' in results
        assert 'COVID_Crash' in results
        assert 'Bull_Market' in results
    
    def test_stress_test_returns_dict(self, sample_returns):
        """Test stress test returns expected structure"""
        from src.risk.risk_management import RiskManagementFramework
        
        framework = RiskManagementFramework()
        
        scenarios = {'Test_Scenario': (-0.10, 1.0)}
        results = framework.stress_test(sample_returns, scenarios)
        
        result = results['Test_Scenario']
        assert 'return_impact' in result
        assert 'volatility_impact' in result
        assert 'new_portfolio_value' in result


class TestRiskLimits:
    """Tests for risk limit checking"""
    
    @pytest.fixture
    def sample_returns(self):
        """Sample returns for limit testing"""
        np.random.seed(42)
        return pd.Series(np.random.randn(252) * 0.015)
    
    def test_check_var_limit(self, sample_returns):
        """Test VaR limit checking"""
        from src.risk.risk_management import RiskManagementFramework, RiskMetric
        
        framework = RiskManagementFramework(initial_capital=1000000)
        framework.add_risk_limit(RiskMetric.VAR, 0.02)  # 2% VaR limit
        
        result = framework.check_risk_limits(
            portfolio_value=1000000,
            positions={'AAPL': 100},
            returns=sample_returns
        )
        
        assert 'var_limit' in result
        assert isinstance(result['var_limit'], dict)
    
    def test_check_drawdown_limit(self, sample_returns):
        """Test max drawdown limit checking"""
        from src.risk.risk_management import RiskManagementFramework, RiskMetric
        
        framework = RiskManagementFramework(initial_capital=1000000)
        framework.add_risk_limit(RiskMetric.MAX_DRAWDOWN, 0.20)  # 20% max drawdown
        
        result = framework.check_risk_limits(
            portfolio_value=950000,
            positions={'AAPL': 100},
            returns=sample_returns
        )
        
        assert 'max_drawdown_limit' in result


class TestMaxDrawdown:
    """Tests for maximum drawdown calculation"""
    
    def test_max_drawdown_calculation(self):
        """Test max drawdown from equity curve"""
        from src.risk.risk_management import calculate_max_drawdown
        
        equity = pd.Series([100, 105, 102, 108, 100, 95, 110])
        mdd = calculate_max_drawdown(equity)
        
        # Max drawdown from 108 to 95 = 13/108 ≈ 12%
        assert mdd > 0
        assert mdd < 0.20
    
    def test_max_drawdown_uptrend(self):
        """Test drawdown in continuous uptrend"""
        from src.risk.risk_management import calculate_max_drawdown
        
        equity = pd.Series([100, 110, 120, 130, 140])
        mdd = calculate_max_drawdown(equity)
        
        assert mdd == 0  # No drawdown in pure uptrend


class TestRiskMetrics:
    """Tests for RiskMetric enum"""
    
    def test_metric_values(self):
        """Test RiskMetric has expected values"""
        from src.risk.risk_management import RiskMetric
        
        assert hasattr(RiskMetric, 'VAR')
        assert hasattr(RiskMetric, 'CVAR')
        assert hasattr(RiskMetric, 'MAX_DRAWDOWN')
        assert hasattr(RiskMetric, 'VOLATILITY')
        assert hasattr(RiskMetric, 'CONCENTRATION')


class TestSharpeSortino:
    """Tests for risk-adjusted return metrics"""
    
    @pytest.fixture
    def sample_returns(self):
        """Sample returns for metrics"""
        np.random.seed(42)
        return pd.Series(np.random.randn(252) * 0.015)
    
    def test_sharpe_ratio(self, sample_returns):
        """Test Sharpe ratio calculation"""
        from src.risk.risk_management import calculate_sharpe_ratio
        
        sharpe = calculate_sharpe_ratio(sample_returns)
        
        assert isinstance(sharpe, float)
        # Sharpe can be negative
        assert not np.isnan(sharpe)
    
    def test_sortino_ratio(self, sample_returns):
        """Test Sortino ratio calculation"""
        from src.risk.risk_management import calculate_sortino_ratio
        
        sortino = calculate_sortino_ratio(sample_returns)
        
        assert isinstance(sortino, float)
        assert not np.isnan(sortino)
        # Sortino should be higher than Sharpe (uses downside deviation)
        sharpe = calculate_sharpe_ratio(sample_returns)
        assert sortino >= sharpe


class TestBetaCalculation:
    """Tests for beta calculation"""
    
    def test_beta_calculation(self):
        """Test portfolio beta against benchmark"""
        from src.risk.risk_management import calculate_beta
        
        np.random.seed(42)
        portfolio_returns = pd.Series(np.random.randn(252) * 0.02)
        benchmark_returns = pd.Series(np.random.randn(252) * 0.015)
        
        beta = calculate_beta(portfolio_returns, benchmark_returns)
        
        assert isinstance(beta, float)
        # Beta should be around 1 for random walks
        assert 0 < beta < 3


class TestRiskReport:
    """Tests for risk report generation"""
    
    @pytest.fixture
    def sample_returns(self):
        """Sample returns for report"""
        np.random.seed(42)
        return pd.Series(np.random.randn(252) * 0.015)
    
    def test_generate_risk_report(self, sample_returns):
        """Test comprehensive risk report generation"""
        from src.risk.risk_management import RiskManagementFramework
        
        framework = RiskManagementFramework(initial_capital=1000000)
        
        report = framework.generate_risk_report(
            returns=sample_returns,
            positions={'AAPL': 100, 'MSFT': 50}
        )
        
        assert 'var' in report
        assert 'cvar' in report
        assert 'max_drawdown' in report
        assert 'sharpe_ratio' in report
        assert 'volatility' in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
