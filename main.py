#!/usr/bin/env python3
"""
AI HEDGE FUND v2.2 - UNIFIED ENTRY POINT
=========================================
Single entry point for the entire trading system.

Features:
- 3-Mode Operation: Manual, Semi-Auto, Full-Auto
- Multi-Asset: Stocks, Forex, Crypto, Commodities
- 34 Trading Strategies
- Enhanced Memory System (SQLite + JSON)
- MetaTrader Browser Bridge (FREE automation)
- Streamlit Web Dashboard
- Enhanced CLI Terminal
- Free Data Sources (Yahoo, CoinGecko, ExchangeRate)
- Paper Trading & Backtesting
- ML Signal Generator (Random Forest, XGBoost, LSTM)
- Telegram Notifications

Usage:
    # Dashboard & Terminal
    python3 main.py --dashboard          # Streamlit web UI
    python3 main.py --cli                # Enhanced CLI
    python3 main.py --terminal           # Legacy CLI

    # Analysis & Trading
    python3 main.py AAPL                 # Quick analysis
    python3 main.py AAPL --mode auto     # Autonomous trading
    python3 main.py AAPL,BTC,USD/IDR     # Multi-asset
    python3 main.py AAPL --paper         # Paper trading

    # Backtesting
    python3 main.py --backtest EURUSD --days 365
    python3 main.py --backtest AAPL --strategies all

    # Testing & Info
    python3 main.py --test               # Integration test
    python3 main.py --status             # System status
    python3 main.py --modules            # List modules
    python3 main.py --help               # This help

Examples:
    python3 main.py AAPL --mode semi-auto --risk 2
    python3 main.py BTC --asset crypto --days 100
    python3 main.py --backtest EURUSD --days 180 --report
    python3 main.py --dashboard --port 8501
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging

sys.path.insert(0, str(Path(__file__).parent))

from colorama import Fore, Style, init

init(autoreset=True)

import pandas as pd


# ============ ENUMS ============


class TradingMode(Enum):
    MANUAL = "manual"
    SEMI_AUTO = "semi-auto"
    FULL_AUTO = "full-auto"


class Signal(Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"


class AssetType(Enum):
    STOCK_US = "stock_us"
    STOCK_IDX = "stock_idx"
    FOREX = "forex"
    CRYPTO = "crypto"
    COMMODITY = "commodity"
    INDEX = "index"


# ============ VERSION ============

VERSION = "2.2.0"
BUILD_DATE = "2026-01-16"


# ============ BANNER ============


def print_banner():
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   🤖 AI HEDGE FUND v{VERSION}                                                              ║
║   Unified Trading System - Single Entry Point                                       ║
║                                                                                      ║
║   • 34+ Trading Strategies  • 3-Mode Operation  • Multi-Asset Support              ║
║   • ML Signal Generator    • Backtesting       • Paper Trading                     ║
║   • Streamlit Dashboard    • CLI Terminal      • Telegram Notifications            ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")


# ============ SYSTEM INITIALIZER ============


class SystemInitializer:
    """Initialize all system components"""

    def __init__(self):
        self.memory = None
        self.trading_plan = None
        self.data_provider = None
        self.mt_bridge = None
        self.ml_generator = None
        self.paper_trader = None

    def initialize_all(self, silent: bool = False) -> Dict[str, bool]:
        """Initialize all components and return status"""
        results = {}

        if not silent:
            print(
                f"\n{Fore.CYAN}⚙️  Initializing system components...{Style.RESET_ALL}\n"
            )

        # Memory System
        try:
            from src.memory.enhanced_memory_system import get_memory_system

            self.memory = get_memory_system()
            results["memory"] = True
            if not silent:
                print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Memory System")
        except Exception as e:
            results["memory"] = False
            if not silent:
                print(f"   {Fore.RED}✗{Style.RESET_ALL} Memory: {e}")

        # Trading Plan
        try:
            from src.trading_plan.trading_plan import get_trading_plan_manager

            self.trading_plan = get_trading_plan_manager()
            results["trading_plan"] = True
            if not silent:
                print(
                    f"   {Fore.GREEN}✓{Style.RESET_ALL} Trading Plan: {self.trading_plan.plan.name}"
                )
        except Exception as e:
            results["trading_plan"] = False
            if not silent:
                print(f"   {Fore.RED}✗{Style.RESET_ALL} Trading Plan: {e}")

        # Data Provider
        try:
            from src.data.free_data_provider import get_free_data_provider

            self.data_provider = get_free_data_provider()
            results["data_provider"] = True
            if not silent:
                print(
                    f"   {Fore.GREEN}✓{Style.RESET_ALL} Data Provider ({len(self.data_provider.get_supported_symbols())} symbols)"
                )
        except Exception as e:
            results["data_provider"] = False
            if not silent:
                print(f"   {Fore.RED}✗{Style.RESET_ALL} Data Provider: {e}")

        # MetaTrader Bridge
        try:
            from src.execution.metatrader_bridge import get_metatrader_bridge

            self.mt_bridge = get_metatrader_bridge(simulate=True)
            results["mt_bridge"] = True
            if not silent:
                print(
                    f"   {Fore.GREEN}✓{Style.RESET_ALL} MetaTrader Bridge (Simulator)"
                )
        except Exception as e:
            results["mt_bridge"] = False
            if not silent:
                print(f"   {Fore.YELLOW}⚠{Style.RESET_ALL} MetaTrader: {e}")

        # ML Generator
        try:
            from src.ml.ml_signal_generator import get_ml_signal_generator

            self.ml_generator = get_ml_signal_generator()
            self.ml_generator.initialize()
            results["ml_generator"] = True
            if not silent:
                print(f"   {Fore.GREEN}✓{Style.RESET_ALL} ML Generator (3 models)")
        except Exception as e:
            results["ml_generator"] = False
            if not silent:
                print(f"   {Fore.YELLOW}⚠{Style.RESET_ALL} ML Generator: {e}")

        # Paper Trader
        try:
            from src.paper_trading.paper_trader import get_paper_trader

            self.paper_trader = get_paper_trader()
            results["paper_trader"] = True
            if not silent:
                print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Paper Trader")
        except Exception as e:
            results["paper_trader"] = False
            if not silent:
                print(f"   {Fore.YELLOW}⚠{Style.RESET_ALL} Paper Trader: {e}")

        return results


# ============ DATA PROVIDER ============


class UnifiedDataProvider:
    """Unified data provider wrapper"""

    def __init__(self, provider):
        self.provider = provider

    def get_price(self, symbol: str) -> Dict:
        """Get current price for a symbol"""
        try:
            data = self.provider.get_current_price(symbol)
            return {
                "symbol": symbol,
                "price": data.current_price,
                "change": data.daily_change_pct,
                "type": data.asset_type,
                "high": data.high_24h,
                "low": data.low_24h,
            }
        except Exception as e:
            return {"symbol": symbol, "error": str(e)}

    def get_historical(self, symbol: str, days: int = 100) -> pd.DataFrame:
        """Get historical data"""
        try:
            data = self.provider.get_historical_data(symbol, days=days)
            if data:
                df = pd.DataFrame(
                    [
                        {
                            "open": o.open,
                            "high": o.high,
                            "low": o.low,
                            "close": o.close,
                            "volume": o.volume,
                        }
                        for o in data
                    ]
                )
                return df
            return pd.DataFrame()
        except Exception:
            return pd.DataFrame()


# ============ ANALYSIS ENGINE ============


class AnalysisEngine:
    """Quick analysis engine"""

    def __init__(self, data_provider):
        self.dp = UnifiedDataProvider(data_provider)

    def analyze(self, symbol: str, days: int = 100) -> Dict:
        """Analyze a symbol"""
        price = self.dp.get_price(symbol)
        df = self.dp.get_historical(symbol, days)

        if "error" in price:
            return price

        if df.empty:
            return {"symbol": symbol, "error": "No historical data"}

        # Simple indicators
        close = df["close"].iloc[-1]
        sma20 = df["close"].rolling(20).mean().iloc[-1]
        rsi = self._calculate_rsi(df["close"])

        # Determine signal
        if close > sma20 and rsi < 70:
            signal = Signal.BUY if rsi > 30 else Signal.STRONG_BUY
        elif close < sma20 and rsi > 30:
            signal = Signal.SELL if rsi < 70 else Signal.STRONG_SELL
        else:
            signal = Signal.HOLD

        return {
            "symbol": symbol,
            "price": price["price"],
            "change": price["change"],
            "sma20": sma20,
            "rsi": rsi,
            "signal": signal.value,
            "trend": "BULLISH" if close > sma20 else "BEARISH",
        }

    def _calculate_rsi(self, closes: pd.Series, period: int = 14) -> float:
        delta = closes.diff()
        gain = delta.where(delta > 0, 0).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / (loss + 1e-10)
        return 100 - (100 / (1 + rs)).iloc[-1]


# ============ COMMAND HANDLERS ============


def cmd_dashboard(args):
    """Launch Streamlit dashboard with auto-browser open"""
    print_banner()

    dashboard_path = Path(__file__).parent / "src" / "dashboard" / "streamlit_app.py"

    if not dashboard_path.exists():
        print(f"{Fore.RED}✗ Dashboard not found at {dashboard_path}{Style.RESET_ALL}")
        return

    url = f"http://localhost:{args.port}"

    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                    🌐 STREAMLIT DASHBOARD v{VERSION}                  ║
╠════════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  🚀 Starting dashboard at: {Fore.GREEN}{url}{Style.RESET_ALL}                          ║
║                                                                    ║
║  📝 Streamlit will open automatically in your browser              ║
║  📍 If browser doesn't open, manually navigate to:                 ║
║     {Fore.WHITE}{url}{Style.RESET_ALL}                                         ║
║                                                                    ║
║  ⏳ Waiting for server to start...                                 ║
║                                                                    ║
║  🛑 Press Ctrl+C to stop                                           ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
    """)

    import subprocess
    import time
    import threading

    def wait_and_open_browser():
        """Wait for server then open browser"""
        max_wait = 10
        waited = 0

        while waited < max_wait:
            try:
                import urllib.request

                urllib.request.urlopen(url, timeout=1)
                break
            except:
                time.sleep(1)
                waited += 1

        if waited < max_wait:
            print(
                f"\n{Fore.GREEN}✅ Server ready! Opening browser...{Style.RESET_ALL}\n"
            )
            try:
                subprocess.run(["xdg-open", url], check=False)
                print(f"{Fore.CYAN}🌐 Browser opened at: {url}{Style.RESET_ALL}")
            except FileNotFoundError:
                print(
                    f"{Fore.YELLOW}⚠ xdg-open not found. Manually open: {url}{Style.RESET_ALL}"
                )
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ Could not open browser: {e}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠ Server took too long to start{Style.RESET_ALL}")

    def streamlit_running():
        """Check if streamlit is running"""
        try:
            import urllib.request

            urllib.request.urlopen(url, timeout=1)
            return True
        except:
            return False

    try:
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(dashboard_path),
                "--server.port",
                str(args.port),
                "--server.headless",
                "true",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        browser_thread = threading.Thread(target=wait_and_open_browser)
        browser_thread.start()

        print(f"{Fore.CYAN}⏳ Dashboard is starting...{Style.RESET_ALL}\n")

        while streamlit_running():
            time.sleep(2)

        process.terminate()
        print(f"\n{Fore.YELLOW}🛑 Dashboard stopped{Style.RESET_ALL}")

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 Dashboard stopped by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")


def cmd_cli(args):
    """Launch enhanced CLI terminal"""
    from src.dashboard.cli_terminal import CLITerminal

    terminal = CLITerminal()
    terminal.run()


def cmd_terminal(args):
    """Launch legacy CLI terminal"""
    print_banner()
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║     🤖 AI HEDGE FUND - TERMINAL v{VERSION}       ║
╚════════════════════════════════════════════╝
{Style.RESET_ALL}

Available commands:
  1. Analyze symbol
  2. Multi-asset analysis
  3. View memory
  4. Statistics
  5. Exit

Type 'help' for more options.
""")

    init = SystemInitializer()
    init.initialize_all(silent=True)

    analyzer = AnalysisEngine(init.data_provider) if init.data_provider else None

    while True:
        try:
            cmd = input(f"\n{Fore.CYAN}HF>{Style.RESET_ALL} ").strip().lower()

            if cmd in ["exit", "quit", "5"]:
                print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}\n")
                break

            elif cmd in ["help", "?"]:
                print("""
Available Commands:
  analyze <symbol>  - Analyze a symbol
  portfolio         - Show portfolio status
  status            - System status
  test              - Run integration test
  clear             - Clear screen
  exit/quit         - Exit
                """)

            elif cmd.startswith("analyze") or cmd == "1":
                symbol = (
                    cmd.split()[1]
                    if len(cmd.split()) > 1
                    else input("Symbol: ").strip().upper()
                )
                if symbol and analyzer:
                    result = analyzer.analyze(symbol)
                    if "error" in result:
                        print(f"   {Fore.RED}✗{Style.RESET_ALL} {result['error']}")
                    else:
                        print(f"""
   {Fore.CYAN}{"─" * 50}{Style.RESET_ALL}
   Symbol:     {Fore.WHITE}{result["symbol"]}{Style.RESET_ALL}
   Price:      {Fore.GREEN}${result["price"]:,.5f}{Style.RESET_ALL}
   Change:     {Fore.GREEN if result["change"] >= 0 else Fore.RED}{result["change"]:+.2f}%{Style.RESET_ALL}
   SMA(20):    {Fore.WHITE}${result["sma20"]:,.5f}{Style.RESET_ALL}
   RSI(14):    {Fore.WHITE}{result["rsi"]:.1f}{Style.RESET_ALL}
   Signal:     {Fore.GREEN if "BUY" in result["signal"] else Fore.RED if "SELL" in result["signal"] else Fore.YELLOW}{result["signal"]}{Style.RESET_ALL}
   Trend:      {Fore.WHITE}{result["trend"]}{Style.RESET_ALL}
   {Fore.CYAN}{"─" * 50}{Style.RESET_ALL}
                """)

            elif cmd in ["portfolio", "status"]:
                if init.memory:
                    status = init.memory.get_system_status()
                    print(f"   Status: {status.get('status', 'unknown')}")
                    print(f"   Total signals: {status.get('total_signals', 0)}")

            elif cmd == "test":
                print(f"\n{Fore.CYAN}Running integration test...{Style.RESET_ALL}")
                cmd_test(args)

            elif cmd == "clear":
                os.system("cls" if os.name == "nt" else "clear")

            else:
                print(f"   {Fore.YELLOW}Unknown command: {cmd}{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}\n")
            break
        except Exception as e:
            print(f"   {Fore.RED}Error: {e}{Style.RESET_ALL}")


def cmd_backtest(args):
    """Run backtest"""
    print_banner()
    print(f"\n{Fore.CYAN}⚙️  Running Backtest: {args.backtest}{Style.RESET_ALL}\n")

    init = SystemInitializer()
    init.initialize_all(silent=True)

    if not init.data_provider:
        print(f"{Fore.RED}✗ Data provider not available{Style.RESET_ALL}")
        return

    from src.backtesting.backtest_engine import get_backtest_engine

    data = init.data_provider.get_historical_data(args.backtest, days=args.days + 50)

    if not data or len(data) < 50:
        print(f"{Fore.RED}✗ Insufficient data for {args.backtest}{Style.RESET_ALL}")
        return

    df = pd.DataFrame(
        [
            {
                "open": o.open,
                "high": o.high,
                "low": o.low,
                "close": o.close,
                "volume": o.volume,
            }
            for o in data
        ]
    )

    engine = get_backtest_engine()
    results = engine.run_backtest(df, args.backtest, "EMA Strategy", days=args.days)

    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║              BACKTEST RESULTS                   ║
╠════════════════════════════════════════════════╣
║  Period:         {results.period_days:>6} days                 ║
║  Initial:        ${results.initial_capital:>10,.2f}            ║
║  Final:          ${results.final_capital:>10,.2f}            ║
║  Return:         {results.total_return_pct:>6.2f}%                  ║
╠════════════════════════════════════════════════╣
║  Trades:         {results.total_trades:>6}                    ║
║  Win Rate:       {results.win_rate:>6.1f}%                  ║
║  Profit Factor:  {results.profit_factor:>6.2f}                    ║
╠════════════════════════════════════════════════╣
║  Max Drawdown:   {results.max_drawdown_pct:>6.2f}%                  ║
║  Sharpe Ratio:   {results.sharpe_ratio:>6.2f}                    ║
╚════════════════════════════════════════════════╝
Time: {results.execution_time_seconds:.2f}s
    """)


def cmd_analyze(args):
    """Analyze symbols"""
    print_banner()
    print(f"\n{Fore.CYAN}📊 Analyzing: {args.symbols}{Style.RESET_ALL}\n")

    init = SystemInitializer()
    init.initialize_all(silent=True)

    if not init.data_provider:
        print(f"{Fore.RED}✗ Data provider not available{Style.RESET_ALL}")
        return

    analyzer = AnalysisEngine(init.data_provider)

    symbols = [s.strip().upper() for s in args.symbols.split(",")]

    print(
        f"{Fore.CYAN}┌──────────┬────────────┬──────────┬────────┬────────┐{Style.RESET_ALL}"
    )
    print(
        f"{Fore.CYAN}│ Symbol   │ Price      │ Change   │ RSI    │ Signal │{Style.RESET_ALL}"
    )
    print(
        f"{Fore.CYAN}├──────────┼────────────┼──────────┼────────┼────────┤{Style.RESET_ALL}"
    )

    for symbol in symbols:
        result = analyzer.analyze(symbol, days=args.days)

        if "error" in result:
            print(
                f"{Fore.CYAN}│{Style.RESET_ALL} {symbol:8s} {Fore.RED}Error: {result['error'][:15]}{Style.RESET_ALL}        "
            )
        else:
            change = result["change"]
            color = Fore.GREEN if change >= 0 else Fore.RED
            signal_color = (
                Fore.GREEN
                if "BUY" in result["signal"]
                else Fore.RED
                if "SELL" in result["signal"]
                else Fore.YELLOW
            )
            print(
                f"{Fore.CYAN}│{Style.RESET_ALL} {symbol:8s} │ ${result['price']:>10,.2f} │ {color}{change:>+7.2f}%{Style.RESET_ALL} │ {result['rsi']:>6.1f} │{signal_color} {result['signal']:<6}{Style.RESET_ALL} │"
            )

    print(
        f"{Fore.CYAN}└──────────┴────────────┴──────────┴────────┴────────┘{Style.RESET_ALL}\n"
    )


def cmd_test(args):
    """Run integration test"""
    print_banner()
    print(f"\n{Fore.CYAN}🧪 Running Integration Test...{Style.RESET_ALL}\n")

    init = SystemInitializer()
    results = init.initialize_all(silent=True)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print(f"\n{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
    print(f"   System Status: {passed}/{total} components ready")
    print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}\n")

    if init.data_provider:
        print(f"{Fore.CYAN}📊 Testing Data Provider...{Style.RESET_ALL}")
        test_symbols = ["AAPL", "BTC", "EURUSD"]
        for symbol in test_symbols:
            price = init.data_provider.get_current_price(symbol)
            status = "✓" if price.current_price > 0 else "✗"
            print(f"   {status} {symbol}: ${price.current_price:,.2f}")

    print(f"\n{Fore.GREEN}✓ Integration test complete!{Style.RESET_ALL}\n")


def cmd_status(args):
    """Show system status"""
    print_banner()
    print(f"\n{Fore.CYAN}📊 System Status v{VERSION}{Style.RESET_ALL}\n")

    init = SystemInitializer()
    results = init.initialize_all(silent=True)

    print(f"""
{Fore.CYAN}{"─" * 60}{Style.RESET_ALL}
Component                    Status
{"─" * 60}{Style.RESET_ALL}
Memory System               {results.get("memory", False) and Fore.GREEN + "✓ Ready" or Fore.RED + "✗ Error"}
Trading Plan                {results.get("trading_plan", False) and Fore.GREEN + "✓ Ready" or Fore.RED + "✗ Error"}
Data Provider               {results.get("data_provider", False) and Fore.GREEN + "✓ Ready" or Fore.RED + "✗ Error"}
MetaTrader Bridge           {results.get("mt_bridge", False) and Fore.GREEN + "✓ Ready" or Fore.YELLOW + "⚠ Simulator"}
ML Generator                {results.get("ml_generator", False) and Fore.GREEN + "✓ Ready" or Fore.YELLOW + "⚠ Unavailable"}
Paper Trader                {results.get("paper_trader", False) and Fore.GREEN + "✓ Ready" or Fore.YELLOW + "⚠ Unavailable"}
{"─" * 60}{Style.RESET_ALL}

Build: {BUILD_DATE}
Python: {sys.version.split()[0]}
    """)


def cmd_modules(args):
    """List all modules"""
    print_banner()
    print(f"\n{Fore.CYAN}📦 Available Modules{Style.RESET_ALL}\n")

    modules = [
        ("src/dashboard/streamlit_app.py", "Streamlit Web Dashboard"),
        ("src/dashboard/cli_terminal.py", "Enhanced CLI Terminal"),
        ("src/dashboard/telegram_bot.py", "Telegram Bot"),
        ("src/data/free_data_provider.py", "Free Data Provider"),
        ("src/ml/ml_signal_generator.py", "ML Signal Generator"),
        ("src/backtesting/backtest_engine.py", "Backtesting Engine"),
        ("src/paper_trading/paper_trader.py", "Paper Trading"),
        ("src/memory/enhanced_memory_system.py", "Memory System"),
        ("src/trading_plan/trading_plan.py", "Trading Plan"),
        ("src/execution/metatrader_bridge.py", "MetaTrader Bridge"),
    ]

    print(
        f"{Fore.CYAN}┌────────────────────────────────────────────────────────┐{Style.RESET_ALL}"
    )
    for path, desc in modules:
        exists = "✓" if Path(path).exists() else "✗"
        print(
            f"{Fore.CYAN}│{Style.RESET_ALL} {exists} {desc:<50} {Fore.CYAN}│{Style.RESET_ALL}"
        )
    print(
        f"{Fore.CYAN}└────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n"
    )


# ============ MAIN ============


def main():
    parser = argparse.ArgumentParser(
        description=f"AI Hedge Fund v{VERSION} - Unified Trading System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dashboard & Terminal
  python3 main.py --dashboard          # Streamlit web UI
  python3 main.py --cli                # Enhanced CLI
  python3 main.py --terminal           # Legacy CLI

  # Analysis & Trading
  python3 main.py AAPL                 # Quick analysis
  python3 main.py AAPL --mode auto     # Autonomous trading
  python3 main.py AAPL,BTC,USD/IDR     # Multi-asset
  python3 main.py AAPL --paper         # Paper trading

  # Backtesting
  python3 main.py --backtest EURUSD --days 365
  python3 main.py --backtest AAPL --report

  # Testing & Info
  python3 main.py --test               # Integration test
  python3 main.py --status             # System status
  python3 main.py --modules            # List modules
        """,
    )

    # Positional arguments
    parser.add_argument("symbols", nargs="?", help="Trading symbols (comma-separated)")

    # Dashboard & Terminal
    parser.add_argument(
        "--dashboard", "-d", action="store_true", help="Launch Streamlit dashboard"
    )
    parser.add_argument(
        "--cli", "-c", action="store_true", help="Launch enhanced CLI terminal"
    )
    parser.add_argument(
        "--terminal", "-t", action="store_true", help="Launch legacy CLI terminal"
    )
    parser.add_argument(
        "--port", type=int, default=8501, help="Dashboard port (default: 8501)"
    )

    # Analysis options
    parser.add_argument(
        "--mode",
        "-m",
        choices=["manual", "semi-auto", "auto"],
        default="manual",
        help="Trading mode",
    )
    parser.add_argument("--days", type=int, default=100, help="Historical data period")
    parser.add_argument(
        "--asset",
        "-a",
        choices=["stock_us", "forex", "crypto"],
        default="stock_us",
        help="Asset type",
    )
    parser.add_argument("--paper", action="store_true", help="Use paper trading")
    parser.add_argument("--risk", type=float, default=2.0, help="Risk percentage")

    # Backtesting
    parser.add_argument(
        "--backtest",
        "-b",
        nargs="?",
        const="EURUSD",
        help="Run backtest (symbol optional)",
    )
    parser.add_argument("--strategies", help="Strategies to test")
    parser.add_argument(
        "--report", action="store_true", help="Generate backtest report"
    )

    # Testing & Info
    parser.add_argument("--test", action="store_true", help="Run integration test")
    parser.add_argument(
        "--status", "-s", action="store_true", help="Show system status"
    )
    parser.add_argument("--modules", action="store_true", help="List all modules")
    parser.add_argument(
        "--version", action="version", version=f"AI Hedge Fund v{VERSION}"
    )

    args = parser.parse_args()

    # Print banner for non-dashboard commands
    if not args.dashboard:
        print_banner()

    # Route commands
    if args.dashboard:
        cmd_dashboard(args)
    elif args.cli:
        cmd_cli(args)
    elif args.terminal:
        cmd_terminal(args)
    elif args.backtest:
        cmd_backtest(args)
    elif args.test:
        cmd_test(args)
    elif args.status:
        cmd_status(args)
    elif args.modules:
        cmd_modules(args)
    elif args.symbols:
        cmd_analyze(args)
    else:
        cmd_status(args)
        print(f"\n{Fore.YELLOW}Use --help for available commands{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
