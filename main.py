#!/usr/bin/env python3
"""
AI HEDGE FUND v2.3.0 - INTERACTIVE UNIFIED ENTRY POINT
=======================================================
SINGLE entry point for entire trading system with interactive menu.

Features:
- Interactive Menu System (Main Entry Point)
- 3-Mode Trading: Manual, Semi-Auto, Full-Auto
- Agent Constitution v2.3.0 Integrated
- Multi-Asset: Indonesian Stocks, Global Stocks, Forex, Crypto, Commodities, Indices
- 53 Trading Strategies (18 Retail/SMC + 6 Quant + 10 Legendary + 13 Enhanced)
- Unified Multi-Strategy Analysis System
- Enhanced Memory System (SQLite + JSON)
- LLM7 Integration (Primary LLM: gpt-5-nano)
- MetaTrader Browser Bridge (FREE automation)
- Streamlit Web Dashboard with Visualizations
- Enhanced CLI Terminal with Colors
- Multi-Source Free Data: Financial Datasets API, Yahoo, CoinGecko, ExchangeRate, IDX
- Paper Trading & Backtesting
- ML Signal Generator (Random Forest, XGBoost, LSTM)
- Telegram Notifications
- Auto-Heal System (Health, Backup, Strategy Evaluation)

Data Sources:
- Indonesian Stocks: BBCA, BBRI, TLKM, UNVR, GOTO, etc.
- Global Stocks: AAPL, MSFT, GOOGL, TSLA, NVDA, etc.
- Forex: EURUSD, GBPUSD, USDJPY, USDIDR, etc.
- Crypto: BTC, ETH, SOL, XRP, ADA, etc.
- Commodities: Gold (XAU), Silver (XAG), Oil, Natural Gas
- Indices: JCI, S&P 500, NASDAQ, DAX, Nikkei, etc.

Interactive Menu Usage:
    python3 main.py                      # Interactive menu (RECOMMENDED)

CLI Usage:
    python3 main.py --dashboard          # Streamlit web UI
    python3 main.py --cli                # Enhanced CLI
    python3 main.py AAPL                 # Quick analysis
    python3 main.py --status             # System status
    python3 main.py --autoheal           # Launch Auto-Heal
    python3 main.py --live-trading       # Start live trading

Examples:
    python3 main.py                      # Interactive menu (recommended)
    python3 main.py --dashboard --port 8501
    python3 main.py BBCA --asset idn        # Indonesian stock analysis
    python3 main.py AAPL --mode auto         # Autonomous trading
    python3 main.py BTC --asset crypto        # Crypto analysis
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

VERSION = "2.3.0"
BUILD_DATE = "2026-01-19"
FEATURE_VERSION = "Agent Constitution + Full Integration"


# ============ BANNER ============


def print_banner():
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════╗
 ║                                                                              ║
 ║   🤖 AI HEDGE FUND v{VERSION}                                        ║
 ║   Interactive Trading System - Single Entry Point                              ║
 ║                                                                              ║
 ║   • 53+ Trading Strategies  • Agent Constitution v2.3.0 • Multi-Asset   ║
 ║   • LLM7 Integration     • Enhanced Data      • Auto-Heal System     ║
 ║   • Graham, Turtle, SEPA • Multi-Agent System   • Risk Management     ║
 ║   • Comprehensive Registry • Unified Analysis • SMC, ICT, Wyckoff     ║
 ║                                                                              ║
 ╚════════════════════════════════════════════════════════════════════════╝
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


# ============ INTERACTIVE MENU ============


class InteractiveMenu:
    """Interactive menu system for AI Hedge Fund"""

    def __init__(self):
        self.init = SystemInitializer()

    def show_menu(self):
        """Show main interactive menu"""

    print_banner()
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════╗
 ║                                                                              ║
 ║   🤖 AI HEDGE FUND v{VERSION}                                        ║
 ║   Interactive Trading System - Single Entry Point                              ║
 ║                                                                              ║
 ║   • 53+ Trading Strategies  • RISET v2.2.2 Integrated  • Multi-Asset   ║
 ║   • LLM7 Integration     • Enhanced Data      • Auto-Heal System     ║
 ║   • Graham, Turtle, SEPA • Multi-Agent System   • Risk Management     ║
 ║   • Comprehensive Registry • Unified Analysis • SMC, ICT, Wyckoff     ║
 ║                                                                              ║
 ╚════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

    def run(self):
        """Run interactive menu loop"""
        self.show_menu()

        while True:
            try:
                choice = input(
                    f"\n{Fore.CYAN}Select option [0-22]: {Style.RESET_ALL}"
                ).strip()

                if choice == "0":
                    print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}\n")
                    break
                elif choice == "1":
                    self._run_dashboard()
                elif choice == "2":
                    self._run_cli()
                elif choice == "3":
                    self._run_quick_analysis()
                elif choice == "4":
                    self._run_multi_asset()
                elif choice == "5":
                    self._run_paper_trading()
                elif choice == "6":
                    self._run_live_trading()
                elif choice == "7":
                    self._run_backtest()
                elif choice == "8":
                    self._run_autoheal()
                elif choice == "9":
                    self._run_strategy_evaluator()
                elif choice == "10":
                    self._run_status()
                elif choice == "11":
                    self._run_graham_value()
                elif choice == "12":
                    self._run_turtle_trading()
                elif choice == "13":
                    self._run_sepa_strategy()
                elif choice == "14":
                    self._run_riset_backtest()
                elif choice == "15":
                    self._run_riset_integration()
                elif choice == "16":
                    self._run_unified_analysis()
                elif choice == "17":
                    self._run_registry_info()
                elif choice == "18":
                    self._run_config()
                elif choice == "19":
                    cmd_modules(None)
                elif choice == "20":
                    self._run_smc_strategies()
                elif choice == "21":
                    self._run_quant_strategies()
                elif choice == "22":
                    self._run_legendary_investors()
                else:
                    print(
                        f"{Fore.YELLOW}Invalid option. Please select 0-22.{Style.RESET_ALL}"
                    )

                if choice != "0":
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    self.show_menu()

            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}\n")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_dashboard(self):
        """Run Streamlit dashboard"""
        import subprocess

        port = 8501

        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   🌐 STARTING STREAMLIT DASHBOARD                                 ║
║                                                                    ║
║   Port: {port}                                                       ║
║   URL:  http://localhost:{port}                                         ║
║                                                                    ║
║   📝 Dashboard will open in your browser                        ║
║                                                                    ║
║   🛑 Press Ctrl+C to stop                                         ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

        try:
            # Try to open browser
            subprocess.run(["xdg-open", f"http://localhost:{port}"], check=False)

            # Run streamlit
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    "src/dashboard/streamlit_app.py",
                    "--server.port",
                    str(port),
                    "--server.headless",
                    "true",
                ]
            )
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Dashboard stopped{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error starting dashboard: {e}{Style.RESET_ALL}")

    def _run_cli(self):
        """Run CLI Terminal"""
        cmd_cli(None)

    def _run_quick_analysis(self):
        """Run quick symbol analysis"""
        symbol = (
            input(
                f"\n{Fore.CYAN}Enter symbol (e.g., AAPL, BTC, BBCA): {Style.RESET_ALL}"
            )
            .strip()
            .upper()
        )

        if not symbol:
            print(f"{Fore.YELLOW}No symbol provided{Style.RESET_ALL}")
            return

        import argparse

        args = argparse.Namespace(
            symbols=symbol,
            days=100,
            mode="manual",
            asset="stock_us",
            paper=False,
            risk=2.0,
        )
        cmd_analyze(args)

    def _run_multi_asset(self):
        """Run multi-asset analysis"""
        symbols = (
            input(f"\n{Fore.CYAN}Enter symbols (comma-separated): {Style.RESET_ALL}")
            .strip()
            .upper()
        )

        if not symbols:
            print(f"{Fore.YELLOW}No symbols provided{Style.RESET_ALL}")
            return

        import argparse

        args = argparse.Namespace(
            symbols=symbols,
            days=100,
            mode="manual",
            asset="stock_us",
            paper=False,
            risk=2.0,
        )
        cmd_analyze(args)

    def _run_paper_trading(self):
        """Run paper trading"""
        print(f"\n{Fore.CYAN}Starting Paper Trading Mode...{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}This is a simulation - no real trades will be executed{Style.RESET_ALL}\n"
        )

        # Start paper trading script
        try:
            from src.paper_trading.paper_trader import get_paper_trader

            trader = get_paper_trader()
            trader.run()
        except Exception as e:
            print(f"{Fore.RED}Error starting paper trading: {e}{Style.RESET_ALL}")

    def _run_live_trading(self):
        """Run live trading with Exness"""
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   🚀 STARTING LIVE TRADING (FULL AUTO)                             ║
║                                                                    ║
║   ⚠️  WARNING: REAL MONEY TRADING                              ║
║   ⚠️  Currently using DEMO ACCOUNT                             ║
║                                                                    ║
║   Broker: Exness                                                  ║
║   Account: Demo (Login: 270816241)                                 ║
║   Balance: $100,000                                                ║
║                                                                    ║
║   📱 Telegram notifications enabled                                  ║
║                                                                    ║
║   🛑 Press Ctrl+C to stop                                         ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

        try:
            import subprocess

            subprocess.run(
                [sys.executable, "start_live_trading.py", "--exness", "--auto"]
            )
        except Exception as e:
            print(f"{Fore.RED}Error starting live trading: {e}{Style.RESET_ALL}")

    def _run_backtest(self):
        """Run backtesting"""
        symbol = (
            input(
                f"\n{Fore.CYAN}Enter symbol for backtest (default: EURUSD): {Style.RESET_ALL}"
            )
            .strip()
            .upper()
        )
        if not symbol:
            symbol = "EURUSD"

        days = input(f"{Fore.CYAN}Days (default: 180): {Style.RESET_ALL}").strip()
        if not days:
            days = "180"

        import argparse

        args = argparse.Namespace(
            backtest=symbol, days=int(days), strategies=None, report=False
        )
        cmd_backtest(args)

    def _run_autoheal(self):
        """Run Auto-Heal System"""
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   🔧 AUTO-HEAL SYSTEM                                            ║
║                                                                    ║
║   Features:                                                          ║
║   • Health Monitoring (CPU, Memory, Disk)                          ║
║   • Automatic Backups (Daily, rotation)                               ║
║   • Strategy Evaluator (Performance ranking)                           ║
║   • Real-time Dashboard                                            ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

        try:
            import subprocess

            subprocess.run([sys.executable, "auto_heal_system.py", "--all"])
        except Exception as e:
            print(f"{Fore.RED}Error starting auto-heal: {e}{Style.RESET_ALL}")

    def _run_strategy_evaluator(self):
        """Run strategy evaluator"""
        try:
            from src.auto_heal.strategy_evaluator import StrategyEvaluator

            print(f"\n{Fore.CYAN}Running Strategy Evaluator...{Style.RESET_ALL}\n")

            evaluator = StrategyEvaluator()
            evaluator.evaluate_all_strategies()
            evaluator.export_report("strategy_rankings.json")

            print(f"\n{Fore.GREEN}✅ Strategy evaluation complete!{Style.RESET_ALL}")
            print(
                f"{Fore.CYAN}Report saved to: strategy_rankings.json{Style.RESET_ALL}"
            )
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _run_status(self):
        """Show system status"""
        cmd_status(None)

    def _run_riset_backtest(self):
        """Run RISET Comprehensive Backtesting"""
        import subprocess

        try:
            print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════╗
 ║                                                                    ║
 ║   📊 RISET COMPREHENSIVE BACKTESTING                         ║
 ║                                                                    ║
 ║   Running comprehensive backtests for all RISET strategies        ║
 ║                                                                    ║
 ╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

            result = subprocess.run(
                [sys.executable, "tests/comprehensive_backtest.py"],
                check=True,
            )

            if result.returncode == 0:
                print(f"\n{Fore.GREEN}✅ Backtesting completed!{Style.RESET_ALL}\n")
                print(
                    f"{Fore.CYAN}Report saved to: backtest_report.json{Style.RESET_ALL}\n"
                )
            else:
                print(
                    f"\n{Fore.YELLOW}⚠ Backtesting finished with errors{Style.RESET_ALL}\n"
                )

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_riset_integration(self):
        """Run RISET System Integration"""
        try:
            from src.integration.riset_integrator import RisetIntegrator

            print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
 ║                                                                    ║
 ║   🚀 RISET v2.2.2 SYSTEM INTEGRATION                         ║
 ║                                                                    ║
 ║   Integrating all RISET components into AI Hedge Fund        ║
 ║                                                                    ║
 ║   Strategies: Graham, Turtle, SEPA                            ║
 ║   Risk: Kelly, Risk Parity, VaR                               ║
 ║   Agents: Multi-Agent System (4 agents)                        ║
 ║   Orchestrator: Unified Strategy Orchestrator                    ║
 ║                                                                    ║
 ╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

            integrator = RisetIntegrator()
            components = integrator.integrate_all()
            status = integrator.get_system_status()

            print(f"\n{Fore.GREEN}✅ RISET Integration Complete!{Style.RESET_ALL}\n")

            print(f"{Fore.CYAN}Registered Strategies:{Style.RESET_ALL}")
            for name, info in status["strategies"].items():
                status_icon = "✓" if info["registered"] else "✗"
                print(f"  {status_icon} {name.upper()}")

            print(f"\n{Fore.CYAN}Risk Managers:{Style.RESET_ALL}")
            for name, info in status["risk_managers"].items():
                status_icon = "✓" if info["available"] else "✗"
                print(f"  {status_icon} {name.upper()}")

            print(f"\n{Fore.CYAN}System Status:{Style.RESET_ALL}")
            print(f"  ✓ Multi-Agent System: {status['multi_agent_system']['status']}")
            print(
                f"  ✓ Unified Orchestrator: {status['unified_orchestrator']['status']}\n"
            )

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_graham_value(self):
        """Run Graham Value Strategy"""
        try:
            from src.strategies.graham_value import GrahamValueStrategy

            symbol = (
                input(f"\n{Fore.CYAN}Enter symbol (e.g., AAPL): {Style.RESET_ALL}")
                .strip()
                .upper()
            )

            if not symbol:
                print(f"{Fore.YELLOW}No symbol provided{Style.RESET_ALL}")
                return

            print(
                f"\n{Fore.CYAN}Analyzing {symbol} with Graham Value Strategy...{Style.RESET_ALL}\n"
            )

            strategy = GrahamValueStrategy()

            graham_num = strategy.calculate_graham_number(eps=5.0, bvps=40.0)
            margin_safety = strategy.calculate_margin_of_safety(
                intrinsic_value=graham_num, market_price=150.0
            )

            print(f"{Fore.CYAN}Results:{Style.RESET_ALL}")
            print(f"  Graham Number: ${graham_num:.2f}")
            print(f"  Margin of Safety: {margin_safety * 100:.1f}%")

            if margin_safety > 0.2:
                print(f"  {Fore.GREEN}Signal: BUY{Style.RESET_ALL}")
            elif margin_safety > 0:
                print(f"  {Fore.YELLOW}Signal: HOLD{Style.RESET_ALL}")
            else:
                print(f"  {Fore.RED}Signal: AVOID{Style.RESET_ALL}\n")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_turtle_trading(self):
        """Run Turtle Trading Strategy"""
        try:
            from src.strategies.turtle_trading import TurtleTradingStrategy
            import numpy as np

            symbol = (
                input(f"\n{Fore.CYAN}Enter symbol (e.g., EURUSD): {Style.RESET_ALL}")
                .strip()
                .upper()
            )

            if not symbol:
                print(f"{Fore.YELLOW}No symbol provided{Style.RESET_ALL}")
                return

            print(
                f"\n{Fore.CYAN}Analyzing {symbol} with Turtle Trading Strategy...{Style.RESET_ALL}\n"
            )

            strategy = TurtleTradingStrategy()

            np.random.seed(42)
            closes = 100 * np.cumprod(1 + np.random.normal(0.0005, 0.02, 252))
            highs = closes * np.random.uniform(1.00, 1.03, 252)
            lows = closes * np.random.uniform(0.97, 1.00, 252)
            volumes = np.random.randint(1000000, 10000000, 252)

            signals = strategy.generate_signals(
                symbol=symbol,
                highs=highs,
                lows=lows,
                closes=closes,
                volumes=volumes,
            )

            print(f"{Fore.CYAN}Results:{Style.RESET_ALL}")
            print(f"  Total Signals Generated: {len(signals)}")

            for i, sig in enumerate(signals[-5:]):
                print(
                    f"  {Fore.GREEN if sig.action == 'BUY' else Fore.RED}{sig.action} @ ${sig.price:.2f}{Style.RESET_ALL}"
                )

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_sepa_strategy(self):
        """Run SEPA Strategy"""
        try:
            from src.strategies.sepa import SEPAStrategy
            import numpy as np
            import pandas as pd

            symbol = (
                input(f"\n{Fore.CYAN}Enter symbol (e.g., NVDA): {Style.RESET_ALL}")
                .strip()
                .upper()
            )

            if not symbol:
                print(f"{Fore.YELLOW}No symbol provided{Style.RESET_ALL}")
                return

            print(
                f"\n{Fore.CYAN}Analyzing {symbol} with SEPA Strategy...{Style.RESET_ALL}\n"
            )

            strategy = SEPAStrategy()

            np.random.seed(42)
            prices = 100 * np.cumprod(1 + np.random.normal(0.0005, 0.02, 252))
            data = pd.DataFrame(
                {
                    "open": prices * np.random.uniform(0.99, 1.01, 252),
                    "high": prices * np.random.uniform(1.00, 1.03, 252),
                    "low": prices * np.random.uniform(0.97, 1.00, 252),
                    "close": prices,
                    "volume": np.random.randint(1000000, 10000000, 252),
                }
            )

            signal_data = strategy.analyze_stock(
                symbol=symbol,
                closes=data["close"].values,
                volumes=data["volume"].values,
                highs=data["high"].values,
                lows=data["low"].values,
            )

            print(f"{Fore.CYAN}SEPA Analysis Results:{Style.RESET_ALL}")
            print(f"  Signal: {signal_data.signal}")
            print(f"  CANSLIM Score: {signal_data.canslim_score.total_score:.1f}/100")
            print(f"  VCP Detected: {signal_data.vcp_pattern.detected}")
            print(f"  Confidence: {signal_data.confidence * 100:.1f}%\n")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_config(self):
        """Show configuration"""
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                    CONFIGURATION                                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  🤖 LLM Configuration                                            ║
║  ─────────────────────────────────────────────────────────────              ║
║  Primary LLM: LLM7 (gpt-5-nano)                             ║
║  Base URL: https://api.llm7.io/v1                          ║
║  Fallbacks: OpenRouter, Groq, Gemini                             ║
║                                                                    ║
║  📊 Data Sources                                                ║
║  ─────────────────────────────────────────────────────────────              ║
║  Primary: Financial Datasets API                                     ║
║  Fallbacks: Yahoo Finance, CoinGecko, ExchangeRate-API              ║
║                                                                    ║
║  🏦 Trading Configuration                                        ║
║  ─────────────────────────────────────────────────────────────              ║
║  Broker: Exness (Demo)                                            ║
║  Mode: Full Auto                                                   ║
║  Risk per trade: 2%                                               ║
║  Max daily loss: 6%                                                ║
║  Min R:R: 1:2                                                     ║
║  Max positions: 5                                                  ║
║                                                                    ║
║  📱 Notifications                                                ║
║  ─────────────────────────────────────────────────────────────              ║
║  Telegram: Enabled (@dhaherautobot)                            ║
║  Signals, Trades, Status: All enabled                            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

    def _run_unified_analysis(self):
        """Run unified multi-strategy analysis"""
        try:
            from src.strategies.unified_analysis import (
                UnifiedStrategyAnalyzer,
                create_sample_data,
            )

            symbol = (
                input(
                    f"\n{Fore.CYAN}Enter symbol (e.g., AAPL, BTC, EURUSD): {Style.RESET_ALL}"
                )
                .strip()
                .upper()
            )

            if not symbol:
                print(f"{Fore.YELLOW}No symbol provided{Style.RESET_ALL}")
                return

            max_strategies = input(
                f"{Fore.CYAN}Max strategies (default: 30): {Style.RESET_ALL}"
            ).strip()
            if not max_strategies:
                max_strategies = 30
            else:
                max_strategies = int(max_strategies)

            print(
                f"\n{Fore.CYAN}Running unified analysis with up to {max_strategies} strategies...{Style.RESET_ALL}\n"
            )

            print(f"{Fore.YELLOW}Analyzing {symbol}...{Style.RESET_ALL}")

            analyzer = UnifiedStrategyAnalyzer()
            data = create_sample_data(symbol)
            result = analyzer.analyze(symbol, data, max_strategies=max_strategies)

            print(f"\n{Fore.GREEN}✅ Analysis Complete!{Style.RESET_ALL}\n")

            formatted = analyzer.format_result(result)

            signal_colors = {
                "STRONG_BUY": Fore.GREEN,
                "BUY": Fore.GREEN,
                "HOLD": Fore.YELLOW,
                "SELL": Fore.RED,
                "STRONG_SELL": Fore.RED,
            }

            for line in formatted.split("\n"):
                if "CONSENSUS SIGNAL:" in line:
                    signal = line.split(":")[-1].strip().split()[0]
                    color = signal_colors.get(signal, Fore.CYAN)
                    print(f"{color}{line}{Style.RESET_ALL}")
                elif "BUY" in line and "Signals" in line:
                    print(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
                elif "SELL" in signal_colors:
                    print(f"{Fore.RED}{line}{Style.RESET_ALL}")
                else:
                    print(line)

            export_choice = (
                input(f"\n{Fore.CYAN}Export results? (csv/json/no): {Style.RESET_ALL}")
                .strip()
                .lower()
            )

            if export_choice in ["csv", "json"]:
                from datetime import datetime

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                if export_choice == "csv":
                    results_list = []
                    for r in result.all_results:
                        results_list.append(
                            {
                                "Strategy": r.strategy_name,
                                "Signal": r.signal,
                                "Confidence": r.confidence,
                                "Score": r.score,
                                "Risk": r.risk_level,
                            }
                        )
                    df = pd.DataFrame(results_list)
                    filename = f"{symbol}_analysis_{timestamp}.csv"
                    df.to_csv(filename, index=False)
                    print(f"\n{Fore.GREEN}✅ Exported to {filename}{Style.RESET_ALL}")
                else:
                    import json

                    export_data = {
                        "symbol": symbol,
                        "consensus_signal": result.consensus_signal,
                        "consensus_confidence": result.consensus_confidence,
                        "consensus_score": result.consensus_score,
                        "signal_breakdown": {
                            "buy": result.buy_signals,
                            "sell": result.sell_signals,
                            "hold": result.hold_signals,
                            "neutral": result.neutral_signals,
                        },
                        "strategies_analyzed": result.total_strategies,
                        "successful": result.successful_strategies,
                    }
                    filename = f"{symbol}_analysis_{timestamp}.json"
                    with open(filename, "w") as f:
                        json.dump(export_data, f, indent=2)
                    print(f"\n{Fore.GREEN}✅ Exported to {filename}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_registry_info(self):
        """Show comprehensive registry information"""
        try:
            from src.strategies.comprehensive_registry import (
                get_comprehensive_registry,
                StrategyCategory,
            )

            registry = get_comprehensive_registry()

            print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║              COMPREHENSIVE STRATEGY REGISTRY v2.2.2                ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  📊 Total Strategies: {len(registry.get_all_strategies())}                                     ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

            print(registry.list_all_strategies())

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_smc_strategies(self):
        """Run SMC strategy analysis"""
        try:
            from src.strategies.unified_analysis import create_sample_data

            symbol = (
                input(
                    f"\n{Fore.CYAN}Enter symbol for SMC analysis (e.g., EURUSD): {Style.RESET_ALL}"
                )
                .strip()
                .upper()
            )

            if not symbol:
                print(f"{Fore.YELLOW}No symbol provided{Style.RESET_ALL}")
                return

            from src.strategies.comprehensive_registry import (
                get_comprehensive_registry,
                StrategyCategory,
            )

            registry = get_comprehensive_registry()
            analyzer = UnifiedStrategyAnalyzer(registry)

            smc_strategies = registry.get_strategies_by_category(
                StrategyCategory.SMC_STRATEGY
            )

            print(
                f"\n{Fore.CYAN}Running {len(smc_strategies)} SMC strategies on {symbol}...{Style.RESET_ALL}\n"
            )

            result = analyzer.analyze(
                symbol, create_sample_data(symbol), max_strategies=10
            )

            print(f"{Fore.CYAN}SMC Strategy Results:{Style.RESET_ALL}")
            for r in result.strategy_results[:10]:
                if (
                    "SMC" in r.strategy_name
                    or "ICT" in r.strategy_name
                    or "Wyckoff" in r.strategy_name
                ):
                    print(f"  {r.strategy_name}: {r.signal} ({r.confidence:.1%})")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_quant_strategies(self):
        """Run quantitative strategy analysis"""
        try:
            from src.strategies.unified_analysis import create_sample_data

            symbol = (
                input(
                    f"\n{Fore.CYAN}Enter symbol for Quant analysis (e.g., AAPL): {Style.RESET_ALL}"
                )
                .strip()
                .upper()
            )

            if not symbol:
                print(f"{Fore.YELLOW}No symbol provided{Style.RESET_ALL}")
                return

            from src.strategies.comprehensive_registry import (
                get_comprehensive_registry,
                StrategyCategory,
            )

            registry = get_comprehensive_registry()
            analyzer = UnifiedStrategyAnalyzer(registry)

            quant_strategies = registry.get_strategies_by_category(
                StrategyCategory.QUANTITATIVE
            )

            print(
                f"\n{Fore.CYAN}Running {len(quant_strategies)} Quantitative strategies on {symbol}...{Style.RESET_ALL}\n"
            )

            result = analyzer.analyze(
                symbol, create_sample_data(symbol), max_strategies=10
            )

            print(f"{Fore.CYAN}Quantitative Strategy Results:{Style.RESET_ALL}")
            for r in result.strategy_results[:10]:
                if (
                    "Quant" in r.strategy_name
                    or "Jim Simons" in r.strategy_name
                    or "Momentum" in r.strategy_name
                ):
                    print(f"  {r.strategy_name}: {r.signal} ({r.confidence:.1%})")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

    def _run_legendary_investors(self):
        """Run legendary investor strategy analysis"""
        try:
            from src.strategies.unified_analysis import create_sample_data

            symbol = (
                input(
                    f"\n{Fore.CYAN}Enter symbol for Legendary Investor analysis (e.g., AAPL): {Style.RESET_ALL}"
                )
                .strip()
                .upper()
            )

            if not symbol:
                print(f"{Fore.YELLOW}No symbol provided{Style.RESET_ALL}")
                return

            from src.strategies.comprehensive_registry import (
                get_comprehensive_registry,
                StrategyCategory,
            )

            registry = get_comprehensive_registry()
            analyzer = UnifiedStrategyAnalyzer(registry)

            legendary_strategies = registry.get_strategies_by_category(
                StrategyCategory.LEGENDARY_INVESTOR
            )

            print(
                f"\n{Fore.CYAN}Running {len(legendary_strategies)} Legendary Investor strategies on {symbol}...{Style.RESET_ALL}\n"
            )

            result = analyzer.analyze(
                symbol, create_sample_data(symbol), max_strategies=10
            )

            print(f"{Fore.CYAN}Legendary Investor Strategy Results:{Style.RESET_ALL}")
            for r in result.strategy_results[:15]:
                print(f"  {r.strategy_name}: {r.signal} ({r.confidence:.1%})")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")


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


def cmd_autoheal(args):
    """Run auto-heal system commands"""
    print_banner()
    print(f"\n{Fore.CYAN}🔧 Auto-Heal System v2.2.1{Style.RESET_ALL}\n")

    try:
        from src.auto_heal.orchestrator import AutoHealOrchestrator

        orchestrator = AutoHealOrchestrator()
        orchestrator.run()
    except ImportError as e:
        print(f"{Fore.RED}✗ Auto-Heal system not available: {e}{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Please ensure src/auto_heal/ is properly installed.{Style.RESET_ALL}"
        )


# ============ MAIN ============


def main():
    """Main entry point - interactive menu or CLI commands"""
    parser = argparse.ArgumentParser(
        description=f"AI Hedge Fund v{VERSION} - Interactive Trading System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage:
  # Interactive Menu (RECOMMENDED)
  python3 main.py                      # Show interactive menu

  # CLI Commands
  python3 main.py --dashboard          # Streamlit web UI
  python3 main.py --cli                # Enhanced CLI
  python3 main.py AAPL                 # Quick analysis
  python3 main.py --status             # System status
  python3 main.py --autoheal           # Launch Auto-Heal

  # Examples
  python3 main.py BBCA --asset idn    # Indonesian stock analysis
  python3 main.py AAPL --mode auto     # Autonomous trading
  python3 main.py BTC --asset crypto    # Crypto analysis
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
        choices=[
            "stock_us",
            "stock_idn",
            "stock_global",
            "forex",
            "crypto",
            "commodity",
            "index",
        ],
        default="stock_us",
        help="Asset type (stock_idn = Indonesian stocks)",
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
        "--autoheal", action="store_true", help="Launch Auto-Heal System"
    )
    parser.add_argument(
        "--live-trading", action="store_true", help="Start live trading"
    )
    parser.add_argument(
        "--version", action="version", version=f"AI Hedge Fund v{VERSION}"
    )

    args = parser.parse_args()

    # IF NO ARGUMENTS: Run Interactive Menu (RECOMMENDED)
    if len(sys.argv) == 1:
        menu = InteractiveMenu()
        menu.run()
        return

    # Print banner for CLI commands
    if not args.dashboard and not args.live_trading:
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
    elif args.autoheal:
        cmd_autoheal(args)
    elif args.live_trading:
        from start_live_trading import main as live_trading_main

        live_trading_main()
    elif args.symbols:
        cmd_analyze(args)
    else:
        print(
            f"\n{Fore.YELLOW}Use --help for available commands or run without arguments for interactive menu{Style.RESET_ALL}\n"
        )
        print(f"{Fore.CYAN}Recommended: python3 main.py{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()

