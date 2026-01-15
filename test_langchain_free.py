#!/usr/bin/env python3
"""
LangChain-Free Core Testing Module
Testing technical indicators without LLM dependencies
"""

import sys
sys.path.insert(0, '/home/mulky/ai-hedge-fund')

import pandas as pd
import numpy as np
import importlib.util

def test_technical_indicators():
    """Test all technical indicators without LLM"""
    print("🚀 Testing Technical Indicators (LangChain-Free)")
    
    # Direct import (bypass __init__.py)
    spec = importlib.util.spec_from_file_location('technical_indicators', '/home/mulky/ai-hedge-fund/src/indicators/technical_indicators.py')
    ti_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ti_module)
    
    TechnicalIndicators = ti_module.TechnicalIndicators
    
    # Create sample data
    np.random.seed(42)
    n = 100
    dates = pd.date_range('2024-01-01', periods=n, freq='D')
    closes = pd.Series(np.random.randn(n).cumsum() + 100, index=dates)
    highs = closes + np.random.rand(n) * 2
    lows = closes - np.random.rand(n) * 2
    volumes = pd.Series(np.random.randint(1000, 10000, n), index=dates)
    
    ti = TechnicalIndicators()
    
    # Test indicators
    indicators = [
        ('RSI', lambda: ti.rsi(closes)),
        ('MACD', lambda: ti.macd(closes)),
        ('Bollinger Bands', lambda: ti.bollinger_bands(closes, period=20)),
        ('Ichimoku', lambda: ti.ichimoku_cloud(highs, lows, closes)),
        ('ATR', lambda: ti.atr(highs, lows, closes)),
        ('ADX', lambda: ti.adx(highs, lows, closes)),
    ]
    
    results = {}
    all_passed = True
    for name, test_func in indicators:
        try:
            result = test_func()
            if isinstance(result, tuple):
                assert len(result) == 3, f"MACD should return 3 components"
                results[name] = f'✅ Tuple: {len(result)} components'
            elif isinstance(result, dict):
                assert len(result) > 0, "Indicator dict should not be empty"
                results[name] = f'✅ Dict: {len(result)} components'
            else:
                series = result.dropna() if hasattr(result, 'dropna') else result
                assert len(series) > 0, "Indicator series should not be empty"
                results[name] = f'✅ Series: {len(series)} values'
        except Exception as e:
            results[name] = f'❌ Error: {str(e)[:30]}'
            all_passed = False
    
    assert all_passed, "Some indicators failed"
    for name, result in results.items():
        print(f"  {name}: {result}")

def test_portfolio_core():
    """Test portfolio manager core functionality without LLM"""
    print("🚀 Testing Portfolio Manager Core (LangChain-Free)")
    
    # Direct import
    spec = importlib.util.spec_from_file_location('portfolio_manager', '/home/mulky/ai-hedge-fund/src/agents/portfolio_manager.py')
    pm_module = importlib.util.module_from_spec(spec)
    
    # Check if we can import without langchain
    try:
        spec.loader.exec_module(pm_module)
        PortfolioManagerOutput = pm_module.PortfolioManagerOutput
        PortfolioDecision = pm_module.PortfolioDecision
        
        # Test creation
        decision = PortfolioDecision(
            action='hold',
            quantity=0,
            confidence=100,
            reasoning='Test decision'
        )
        
        output = PortfolioManagerOutput(decisions={'AAPL': decision})
        assert output is not None
        print("  Portfolio Manager: ✅ Portfolio Manager Core Works")
    except Exception as e:
        raise AssertionError(f"Portfolio Manager Core: {str(e)[:50]}")

def test_strategies_core():
    """Test strategies without LLM"""
    print("🚀 Testing Strategies Core (LangChain-Free)")
    
    # Direct import
    spec = importlib.util.spec_from_file_location('quantitative_strategies', '/home/mulky/ai-hedge-fund/src/strategies/quantitative_strategies.py')
    strats_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(strats_module)
    
    assert hasattr(strats_module, 'analyze_with_all_strategies'), "Strategies module missing analyze_with_all_strategies"
    print("  Strategies: ✅ Strategies Core Works")

def main():
    """Run all LangChain-free tests"""
    print("=" * 60)
    print("🚀 AGENT 2 - LANGCHAIN-FREE CORE TESTING")
    print("=" * 60)
    
    # Test 1: Technical Indicators
    print("\n📊 TEST 1: Technical Indicators")
    test_technical_indicators()
    
    # Test 2: Portfolio Manager Core
    print("\n📊 TEST 2: Portfolio Manager Core")
    test_portfolio_core()
    
    # Test 3: Strategies Core
    print("\n📊 TEST 3: Strategies Core")
    test_strategies_core()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print("Overall: All tests passed (LangChain-free)")
    print("🎉 Core functionality WORKING!")

if __name__ == "__main__":
    main()