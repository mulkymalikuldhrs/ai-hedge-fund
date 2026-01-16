#!/usr/bin/env python3
"""
AI HEDGE FUND v2.2 - INTERACTIVE LAUNCHER
=========================================

Complete interactive launcher with menu system for:
- Web Dashboard (Streamlit)
- CLI Terminal
- Backtesting
- Paper Trading
- System Status
- Configuration

Usage:
    python3 launcher.py                    # Interactive menu
    python3 launcher.py --dashboard        # Direct launch
    python3 launcher.py --cli              # Direct CLI
    python3 launcher.py --backtest AAPL    # Direct backtest
"""

import sys
import os
import time
import threading
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

try:
    from colorama import Fore, Style, init

    init(autoreset=True)
except ImportError:

    class Fore:
        CYAN = "\033[96m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        WHITE = "\033[97m"
        RESET = "\033[0m"

    class Style:
        BRIGHT = "\033[1m"
        RESET_ALL = "\033[0m"

    def init(autoreset=False):
        pass


VERSION = "2.2.0"
BUILD_DATE = "2026-01-16"


class InteractiveLauncher:
    """Interactive menu-driven launcher"""

    def __init__(self):
        self.system_status = {}
        self.running = True

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print_banner(self):
        self.clear_screen()
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   🤖 AI HEDGE FUND v{VERSION} - INTERACTIVE LAUNCHER                                ║
║                                                                                      ║
║   ───────────────────────────────────────────────────────────────────────────────   ║
║                                                                                      ║
║   {Fore.WHITE}OPTIONS:{Style.RESET_ALL}                                                                         ║
║                                                                                      ║
║   {Fore.GREEN}[1]{Style.RESET_ALL} 🌐  Web Dashboard     Streamlit UI with real-time monitoring           ║
║   {Fore.GREEN}[2]{Style.RESET_ALL} 💻  CLI Terminal       Interactive command-line interface             ║
║   {Fore.GREEN}[3]{Style.RESET_ALL} 📊  Backtest           Run strategy backtesting                        ║
║   {Fore.GREEN}[4]{Style.RESET_ALL} 📝  Paper Trading     Simulation mode without real money              ║
║   {Fore.GREEN}[5]{Style.RESET_ALL} 📈  Quick Analysis    Analyze single or symbols             ║
║   {Fore.GREEN}[6]{Style.RESET_ALL} 🔧  System Status     Check all components and connections           ║
║   {Fore.GREEN}[7]{Style.RESET_ALL} ⚙️  Configuration     System settings and parameters                ║
║   {Fore.GREEN}[8]{Style.RESET_ALL} ℹ️   Help              Show help and documentation                   ║
║                                                                                      ║
║   {Fore.YELLOW}[0]{Style.RESET_ALL} 🚪  Exit              Quit the launcher                              ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

    def print_status_bar(self):
        print(f"""
{Fore.CYAN}{"─" * 80}{Style.RESET_ALL}
  {Fore.WHITE}Version:{Style.RESET_ALL} {VERSION}  |  {Fore.WHITE}Build:{Style.RESET_ALL} {BUILD_DATE}  |  {Fore.WHITE}Python:{Style.RESET_ALL} {sys.version.split()[0]}  |  {Fore.WHITE}Time:{Style.RESET_ALL} {datetime.now().strftime("%H:%M:%S")}
{Fore.CYAN}{"─" * 80}{Style.RESET_ALL}
        """)

    def check_system_status(self):
        """Check all system components"""
        status = {}

        # Memory System
        try:
            from src.memory.enhanced_memory_system import get_memory_system

            mem = get_memory_system()
            s = mem.get_system_status()
            status["memory"] = ("✓ Ready", Fore.GREEN)
        except Exception as e:
            status["memory"] = (f"✗ Error", Fore.RED)

        # Trading Plan
        try:
            from src.trading_plan.trading_plan import get_trading_plan_manager

            plan = get_trading_plan_manager()
            status["trading_plan"] = (f"✓ {plan.plan.name}", Fore.GREEN)
        except Exception as e:
            status["trading_plan"] = ("✗ Error", Fore.RED)

        # Data Provider
        try:
            from src.data.free_data_provider import get_free_data_provider

            dp = get_free_data_provider()
            symbols = len(dp.get_supported_symbols())
            status["data_provider"] = (f"✓ {symbols} symbols", Fore.GREEN)
        except Exception as e:
            status["data_provider"] = ("✗ Error", Fore.RED)

        # MetaTrader Bridge
        try:
            from src.execution.metatrader_bridge import get_metatrader_bridge

            mt = get_metatrader_bridge(simulate=True)
            status["mt_bridge"] = ("✓ Simulator", Fore.GREEN)
        except Exception as e:
            status["mt_bridge"] = ("✗ Error", Fore.RED)

        # ML Generator
        try:
            from src.ml.ml_signal_generator import get_ml_signal_generator

            ml = get_ml_signal_generator()
            ml.initialize()
            status["ml_generator"] = ("✓ 3 models", Fore.GREEN)
        except Exception as e:
            status["ml_generator"] = ("⚠ Unavailable", Fore.YELLOW)

        # Backtesting
        try:
            from src.backtesting.backtest_engine import get_backtest_engine

            status["backtesting"] = ("✓ Ready", Fore.GREEN)
        except Exception as e:
            status["backtesting"] = ("✗ Error", Fore.RED)

        # Paper Trading
        try:
            from src.paper_trading.paper_trader import get_paper_trader

            pt = get_paper_trader()
            p = pt.get_portfolio_summary()
            status["paper_trading"] = (f"✓ ${p.total_equity:,.0f}", Fore.GREEN)
        except Exception as e:
            status["paper_trading"] = ("⚠ Unavailable", Fore.YELLOW)

        self.system_status = status
        return status

    def launch_dashboard(self):
        """Launch Streamlit dashboard"""
        print(f"\n{Fore.CYAN}🌐 LAUNCHING WEB DASHBOARD...{Style.RESET_ALL}\n")

        dashboard_path = (
            Path(__file__).parent / "src" / "dashboard" / "streamlit_app.py"
        )

        if not dashboard_path.exists():
            print(f"{Fore.RED}✗ Dashboard not found!{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return

        url = "http://localhost:8501"

        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                    🌐 STREAMLIT DASHBOARD v{VERSION}                  ║
╠════════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  🚀 Starting at: {Fore.GREEN}{url}{Style.RESET_Fore.CYAN}                                 ║
║                                                                    ║
║  📝 Browser will open automatically when server is ready           ║
║  📍 Or manually navigate to: {Fore.WHITE}{url}{Style.RESET_Fore.CYAN}                     ║
║                                                                    ║
║  🛑 Press Ctrl+C to stop                                           ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """)

        import urllib.request

        def wait_and_open():
            for i in range(15):
                try:
                    urllib.request.urlopen(url, timeout=1)
                    break
                except:
                    time.sleep(1)

            try:
                subprocess.run(["xdg-open", url], check=False)
                print(f"\n{Fore.GREEN}✅ Browser opened at {url}{Style.RESET_ALL}\n")
            except:
                print(
                    f"\n{Fore.YELLOW}⚠ Could not open browser. Navigate to: {url}{Style.RESET_ALL}\n"
                )

        browser_thread = threading.Thread(target=wait_and_open)
        browser_thread.start()

        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    str(dashboard_path),
                    "--server.port",
                    "8501",
                    "--server.headless",
                    "true",
                ]
            )
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}🛑 Dashboard stopped{Style.RESET_ALL}")

    def launch_cli(self):
        """Launch enhanced CLI terminal"""
        print(f"\n{Fore.CYAN}💻 LAUNCHING CLI TERMINAL...{Style.RESET_ALL}\n")
        from src.dashboard.cli_terminal import CLITerminal

        terminal = CLITerminal()
        terminal.run()

    def launch_backtest(self):
        """Run backtest with interactive prompts"""
        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                       📊 BACKTEST MODULE                        ║
╚════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

        symbol = (
            input(
                f"  {Fore.WHITE}Enter symbol (e.g., EURUSD, AAPL, BTC): {Style.RESET_ALL}"
            )
            .strip()
            .upper()
        )

        if not symbol:
            print(f"\n{Fore.YELLOW}⚠ Cancelled{Style.RESET_ALL}\n")
            return

        days_input = input(
            f"  {Fore.WHITE}Enter days (default 180): {Style.RESET_ALL}"
        ).strip()
        days = int(days_input) if days_input else 180

        print(
            f"\n{Fore.CYAN}⚙️ Running backtest for {symbol} ({days} days)...{Style.RESET_ALL}\n"
        )

        try:
            from src.data.free_data_provider import get_free_data_provider
            from src.backtesting.backtest_engine import get_backtest_engine
            import pandas as pd

            dp = get_free_data_provider()
            data = dp.get_historical_data(symbol, days=days + 30)

            if not data or len(data) < 50:
                print(f"{Fore.RED}✗ Insufficient data for {symbol}{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
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
            results = engine.run_backtest(df, symbol, "EMA Strategy", days=days)

            print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                      BACKTEST RESULTS                           ║
╠════════════════════════════════════════════════════════════════╣
║  Symbol:           {results.symbol:<20} Period: {results.period_days} days    ║
║  Initial Capital:  ${results.initial_capital:>12,.2f}                            ║
║  Final Capital:    ${results.final_capital:>12,.2f}                            ║
║  Total Return:     {results.total_return_pct:>12.2f}%                            ║
╠════════════════════════════════════════════════════════════════╣
║  Total Trades:     {results.total_trades:<20} Win Rate: {results.win_rate:.1f}%    ║
║  Profit Factor:    {results.profit_factor:<20} Sharpe: {results.sharpe_ratio:.2f}       ║
╠════════════════════════════════════════════════════════════════╣
║  Max Drawdown:     {results.max_drawdown_pct:>12.2f}%                            ║
║  Avg Win:          ${results.avg_win:>12,.2f}                            ║
║  Avg Loss:         ${results.avg_loss:>12,.2f}                            ║
╚════════════════════════════════════════════════════════════════╝
Time: {results.execution_time_seconds:.2f}s
            """)

        except Exception as e:
            print(f"{Fore.RED}✗ Backtest error: {e}{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def launch_paper_trading(self):
        """Run paper trading simulation"""
        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                     📝 PAPER TRADING MODULE                      ║
╚════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

        symbol = (
            input(f"  {Fore.WHITE}Enter symbol to trade: {Style.RESET_ALL}")
            .strip()
            .upper()
        )

        if not symbol:
            print(f"\n{Fore.YELLOW}⚠ Cancelled{Style.RESET_ALL}\n")
            return

        action = (
            input(f"  {Fore.WHITE}Action (buy/sell): {Style.RESET_ALL}").strip().lower()
        )

        try:
            from src.paper_trading.paper_trader import get_paper_trader
            from src.data.free_data_provider import get_free_data_provider

            trader = get_paper_trader()
            dp = get_free_data_provider()

            price = dp.get_current_price(symbol)
            if price.current_price <= 0:
                print(f"{Fore.RED}✗ Could not get price for {symbol}{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                return

            quantity = input(f"  {Fore.WHITE}Quantity: {Style.RESET_ALL}").strip()
            quantity = float(quantity) if quantity else 1.0

            order = trader.create_order(
                symbol, action, "market", quantity, price.current_price
            )
            result = trader.execute_order(order.order_id, price.current_price)

            portfolio = trader.get_portfolio_summary()

            print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                      PAPER TRADE RESULT                          ║
╠════════════════════════════════════════════════════════════════╣
║  Symbol:      {symbol:<15} Action: {action.upper()}                         ║
║  Price:       ${price.current_price:<12,.2f} Quantity: {quantity:<10.1f}        ║
║  Order:       {result.status:<15} Filled: ${result.filled_price:<10.2f}        ║
╠════════════════════════════════════════════════════════════════╣
║  Portfolio Equity:  ${portfolio.total_equity:>10,.2f}                          ║
║  Cash Balance:      ${portfolio.cash_balance:>10,.2f}                          ║
║  Open Positions:    {portfolio.open_positions:<10}                              ║
╚════════════════════════════════════════════════════════════════╝
            """)

        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def quick_analysis(self):
        """Quick symbol analysis"""
        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                      📈 QUICK ANALYSIS MODULE                     ║
╚════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

        symbols_input = (
            input(f"  {Fore.WHITE}Enter symbols (comma-separated): {Style.RESET_ALL}")
            .strip()
            .upper()
        )

        if not symbols_input:
            print(f"\n{Fore.YELLOW}⚠ Cancelled{Style.RESET_ALL}\n")
            return

        symbols = [s.strip() for s in symbols_input.split(",")]

        try:
            from src.data.free_data_provider import get_free_data_provider
            from src.ml.ml_signal_generator import get_ml_signal_generator
            import pandas as pd

            dp = get_free_data_provider()

            print(
                f"\n{Fore.CYAN}┌──────────┬────────────┬──────────┬────────┬────────┬────────┐{Style.RESET_ALL}"
            )
            print(
                f"{Fore.CYAN}│ Symbol   │ Price      │ Change   │ RSI    │ Signal │ Trend  │{Style.RESET_ALL}"
            )
            print(
                f"{Fore.CYAN}├──────────┼────────────┼──────────┼────────┼────────┼────────┤{Style.RESET_ALL}"
            )

            for symbol in symbols:
                price = dp.get_current_price(symbol)
                data = dp.get_historical_data(symbol, days=100)

                if price.current_price > 0 and data:
                    df = pd.DataFrame(
                        [
                            {
                                "open": o.open,
                                "high": o.high,
                                "low": o.low,
                                "close": o.close,
                            }
                            for o in data
                        ]
                    )

                    close = df["close"].iloc[-1]
                    sma20 = df["close"].rolling(20).mean().iloc[-1]
                    delta = df["close"].diff()
                    gain = delta.where(delta > 0, 0).rolling(14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                    rs = gain / (loss + 1e-10)
                    rsi = 100 - (100 / (1 + rs)).iloc[-1]

                    change = price.daily_change_pct
                    change_color = Fore.GREEN if change >= 0 else Fore.RED

                    if close > sma20 and rsi < 70:
                        signal = "BUY"
                        signal_color = Fore.GREEN
                    elif close < sma20 and rsi > 30:
                        signal = "SELL"
                        signal_color = Fore.RED
                    else:
                        signal = "HOLD"
                        signal_color = Fore.YELLOW

                    trend = "BULLISH" if close > sma20 else "BEARISH"
                    trend_color = Fore.GREEN if trend == "BULLISH" else Fore.RED

                    print(
                        f"{Fore.CYAN}│{Style.RESET_ALL} {symbol:8s} │ ${price.current_price:>10,.2f} │ {change_color}{change:>+7.2f}%{Style.RESET_ALL} │ {rsi:>6.1f} │{signal_color} {signal:<6}{Style.RESET_ALL} │{trend_color} {trend:<7}{Style.RESET_ALL} │"
                    )

            print(
                f"{Fore.CYAN}└──────────┴────────────┴──────────┴────────┴────────┴────────┘{Style.RESET_ALL}\n"
            )

        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def show_system_status(self):
        """Show detailed system status"""
        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                        🔧 SYSTEM STATUS                            ║
╚════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

        status = self.check_system_status()

        print(
            f"{Fore.CYAN}┌────────────────────────────────────────────────────────────┐{Style.RESET_ALL}"
        )
        print(
            f"{Fore.CYAN}│{Style.RESET_ALL} Component                Status                         {Fore.CYAN}│{Style.RESET_ALL}"
        )

        for name, (text, color) in status.items():
            display_name = name.replace("_", " ").title()
            print(
                f"{Fore.CYAN}│{Style.RESET_ALL} {display_name:<23} {color}{text:<30}{Style.RESET_ALL} {Fore.CYAN}│{Style.RESET_ALL}"
            )

        print(
            f"{Fore.CYAN}└────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n"
        )

        print(f"""
{Fore.WHITE}System Information:{Style.RESET_ALL}
  Version:    {VERSION}
  Build:      {BUILD_DATE}
  Python:     {sys.version.split()[0]}
  Working Dir: {os.getcwd()}

{Fore.WHITE}Available Commands:{Style.RESET_ALL}
  --dashboard  Launch web dashboard
  --cli        Launch CLI terminal
  --backtest   Run backtest
  --paper      Paper trading
  --analyze    Quick analysis
  --status     System status
  --help       Show help
        """)

        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def show_configuration(self):
        """Show and edit configuration"""
        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                       ⚙️ CONFIGURATION                            ║
╚════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

        config = {
            "Default Risk %": "2.0",
            "Trading Mode": "semi-auto",
            "Data Provider": "Yahoo/Coingecko/ExchangeRate",
            "MetaTrader": "Simulator (Browser Automation)",
            "ML Models": "Random Forest, XGBoost, LSTM",
            "Backtesting Period": "180 days",
            "Commission": "0.1%",
            "Slippage": "0.05%",
        }

        print(
            f"{Fore.CYAN}┌────────────────────────────────────────────────────────────┐{Style.RESET_ALL}"
        )
        print(
            f"{Fore.CYAN}│{Style.RESET_ALL} Setting                     Value                          {Fore.CYAN}│{Style.RESET_ALL}"
        )
        print(
            f"{Fore.CYAN}├────────────────────────────────────────────────────────────┤{Style.RESET_ALL}"
        )

        for key, value in config.items():
            print(
                f"{Fore.CYAN}│{Style.RESET_ALL} {key:<25} {value:<32} {Fore.CYAN}│{Style.RESET_ALL}"
            )

        print(
            f"{Fore.CYAN}└────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n"
        )

        print(
            f"{Fore.YELLOW}Note: Configuration editing coming in v2.3{Style.RESET_ALL}\n"
        )
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def show_help(self):
        """Show help"""
        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                           ℹ️ HELP                                    ║
╚════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.WHITE}USAGE:{Style.RESET_ALL}
    python3 launcher.py              Interactive menu (this interface)
    python3 launcher.py --dashboard  Launch Streamlit dashboard directly
    python3 launcher.py --cli        Launch CLI terminal directly
    python3 launcher.py --backtest AAPL  Run backtest directly

{Fore.WHITE}OPTIONS:{Style.RESET_ALL}
    -d, --dashboard    Launch web dashboard
    -c, --cli          Launch CLI terminal
    -b, --backtest     Run backtest (symbol optional)
    -p, --paper        Paper trading simulation
    -a, --analyze      Quick analysis
    -s, --status       System status
    -h, --help         Show this help

{Fore.WHITE}EXAMPLES:{Style.RESET_ALL}
    python3 launcher.py                           # Interactive menu
    python3 launcher.py --dashboard               # Web UI
    python3 launcher.py --cli                     # CLI
    python3 launcher.py --backtest EURUSD         # Backtest
    python3 launcher.py --backtest AAPL --days 90 # Custom backtest

{Fore.WHITE}FEATURES:{Style.RESET_ALL}
    • 34+ Trading Strategies
    • ML Signal Generator (RF, XGBoost, LSTM)
    • Free Data Sources (Yahoo, CoinGecko, ExchangeRate)
    • Paper Trading Simulation
    • Walk-Forward Backtesting
    • MetaTrader Browser Automation

{Fore.WHITE}TROUBLESHOOTING:{Style.RESET_ALL}
    • If dashboard fails: Check if port 8501 is available
    • If data not loading: Check internet connection
    • If ML fails: Install sklearn, xgboost, tensorflow

{Fore.WHITE}VERSION:{Style.RESET_ALL} {VERSION} ({BUILD_DATE})
        """)

        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def run(self):
        """Main menu loop"""
        while self.running:
            self.print_banner()
            self.print_status_bar()

            choice = input(f"\n{Fore.CYAN}HF {Fore.WHITE}➜{Style.RESET_ALL} ").strip()

            if choice == "1" or choice.lower() in ["dashboard", "d"]:
                self.launch_dashboard()
            elif choice == "2" or choice.lower() in ["cli", "c"]:
                self.launch_cli()
            elif choice == "3" or choice.lower() in ["backtest", "b"]:
                self.launch_backtest()
            elif choice == "4" or choice.lower() in ["paper", "p"]:
                self.launch_paper_trading()
            elif choice == "5" or choice.lower() in ["analyze", "a"]:
                self.quick_analysis()
            elif choice == "6" or choice.lower() in ["status", "s"]:
                self.show_system_status()
            elif choice == "7" or choice.lower() in ["config", "cfg"]:
                self.show_configuration()
            elif choice == "8" or choice.lower() in ["help", "h", "?"]:
                self.show_help()
            elif choice in ["0", "exit", "quit"]:
                print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}\n")
                self.running = False
            else:
                print(f"\n{Fore.YELLOW}⚠ Invalid option: {choice}{Style.RESET_ALL}\n")


def direct_launch(args):
    """Handle direct command-line launches"""
    # Add short form attributes if not present
    if not hasattr(args, "d"):
        args.d = False
    if not hasattr(args, "c"):
        args.c = False
    if not hasattr(args, "b"):
        args.b = False
    if not hasattr(args, "p"):
        args.p = False
    if not hasattr(args, "a"):
        args.a = False
    if not hasattr(args, "s"):
        args.s = False
    if not hasattr(args, "h"):
        args.h = False
    if not hasattr(args, "v"):
        args.v = False

    if args.dashboard or args.d:
        launch_dashboard_direct(args)
    elif args.cli or args.c:
        launch_cli_direct(args)
    elif args.backtest or args.b:
        launch_backtest_direct(args)
    elif args.paper or args.p:
        launch_paper_direct(args)
    elif args.analyze or args.a:
        launch_analyze_direct(args)
    elif args.status or args.s:
        show_status_direct(args)
    elif args.help or args.h:
        show_help_direct(args)
    elif args.version or args.v:
        print(f"AI Hedge Fund v{VERSION}")


def launch_dashboard_direct(args):
    """Direct dashboard launch"""
    url = "http://localhost:8501"
    print(f"{Fore.CYAN}🌐 Starting dashboard at {url}{Style.RESET_ALL}")

    dashboard_path = Path(__file__).parent / "src" / "dashboard" / "streamlit_app.py"

    def wait_and_open():
        import urllib.request

        for i in range(15):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except:
                time.sleep(1)
        try:
            subprocess.run(["xdg-open", url], check=False)
        except:
            pass

    threading.Thread(target=wait_and_open).start()

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(dashboard_path),
                "--server.port",
                "8501",
            ]
        )
    except KeyboardInterrupt:
        pass


def launch_cli_direct(args):
    """Direct CLI launch"""
    from src.dashboard.cli_terminal import CLITerminal

    terminal = CLITerminal()
    terminal.run()


def launch_backtest_direct(args):
    """Direct backtest launch"""
    symbol = args.backtest if args.backtest else "EURUSD"
    days = getattr(args, "days", 180)

    print(f"{Fore.CYAN}📊 Running backtest for {symbol} ({days} days){Style.RESET_ALL}")

    try:
        from src.data.free_data_provider import get_free_data_provider
        from src.backtesting.backtest_engine import get_backtest_engine
        import pandas as pd

        dp = get_free_data_provider()
        data = dp.get_historical_data(symbol, days=days + 30)

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

            engine = get_backtest_engine()
            results = engine.run_backtest(df, symbol, "Strategy", days=days)

            print(
                f"\n{Fore.GREEN}Return: {results.total_return_pct:.2f}% | Trades: {results.total_trades} | Win: {results.win_rate:.1f}%{Style.RESET_ALL}"
            )
            print(
                f"Sharpe: {results.sharpe_ratio:.2f} | Max DD: {results.max_drawdown_pct:.2f}%"
            )
        else:
            print(f"{Fore.RED}No data for {symbol}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def launch_paper_direct(args):
    """Direct paper trading"""
    print(f"{Fore.CYAN}📝 Paper trading - use interactive mode{Style.RESET_ALL}")


def launch_analyze_direct(args):
    """Direct analysis"""
    print(f"{Fore.CYAN}📈 Quick analysis - use interactive mode{Style.RESET_ALL}")


def show_status_direct(args):
    """Direct status"""
    launcher = InteractiveLauncher()
    launcher.check_system_status()
    print(f"{Fore.GREEN}System check complete!{Style.RESET_ALL}")


def show_help_direct(args):
    """Direct help"""
    print(f"""
{Fore.CYAN}AI HEDGE FUND v{VERSION} - HELP{Style.RESET_ALL}

USAGE:
    python3 launcher.py              Interactive menu
    python3 launcher.py --dashboard  Web dashboard
    python3 launcher.py --cli        CLI terminal
    python3 launcher.py --backtest SYM  Backtest

OPTIONS:
    -d, --dashboard   Launch web dashboard
    -c, --cli         Launch CLI
    -b, --backtest    Run backtest
    -p, --paper       Paper trading
    -a, --analyze     Quick analysis
    -s, --status      System status
    -h, --help        This help
    -v, --version     Version info
    """)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description=f"AI Hedge Fund v{VERSION} - Interactive Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "--dashboard", "-d", action="store_true", help="Launch web dashboard"
    )
    parser.add_argument("--cli", "-c", action="store_true", help="Launch CLI terminal")
    parser.add_argument(
        "--backtest", "-b", nargs="?", const="EURUSD", help="Run backtest"
    )
    parser.add_argument("--paper", "-p", action="store_true", help="Paper trading")
    parser.add_argument("--analyze", "-a", action="store_true", help="Quick analysis")
    parser.add_argument("--status", "-s", action="store_true", help="System status")
    parser.add_argument("--help", "-h", action="store_true", help="Show help")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")

    args, _ = parser.parse_known_args()

    if args.help:
        show_help_direct(args)
    elif args.version:
        print(f"AI Hedge Fund v{VERSION}")
    elif any(
        [
            args.dashboard,
            args.cli,
            args.backtest,
            args.paper,
            args.analyze,
            args.status,
        ]
    ):
        direct_launch(args)
    else:
        launcher = InteractiveLauncher()
        launcher.run()


if __name__ == "__main__":
    main()
