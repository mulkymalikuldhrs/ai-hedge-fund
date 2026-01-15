#!/usr/bin/env python3
"""
Unit tests for Portfolio Optimizer Module
Tests Mean-Variance, Black-Litterman, Risk Parity, HRP
"""

import sys
sys.path.insert(0, '.')

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch


class TestPortfolioOptimizer:
    """Tests for PortfolioOptimizer class"""
    
    @pytest.fixture
    def sample_returns(self):
        """Generate sample returns data"""
        np.random.seed(42)
        n = 252  # 1 year of daily returns
        assets = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
        
        returns = pd.DataFrame(
            np.random.randn(n, len(assets)) * 0.02,
            columns=assets
        )
        return returns
    
    @pytest.fixture
    def optimizer(self, sample_returns):
        """Create PortfolioOptimizer instance"""
        from src.optimization.portfolio_optimizer import PortfolioOptimizer
        return PortfolioOptimizer(sample_returns)
    
    def test_optimizer_initialization(self, optimizer):
        """Test optimizer initializes correctly"""
        assert optimizer.returns is not None
        assert len(optimizer.assets) == 4
    
    def test_mean_variance_optimization(self, optimizer):
        """Test Mean-Variance Optimization"""
        result = optimizer.mean_variance_optimization()
        
        assert result is not None
        assert 'weights' in result
        assert 'expected_return' in result
        assert 'volatility' in result
        
        weights = result['weights']
        assert len(weights) == len(optimizer.assets)
        assert abs(sum(weights) - 1.0) < 0.001  # Weights sum to 1
    
    def test_mean_variance_target_return(self, optimizer):
        """Test MVO with target return constraint"""
        target_return = 0.10  # 10% annual return
        result = optimizer.mean_variance_optimization(target_return=target_return)
        
        assert result is not None
        assert result['expected_return'] >= target_return * 0.9  # Allow some tolerance
    
    def test_risk_parity_portfolio(self, optimizer):
        """Test Risk Parity portfolio construction"""
        result = optimizer.risk_parity_portfolio()
        
        assert result is not None
        assert 'weights' in result
        assert 'risk_contributions' in result
        
        weights = result['weights']
        assert len(weights) == len(optimizer.assets)
        assert abs(sum(weights) - 1.0) < 0.001
    
    def test_black_litterman_import(self):
        """Test Black-Litterman can be imported"""
        from src.optimization.portfolio_optimizer import PortfolioOptimizer
        assert hasattr(PortfolioOptimizer, 'black_litterman_optimization')
    
    def test_black_litterman_with_views(self, optimizer):
        """Test Black-Litterman with market views"""
        market_caps = {
            'AAPL': 1000,
            'GOOGL': 800,
            'MSFT': 900,
            'AMZN': 700
        }
        
        views = {
            'AAPL': (0.15, 0.7),  # Expected return 15%, 70% confidence
            'GOOGL': (0.12, 0.6),
        }
        
        result = optimizer.black_litterman_optimization(
            market_caps=market_caps,
            views=views
        )
        
        assert result is not None
        assert 'weights' in result
        assert 'expected_return' in result
    
    def test_hierarchical_risk_parity(self, optimizer):
        """Test Hierarchical Risk Parity (HRP)"""
        result = optimizer.hierarchical_risk_parity()
        
        assert result is not None
        assert 'weights' in result
        assert 'cluster_order' in result
        
        weights = result['weights']
        assert len(weights) == len(optimizer.assets)
        assert abs(sum(weights) - 1.0) < 0.001
    
    def test_efficient_frontier(self, optimizer):
        """Test Efficient Frontier generation"""
        n_points = 20
        frontier = optimizer.efficient_frontier(n_points=n_points)
        
        assert frontier is not None
        assert len(frontier) == n_points
        
        # Each point should have return and volatility
        for point in frontier:
            assert 'return' in point
            assert 'volatility' in point
            assert 'weights' in point
    
    def test_minimum_variance_portfolio(self, optimizer):
        """Test minimum variance portfolio"""
        result = optimizer.minimum_variance_portfolio()
        
        assert result is not None
        assert 'weights' in result
        assert 'volatility' in result
        
        weights = result['weights']
        # Min variance should have positive weights
        assert all(w >= 0 for w in weights)
        assert abs(sum(weights) - 1.0) < 0.001


class TestOptimizationMethods:
    """Tests for OptimizationMethod enum"""
    
    def test_method_values(self):
        """Test OptimizationMethod has expected values"""
        from src.optimization.portfolio_optimizer import OptimizationMethod
        
        assert hasattr(OptimizationMethod, 'MEAN_VARIANCE')
        assert hasattr(OptimizationMethod, 'RISK_PARITY')
        assert hasattr(OptimizationMethod, 'BLACK_LITTERMAN')
        assert hasattr(OptimizationMethod, 'HRP')


class TestPortfolioMetrics:
    """Tests for portfolio metrics calculations"""
    
    @pytest.fixture
    def sample_returns(self):
        """Sample returns for metrics testing"""
        np.random.seed(42)
        n = 252
        assets = ['AAPL', 'MSFT']
        
        returns = pd.DataFrame(
            np.random.randn(n, len(assets)) * 0.02,
            columns=assets
        )
        return returns
    
    def test_sharpe_ratio_calculation(self, sample_returns):
        """Test Sharpe ratio calculation"""
        from src.optimization.portfolio_optimizer import calculate_sharpe_ratio
        
        weights = np.array([0.5, 0.5])
        sharpe = calculate_sharpe_ratio(sample_returns, weights)
        
        assert isinstance(sharpe, float)
        # Sharpe can be negative
        assert not np.isnan(sharpe)
    
    def test_sortino_ratio_calculation(self, sample_returns):
        """Test Sortino ratio calculation"""
        from src.optimization.portfolio_optimizer import calculate_sortino_ratio
        
        weights = np.array([0.5, 0.5])
        sortino = calculate_sortino_ratio(sample_returns, weights)
        
        assert isinstance(sortino, float)
        assert not np.isnan(sortino)
    
    def test_portfolio_volatility(self, sample_returns):
        """Test portfolio volatility calculation"""
        from src.optimization.portfolio_optimizer import calculate_portfolio_volatility
        
        weights = np.array([0.5, 0.5])
        vol = calculate_portfolio_volatility(sample_returns, weights)
        
        assert isinstance(vol, float)
        assert vol > 0


class TestEdgeCases:
    """Tests for edge cases"""
    
    def test_single_asset(self):
        """Test optimizer with single asset"""
        from src.optimization.portfolio_optimizer import PortfolioOptimizer
        
        returns = pd.DataFrame({'AAPL': np.random.randn(252) * 0.02})
        optimizer = PortfolioOptimizer(returns)
        
        result = optimizer.mean_variance_optimization()
        assert result['weights']['AAPL'] == 1.0
    
    def test_identical_returns(self):
        """Test optimizer with identical assets"""
        from src.optimization.portfolio_optimizer import PortfolioOptimizer
        
        returns = pd.DataFrame({
            'AAPL': np.random.randn(252) * 0.02,
            'MSFT': np.random.randn(252) * 0.02,
        })
        # Make returns identical
        returns['MSFT'] = returns['AAPL']
        
        optimizer = PortfolioOptimizer(returns)
        result = optimizer.mean_variance_optimization()
        
        assert result is not None
    
    def test_highly_correlated_assets(self):
        """Test optimizer with highly correlated assets"""
        from src.optimization.portfolio_optimizer import PortfolioOptimizer
        
        n = 252
        base_returns = np.random.randn(n) * 0.02
        
        returns = pd.DataFrame({
            'AAPL': base_returns + np.random.randn(n) * 0.005,
            'MSFT': base_returns + np.random.randn(n) * 0.005,
        })
        
        optimizer = PortfolioOptimizer(returns)
        result = optimizer.mean_variance_optimization()
        
        assert result is not None
        assert 'weights' in result
    
    def test_insufficient_data(self):
        """Test optimizer with insufficient data"""
        from src.optimization.portfolio_optimizer import PortfolioOptimizer
        
        # Less than 2 observations
        returns = pd.DataFrame({'AAPL': [0.01, 0.02]})
        
        optimizer = PortfolioOptimizer(returns)
        # Should handle gracefully
        try:
            optimizer.mean_variance_optimization()
        except Exception as e:
            assert "insufficient" in str(e).lower() or "data" in str(e).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
