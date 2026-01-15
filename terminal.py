#!/usr/bin/env python3
"""
AI Hedge Fund - Interactive Terminal
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from colorama import Fore, Style, init, Back
init(autoreset=True)

# Icons
ICONS = {
    "bull": f"{Fore.GREEN}🐂{Style.RESET_ALL}",
    "bear": f"{Fore.RED}🐻{Style.RESET_ALL}",
    "neutral": f"{Fore.YELLOW}⚖️{Style.RESET_ALL}",
    "buy": f"{Fore.GREEN}✅{Style.RESET_ALL}",
    "sell": f"{Fore.RED}❌{Style.RESET_ALL}",
    "hold": f"{Fore.YELLOW}⏸️{Style.RESET_ALL}",
    "stock": f"{Fore.CYAN}📈{Style.RESET_ALL}",
    "crypto": f"{Fore.YELLOW}🪙{Style.RESET_ALL}",
    "forex": f"{Fore.MAGENTA}💱{Style.RESET_ALL}",
    "commodity": f"{Fore.RED}🥇{Style.RESET_ALL}",
    "brain": f"{Fore.MAGENTA}🧠{Style.RESET_ALL}",
    "chart": f"{Fore.CYAN}📊{Style.RESET_ALL}",
    "money": f"{Fore.GREEN}💰{Style.RESET_ALL}",
    "rocket": f"{Fore.YELLOW}🚀{Style.RESET_ALL}",
    "check": f"{Fore.GREEN}✓{Style.RESET_ALL}",
    "cross": f"{Fore.RED}✗{Style.RESET_ALL}",
}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def title(text):
    """Display centered title"""
    width = 60
    padding = (width - len(text)) // 2
    print(f"{Fore.CYAN}{'═' * width}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{' ' * padding}{text}{' ' * (width - padding - len(text) - 2)}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * width}{Style.RESET_ALL}")


def menu(title_text, options, footer=""):
    """Display menu"""
    clear()
    title("🤖 AI HEDGE FUND TERMINAL")
    print()
    
    for i, option in enumerate(options, 1):
        icon = option.get("icon", "•")
        desc = option.get("desc", "")
        text = option.get("text", "")
        print(f"  {Fore.GREEN}{i}{Style.RESET_ALL} {icon} {text}")
        if desc:
            print(f"     {Fore.BLUE}{desc}{Style.RESET_ALL}")
    
    print()
    if footer:
        print(f"  {Fore.WHITE}{footer}{Style.RESET_ALL}")
    print()
    
    while True:
        try:
            choice = input(f"  {Fore.CYAN}➜ {Style.RESET_ALL}").strip()
            if choice:
                return int(choice)
        except:
            pass


def input_text(prompt, default=""):
    """Get text input"""
    if default:
        result = input(f"  {Fore.CYAN}{prompt} [{default}]: {Style.RESET_ALL}").strip()
        return result if result else default
    else:
        return input(f"  {Fore.CYAN}{prompt}: {Style.RESET_ALL}").strip()


def loading(text, duration=2):
    """Show loading animation"""
    print(f"\n  {Fore.YELLOW}{text}...{Style.RESET_ALL}")
    chars = "▁▂▃▄▅▆▇█"
    for _ in range(duration * 10):
        for char in chars:
            print(f"  {Fore.CYAN}{char}{Style.RESET_ALL}", end="\r")
            time.sleep(0.05)
    print("  " + " " * 20 + "\r")


def show_status(data):
    """Show real-time status"""
    print(f"""
  {Fore.CYAN}┌{'─' * 56}┐{Style.RESET_ALL}
  {Fore.CYAN}│{Style.RESET_ALL} {Fore.WHITE}MARKET STATUS{Style.RESET_ALL}{' ' * 42}│
  {Fore.CYAN}├{'─' * 56}┤{Style.RESET_ALL}
  {Fore.CYAN}│{Style.RESET_ALL}  {ICONS['stock']} IHSG:   {data.get('ihsg', 'Loading...'):<15} {Fore.CYAN}│{Style.RESET_ALL}
  {Fore.CYAN}│{Style.RESET_ALL}  {ICONS['stock']} S&P 500: {data.get('spx', 'Loading...'):<15} {Fore.CYAN}│{Style.RESET_ALL}
  {Fore.CYAN}│{Style.RESET_ALL}  {ICONS['crypto']} BTC:     {data.get('btc', 'Loading...'):<15} {Fore.CYAN}│{Style.RESET_ALL}
  {Fore.CYAN}│{Style.RESET_ALL}  {ICONS['forex']} USD/IDR: {data.get('usd_idr', 'Loading...'):<15} {Fore.CYAN}│{Style.RESET_ALL}
  {Fore.CYAN}└{'─' * 56}┘{Style.RESET_ALL}
""")


def show_result(result):
    """Show analysis result"""
    ticker = result.get('ticker', '').upper()
    signal = result.get('signal', 'HOLD')
    confidence = result.get('confidence', 0)
    reasoning = result.get('reasoning', '')
    
    # Signal color
    if signal == 'BUY':
        signal_icon = ICONS['buy']
        signal_color = Fore.GREEN
    elif signal == 'SELL':
        signal_icon = ICONS['sell']
        signal_color = Fore.RED
    else:
        signal_icon = ICONS['hold']
        signal_color = Fore.YELLOW
    
    print(f"""
  {Fore.CYAN}┌{'─' * 56}┐{Style.RESET_ALL}
  {Fore.CYAN}│{Style.RESET_ALL}  {Fore.WHITE}{ticker:<10}{Style.RESET_ALL} {signal_icon} {signal_color}{signal:<8}{Style.RESET_ALL} {Fore.CYAN}│{Style.RESET_ALL}
  {Fore.CYAN}├{'─' * 56}┤{Style.RESET_ALL}
  {Fore.CYAN}│{Style.RESET_ALL}  Confidence: {Fore.CYAN}{confidence:.0f}%{Style.RESET_ALL}{' ' * 36}│
  {Fore.CYAN}│{Style.RESET_ALL}  Reasoning: {Fore.WHITE}{reasoning[:45]}...{Style.RESET_ALL}{' ' * (45 - len(reasoning[:45]))}│
  {Fore.CYAN}└{'─' * 56}┘{Style.RESET_ALL}
""")


def show_portfolio(results):
    """Show portfolio summary"""
    print(f"""
  {Fore.CYAN}╔{'═' * 56}╗{Style.RESET_ALL}
  {Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}PORTFOLIO SUMMARY{Style.RESET_ALL}{' ' * 38}│
  {Fore.CYAN}╠{'═' * 56}╣{Style.RESET_ALL}
  {Fore.CYAN}║{Style.RESET_ALL}  TICKER     SIGNAL    CONFIDENCE    STRATEGIES    AGENTS     │
  {Fore.CYAN}╠{'═' * 56}╣{Style.RESET_ALL}
""")
    
    buy = sell = hold = 0
    
    for r in results:
        ticker = r.get('ticker', '').upper()
        signal = r.get('signal', 'HOLD')
        conf = r.get('confidence', 0)
        strategies = r.get('strategies', 0)
        agents = r.get('agents', 0)
        
        if signal == 'BUY':
            buy += 1
            signal_icon = ICONS['buy']
        elif signal == 'SELL':
            sell += 1
            signal_icon = ICONS['sell']
        else:
            hold += 1
            signal_icon = ICONS['hold']
        
        print(f"  {Fore.CYAN}║{Style.RESET_ALL}  {ticker:<10} {signal_icon} {signal:<8} {conf:>6.0f}%    {strategies:>3}          {agents:>3}      │")
    
    print(f"  {Fore.CYAN}╠{'═' * 56}╣{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}BUY: {buy}{Style.RESET_ALL}    {Fore.RED}SELL: {sell}{Style.RESET_ALL}    {Fore.YELLOW}HOLD: {hold}{Style.RESET_ALL}                          │")
    print(f"  {Fore.CYAN}╚{'═' * 56}╝{Style.RESET_ALL}")


def get_tickers_by_type(asset_type):
    """Get popular tickers by type"""
    tickers = {
        'stock_us': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'JPM'],
        'stock_idx': ['BBCA', 'BBRI', 'BMRI', 'TLKM', 'UNVR', 'ASII', 'HMSP', 'PTBA'],
        'crypto': ['BTC', 'ETH', 'SOL', 'XRP', 'ADA', 'DOGE', 'DOT', 'LINK'],
        'forex': ['USD/IDR', 'EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD'],
        'commodity': ['GOLD', 'SILVER', 'OIL', 'BRENT', 'NATGAS'],
    }
    return tickers.get(asset_type, [])


def run_analysis(tickers, asset_type):
    """Run analysis on tickers"""
    from enhanced_analyzer import run_enhanced_analysis
    
    # Load data
    loading("Fetching market data")
    
    # Get data
    from src.tools.advanced_data_provider import data_provider
    from src.tools.multi_asset_api import get_index_price, get_forex_cross_rate
    
    market_data = {
        'ihsg': get_index_price('IHSG'),
        'spx': get_index_price('SPX'),
        'btc': data_provider.get_crypto_binance('BTC'),
        'usd_idr': get_forex_cross_rate('USD', 'IDR')
    }
    
    show_status(market_data)
    
    # Run enhanced analysis
    loading("Running strategy analysis", 1)
    
    results = []
    for ticker in tickers:
        print(f"\n  Analyzing {ticker}...")
        
        # Get prices
        if asset_type == 'stock_us':
            prices = data_provider.get_stock_price_yahoo(ticker, 90)
        elif asset_type == 'stock_idx':
            prices = data_provider.get_idx_stock_price(ticker, 90)
        elif asset_type == 'crypto':
            prices = data_provider.get_crypto_coingecko(ticker, 'usd', 90)
        else:
            prices = []
        
        # Run strategies
        from src.strategies.quantitative_strategies import analyze_with_all_strategies
        from src.agents.enhanced_agents import run_multi_agent_analysis
        
        strategy_result = analyze_with_all_strategies(prices)
        agent_result = run_multi_agent_analysis(ticker, prices)
        
        # Combine results
        final_signal = strategy_result.final_signal
        final_confidence = (strategy_result.final_confidence + agent_result.final_confidence) / 2
        
        results.append({
            'ticker': ticker,
            'signal': final_signal,
            'confidence': final_confidence,
            'reasoning': f"Strategy: {strategy_result.consensus_level}, Agent: {agent_result.consensus_level}",
            'strategies': strategy_result.total_strategies,
            'agents': len(agent_result.agents_called)
        })
    
    return results


def main():
    """Main interactive terminal"""
    while True:
        options = [
            {"icon": ICONS['chart'], "text": "📊 New Analysis", "desc": "Start portfolio analysis"},
            {"icon": ICONS['stock'], "text": "🇺🇸 US Stocks", "desc": "AAPL, MSFT, NVDA..."},
            {"icon": ICONS['stock'], "text": "🇮🇩 Indonesia Stocks", "desc": "BBCA, BBRI, BMRI..."},
            {"icon": ICONS['crypto'], "text": "🪙 Cryptocurrency", "desc": "BTC, ETH, SOL..."},
            {"icon": ICONS['forex'], "text": "💱 Forex", "desc": "USD/IDR, EUR/USD..."},
            {"icon": ICONS['commodity'], "text": "🥇 Commodities", "desc": "GOLD, OIL, SILVER..."},
            {"icon": ICONS['brain'], "text": "🧠 All Strategies", "desc": "6 strategies + 6 agents"},
            {"icon": "🚪", "text": "Exit", "desc": "Quit the terminal"},
        ]
        
        choice = menu("MAIN MENU", options, "Enter number to select")
        
        if choice == 1:
            # New analysis
            tickers = input_text("Enter tickers (comma-separated)")
            if tickers:
                results = run_analysis(tickers.split(','), 'auto')
                show_portfolio(results)
                input(f"\n  {Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == 2:
            # US Stocks
            popular = get_tickers_by_type('stock_us')
            print(f"\n  {Fore.CYAN}Popular: {', '.join(popular)}{Style.RESET_ALL}")
            tickers = input_text("Enter tickers", ",".join(popular[:3]))
            if tickers:
                results = run_analysis(tickers.split(','), 'stock_us')
                show_portfolio(results)
                input(f"\n  {Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == 3:
            # IDX Stocks
            popular = get_tickers_by_type('stock_idx')
            print(f"\n  {Fore.CYAN}Popular: {', '.join(popular)}{Style.RESET_ALL}")
            tickers = input_text("Enter tickers", ",".join(popular[:3]))
            if tickers:
                results = run_analysis(tickers.split(','), 'stock_idx')
                show_portfolio(results)
                input(f"\n  {Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == 4:
            # Crypto
            popular = get_tickers_by_type('crypto')
            print(f"\n  {Fore.CYAN}Popular: {', '.join(popular)}{Style.RESET_ALL}")
            tickers = input_text("Enter tickers", ",".join(popular[:3]))
            if tickers:
                results = run_analysis(tickers.split(','), 'crypto')
                show_portfolio(results)
                input(f"\n  {Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == 5:
            # Forex
            popular = get_tickers_by_type('forex')
            print(f"\n  {Fore.CYAN}Popular: {', '.join(popular)}{Style.RESET_ALL}")
            tickers = input_text("Enter pairs", ",".join(popular[:2]))
            if tickers:
                results = run_analysis(tickers.split(','), 'forex')
                show_portfolio(results)
                input(f"\n  {Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == 6:
            # Commodities
            popular = get_tickers_by_type('commodity')
            print(f"\n  {Fore.CYAN}Popular: {', '.join(popular)}{Style.RESET_ALL}")
            tickers = input_text("Enter commodities", ",".join(popular[:2]))
            if tickers:
                results = run_analysis(tickers.split(','), 'commodity')
                show_portfolio(results)
                input(f"\n  {Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == 7:
            # All strategies
            print(f"\n  {Fore.CYAN}Running all 6 strategies + 6 agents...{Style.RESET_ALL}")
            tickers = input_text("Enter tickers", "AAPL,BTC")
            if tickers:
                results = run_analysis(tickers.split(','), 'auto')
                show_portfolio(results)
                input(f"\n  {Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == 8:
            # Exit
            print(f"\n  {Fore.CYAN}👋 Goodbye! Happy Trading!{Style.RESET_ALL}\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}\n")
