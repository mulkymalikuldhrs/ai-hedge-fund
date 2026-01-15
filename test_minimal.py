#!/usr/bin/env python3
"""
MINIMAL TEST RUNNER - Test core functionality without external dependencies
Focus on indicators, strategies, and data processing
"""

import sys
import os
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def test_technical_indicators():
    """Test Technical Indicators standalone"""
    print("\n=== TECHNICAL INDICATORS TEST ===")
    
    try:
        # Generate sample data
        np.random.seed(42)
        n = 100
        dates = pd.date_range(start='2024-01-01', periods=n, freq='1D')
        closes = pd.Series(np.cumsum(np.random.randn(n)) + 100, index=dates)
        highs = closes + np.abs(np.random.randn(n)) * 2
        lows = closes - np.abs(np.random.randn(n)) * 2
        volumes = pd.Series(np.random.randint(1000, 10000, n), index=dates)
        
        # Test imports - temporary fix for langchain issue
        import importlib.util
        
        # Temporarily mock langchain_core for testing
        sys.modules['langchain_core'] = type(sys)('langchain_core')
        sys.modules['langchain_core.runnables'] = type(sys)('langchain_core.runnables')
        sys.modules['langchain_core.runnables.graph'] = type(sys)('langchain_core.runnables.graph')
        sys.modules['langchain_core.runnables.graph'].MermaidDrawMethod = type('MermaidDrawMethod', (), {})
        
        from src.indicators.technical_indicators import TechnicalIndicators
        ti = TechnicalIndicators()
        
        # Test key indicators
        print("  Testing RSI...")
        rsi = ti.rsi(closes)
        assert len(rsi) == len(closes)
        print("    ✅ RSI calculated")
        
        print("  Testing MACD...")
        macd, signal, hist = ti.macd(closes)
        assert len(macd) == len(closes)
        print("    ✅ MACD calculated")
        
        print("  Testing Bollinger Bands...")
        upper, middle, lower = ti.bollinger_bands(closes)
        assert len(upper) == len(closes)
        print("    ✅ Bollinger Bands calculated")
        
        print("  Testing Stochastic...")
        k, d = ti.stochastic(highs, lows, closes)
        assert len(k) == len(closes)
        print("    ✅ Stochastic calculated")
        
        print("  Testing ATR...")
        atr = ti.atr(highs, lows, closes)
        assert len(atr) == len(closes)
        print("    ✅ ATR calculated")
        
        print("  Testing Ichimoku Cloud...")
        ichimoku = ti.ichimoku_cloud(highs, lows, closes)
        assert 'conversion' in ichimoku
        assert 'lagging' in ichimoku
        print("    ✅ Ichimoku Cloud calculated")
        
        print("  Testing SuperTrend...")
        supertrend, direction = ti.supertrend(highs, lows, closes)
        assert len(supertrend) == len(closes)
        print("    ✅ SuperTrend calculated")
        
        print("  Testing All Indicators...")
        all_indicators = ti.get_all_indicators(highs, lows, closes, volumes)
        assert len(all_indicators) > 0
        print(f"    ✅ {len(all_indicators)} indicators calculated")
        
    except Exception as e:
        print(f"  ❌ Technical Indicators Error: {e}")
        import traceback
        traceback.print_exc()
        raise

def test_quantitative_strategies():
    """Test Quantitative Strategies standalone"""
    print("\n=== QUANTITATIVE STRATEGIES TEST ===")
    
    try:
        from src.strategies.quantitative_strategies import analyze_with_all_strategies
        
        # Sample price data
        np.random.seed(42)
        prices = list(np.cumsum(np.random.randn(100)) + 100)
        
        # Test strategies
        result = analyze_with_all_strategies("AAPL", prices, {})
        
        assert result is not None
        assert hasattr(result, 'final_signal'), "Result should have final_signal"
        assert hasattr(result, 'strategy_details'), "Result should have strategy_details"
        assert hasattr(result, 'weighted_score'), "Result should have weighted_score"
        
        print("  ✅ All 6 strategies executed")
        print(f"    Final Signal: {result.final_signal}")
        print(f"    Weighted Score: {result.weighted_score}")
        
    except Exception as e:
        print(f"  ❌ Quantitative Strategies Error: {e}")
        import traceback
        traceback.print_exc()
        raise

def test_portfolio_optimization():
    """Test Portfolio Optimization standalone"""
    print("\n=== PORTFOLIO OPTIMIZATION TEST ===")
    
    try:
        # Mock langchain_core for portfolio optimizer too
        sys.modules['langchain_core'] = type(sys)('langchain_core')
        sys.modules['langchain_core.runnables'] = type(sys)('langchain_core.runnables')
        
        from src.optimization.portfolio_optimizer import PortfolioOptimizer
        
        # Generate sample returns
        np.random.seed(42)
        n = 252
        assets = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
        returns = pd.DataFrame(
            np.random.randn(n, len(assets)) * 0.02,
            columns=assets
        )
        
        optimizer = PortfolioOptimizer(returns)
        
        print("  Testing Mean-Variance Optimization...")
        mv_result = optimizer.mean_variance_optimization()
        assert mv_result is not None
        assert hasattr(mv_result, 'weights'), "MVO result should have weights attribute"
        print("    ✅ MVO completed")
        
        print("  Testing Risk Parity...")
        rp_result = optimizer.risk_parity_portfolio()
        assert rp_result is not None
        print("    ✅ Risk Parity completed")
        
        print("  Testing Minimum Variance...")
        min_var = optimizer.min_variance_portfolio()
        assert min_var is not None
        print("    ✅ Minimum Variance completed")
        
        print("  Testing Efficient Frontier...")
        frontier = optimizer.efficient_frontier(n_points=10)
        assert len(frontier) == 10
        print("    ✅ Efficient Frontier completed")
        
    except Exception as e:
        print(f"  ❌ Portfolio Optimization Error: {e}")
        import traceback
        traceback.print_exc()
        raise

def test_risk_management():
    """Test Risk Management standalone"""
    print("\n=== RISK MANAGEMENT TEST ===")
    
    try:
        # Mock langchain_core for risk management
        sys.modules['langchain_core'] = type(sys)('langchain_core')
        sys.modules['langchain_core.runnables'] = type(sys)('langchain_core.runnables')
        
        from src.risk.risk_management import RiskManagementFramework
        
        framework = RiskManagementFramework()
        
        # Generate sample returns
        np.random.seed(42)
        returns = pd.Series(np.random.randn(252) * 0.015)
        returns.index = pd.date_range('2024-01-01', periods=252, freq='D')
        
        print("  Testing VaR Calculation...")
        var = framework.calculate_var(returns, portfolio_value=1000000, method="historical")
        assert var is not None
        print(f"    ✅ 95% VaR: {var:.2f}")
        
        print("  Testing CVaR Calculation...")
        cvar = framework.calculate_cvar(returns, portfolio_value=1000000)
        assert cvar is not None
        print(f"    ✅ 95% CVaR: {cvar:.2f}")
        
        print("  Testing Stress Testing...")
        scenarios = {
            'Market_Crash': (-0.20, 2.0),
            'Bull_Market': (0.15, 0.8)
        }
        stress_results = framework.stress_test(returns, scenarios)
        assert len(stress_results) == 2
        print("    ✅ Stress testing completed")
        
    except Exception as e:
        print(f"  ❌ Risk Management Error: {e}")
        import traceback
        traceback.print_exc()
        raise

def test_data_provider():
    """Test Data Provider functionality (without API calls)"""
    print("\n=== DATA PROVIDER TEST ===")
    
    try:
        # Mock langchain_core
        sys.modules['langchain_core'] = type(sys)('langchain_core')
        sys.modules['langchain_core.runnables'] = type(sys)('langchain_core.runnables')
        
        from src.tools.multi_asset_api import POPULAR_TICKERS
        
        assert POPULAR_TICKERS is not None
        assert len(POPULAR_TICKERS) > 0
        print(f"  ✅ POPULAR_TICKERS: {len(POPULAR_TICKERS)} tickers")
        
        # Test ticker validation (if function exists)
        try:
            from src.tools.advanced_data_provider import validate_ticker
            assert validate_ticker("AAPL") == True
            assert validate_ticker("") == False
            print("  ✅ Ticker validation works")
        except ImportError:
            print("  ⚠️  Ticker validation not available")
        
    except Exception as e:
        print(f"  ❌ Data Provider Error: {e}")
        import traceback
        traceback.print_exc()
        raise

def test_launcher_imports():
    """Test launcher can import (basic syntax check)"""
    print("\n=== LAUNCHER IMPORT TEST ===")
    
    try:
        # Test launcher file exists and can be parsed
        with open('launcher.py', 'r') as f:
            launcher_code = f.read()
        
        # Basic syntax check
        compile(launcher_code, 'launcher.py', 'exec')
        print("  ✅ launcher.py syntax valid")
        
        # Check for key functions
        assert 'def main' in launcher_code
        assert 'if __name__' in launcher_code
        print("  ✅ launcher.py has main function")
        
    except Exception as e:
        print(f"  ❌ Launcher Import Error: {e}")
        raise

def main():
    """Run all tests"""
    print("🚀 AI HEDGE FUND - MINIMAL TEST SUITE")
    print("=" * 60)
    print("Testing core functionality without external dependencies")
    
    test_results = []
    
    # Run tests
    test_results.append(("Technical Indicators", test_technical_indicators()))
    test_results.append(("Quantitative Strategies", test_quantitative_strategies()))
    test_results.append(("Portfolio Optimization", test_portfolio_optimization()))
    test_results.append(("Risk Management", test_risk_management()))
    test_results.append(("Data Provider", test_data_provider()))
    test_results.append(("Launcher Syntax", test_launcher_imports()))
    
    # Results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:<10} {test_name}")
        if result:
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 OVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Core functionality working!")
        print("\n📋 NEXT STEPS:")
        print("1. Install missing langchain-core package")
        print("2. Test launcher.py functionality")
        print("3. Run integration tests")
        print("4. Test with real data")
    else:
        print(f"⚠️  {total - passed} tests failed. Fix issues before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
