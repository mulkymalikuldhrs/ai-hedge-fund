"""
Complete Integration Test for AI Hedge Fund v2.2
=================================================

Tests all major modules and their interactions.

Usage:
    python3 test_integration.py
"""

import sys
import json
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def test_memory_system():
    """Test enhanced memory system"""
    print("1. Testing Memory System...")
    try:
        from src.memory.enhanced_memory_system import get_memory_system

        mem = get_memory_system()
        status = mem.get_system_status()
        print(f"   ✓ Memory loaded - Status: {status['status']}")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_trading_plan():
    """Test trading plan"""
    print("2. Testing Trading Plan...")
    try:
        from src.trading_plan.trading_plan import get_trading_plan_manager

        plan = get_trading_plan_manager()
        print(f"   ✓ Plan loaded: {plan.plan.name}")
        print(f"   ✓ Risk/Trade: {plan.plan.risk_parameters.max_risk_per_trade * 100}%")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_data_provider():
    """Test free data provider"""
    print("3. Testing Data Provider...")
    try:
        from src.data.free_data_provider import get_free_data_provider

        dp = get_free_data_provider()
        symbols = dp.get_supported_symbols()
        print(f"   ✓ Data provider loaded - {len(symbols)} symbols")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_mt_bridge():
    """Test MetaTrader bridge"""
    print("4. Testing MetaTrader Bridge...")
    try:
        from src.execution.metatrader_bridge import get_metatrader_bridge

        mt = get_metatrader_bridge(simulate=True)
        info = mt.get_account_info()
        print(f"   ✓ MT Bridge ready - Balance: ${info.balance:,.2f}")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_telegram_bot():
    """Test Telegram bot"""
    print("5. Testing Telegram Bot...")
    try:
        from src.dashboard.telegram_bot import get_notification_manager

        manager = get_notification_manager()
        manager.initialize(use_mock=True)
        bot = manager.get_bot()
        print(f"   ✓ Telegram bot loaded - Type: {type(bot).__name__}")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_ml_generator():
    """Test ML signal generator"""
    print("6. Testing ML Signal Generator...")
    try:
        from src.ml.ml_signal_generator import get_ml_signal_generator

        ml_gen = get_ml_signal_generator()
        ml_gen.initialize()
        status = ml_gen.get_model_status()
        print(f"   ✓ ML Generator loaded - {len(status['models'])} models")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_backtesting():
    """Test backtesting engine"""
    print("7. Testing Backtesting Engine...")
    try:
        from src.backtesting.backtest_engine import get_backtest_engine

        engine = get_backtest_engine()
        print(f"   ✓ Backtesting engine loaded")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_paper_trading():
    """Test paper trading"""
    print("8. Testing Paper Trading...")
    try:
        from src.paper_trading.paper_trader import get_paper_trader

        trader = get_paper_trader()
        portfolio = trader.get_portfolio_summary()
        print(f"   ✓ Paper trader loaded - Equity: ${portfolio.total_equity:,.2f}")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_dashboard_modules():
    """Test dashboard modules"""
    print("9. Testing Dashboard Modules...")
    try:
        from src.dashboard import CLITerminal

        print(f"   ✓ CLI Terminal loaded")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_data_fetching():
    """Test real data fetching"""
    print("10. Testing Data Fetching...")
    try:
        from src.data.free_data_provider import get_free_data_provider

        dp = get_free_data_provider()

        test_symbols = ["BTC", "EURUSD"]
        results = []
        for symbol in test_symbols:
            price = dp.get_current_price(symbol)
            if price.current_price > 0:
                results.append(f"{symbol}: ${price.current_price:,.2f}")

        print(f"   ✓ Data fetched: {', '.join(results)}")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def main():
    print("=" * 60)
    print("AI HEDGE FUND v2.2 - INTEGRATION TEST")
    print("=" * 60)
    print()

    tests = [
        test_memory_system,
        test_trading_plan,
        test_data_provider,
        test_mt_bridge,
        test_telegram_bot,
        test_ml_generator,
        test_backtesting,
        test_paper_trading,
        test_dashboard_modules,
        test_data_fetching,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ✗ Unexpected error: {e}")
            results.append(False)
        print()

    passed = sum(results)
    total = len(results)

    print("=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("✓ All systems operational!")
    else:
        print("⚠ Some issues detected - review output above")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
