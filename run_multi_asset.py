#!/usr/bin/env python3
"""
Multi-Asset AI Hedge Fund Trading System
Supports: Stocks (US/IDX), Forex, Crypto, Commodities
All data from FREE sources!
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.multi_asset_api import (
    get_price_data, get_index_price,
    POPULAR_TICKERS, AssetType
)
from src.llm.opencode_client import OpenCodeLLM
from colorama import Fore, Style, init

init(autoreset=True)


def print_banner():
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║         🤖 MULTI-ASSET AI HEDGE FUND TRADING SYSTEM 🤖          ║
║                                                                  ║
║  Supported Assets:                                               ║
{Fore.GREEN}  • US Stocks: AAPL, MSFT, GOOGL, NVDA, etc.{Fore.CYAN}                       ║
{Fore.GREEN}  • IDX Stocks: BBCA, BBRI, BMRI, TLKM, etc.{Fore.CYAN}                       ║
{Fore.GREEN}  • Forex: USD/IDR, EUR/USD, GBP/JPY, etc.{Fore.CYAN}                        ║
{Fore.GREEN}  • Crypto: BTC, ETH, SOL, XRP, ADA, etc.{Fore.CYAN}                        ║
{Fore.GREEN}  • Commodities: GOLD, OIL, SILVER, etc.{Fore.CYAN}                         ║
{Fore.GREEN}  • Indices: IHSG, S&P 500, NASDAQ, etc.{Fore.CYAN}                         ║
║                                                                  ║
║  Powered by OpenCode (FREE AI - No API Key!)                     ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)


def get_asset_type(ticker: str) -> str:
    """Auto-detect asset type from ticker"""
    ticker = ticker.upper()
    
    if ticker.endswith('.JK') or ticker in POPULAR_TICKERS['stock_idx']:
        return 'stock_idx'
    elif '/' in ticker or len(ticker) == 6:
        return 'forex'
    elif ticker.upper() in POPULAR_TICKERS['crypto']:
        return 'crypto'
    elif ticker.upper() in POPULAR_TICKERS['commodity']:
        return 'commodity'
    elif ticker.upper() in POPULAR_TICKERS['index']:
        return 'index'
    else:
        return 'stock_us'


def analyze_with_ai(ticker: str, asset_type: str, prices) -> dict:
    """Analyze asset using OpenCode AI"""
    llm = OpenCodeLLM("opencode/grok-code")
    
    # Calculate basic metrics
    if prices:
        latest = prices[-1]
        if len(prices) > 1:
            prev = prices[-2]
            change = ((latest.close - prev.close) / prev.close) * 100
        else:
            change = 0
        
        price_info = f"""
Current Price: ${latest.close:,.2f}
Volume: {latest.volume:,}
Change: {change:+.2f}%
"""
    else:
        price_info = "No price data available"
    
    prompt = f"""Analyze {ticker} ({asset_type.upper()}) and provide:

1. Signal: BUY, SELL, or HOLD
2. Confidence: 0-100%
3. Key Reasoning: 2-3 sentences

Current Market Data:
{price_info}

Respond in this exact JSON format:
{{"signal": "BUY", "confidence": 75, "reasoning": "..."}}
"""
    
    try:
        result = llm.structured_output(prompt, {
            "type": "object",
            "properties": {
                "signal": {"type": "string"},
                "confidence": {"type": "number"},
                "reasoning": {"type": "string"}
            },
            "required": ["signal", "confidence", "reasoning"]
        })
        return result
    except Exception as e:
        print(f"{Fore.RED}AI Analysis Error: {e}{Style.RESET_ALL}")
        return {"signal": "HOLD", "confidence": 50, "reasoning": "AI analysis failed"}


def format_currency(value: float, currency: str = "USD") -> str:
    """Format currency based on type"""
    if currency == "IDR":
        return f"Rp {value:,.0f}"
    elif currency in ["BTC", "ETH", "SOL"]:
        return f"{value:.6f} {currency}"
    else:
        return f"${value:,.2f}"


def run_multi_asset_analysis(tickers: list, model: str = "opencode/grok-code"):
    """Run analysis on multiple asset types"""
    print_banner()
    
    all_results = []
    
    for ticker in tickers:
        asset_type = get_asset_type(ticker)
        display_ticker = ticker.upper()
        
        print(f"\n{Fore.YELLOW}📊 Analyzing: {display_ticker} ({asset_type.upper()})...{Style.RESET_ALL}")
        
        # Get price data
        if asset_type == 'index':
            price_data = get_index_price(display_ticker)
            prices = []
        else:
            prices = get_price_data(ticker, asset_type, 30)
            price_data = prices[-1] if prices else None
        
        # Get IHSG/Index data
        if asset_type == 'stock_idx':
            market_data = get_index_price('IHSG')
            print(f"   {Fore.CYAN}Market (IHSG): {format_currency(market_data.get('price', 0), 'IDR')}{Style.RESET_ALL}")
        
        # Display price
        if price_data:
            currency = "IDR" if asset_type == 'stock_idx' else "USD"
            print(f"   {Fore.GREEN}Price: {format_currency(price_data.close, currency)}{Style.RESET_ALL}")
        
        # Analyze with AI
        analysis = analyze_with_ai(ticker, asset_type, prices)
        
        # Color based on signal
        signal_color = {
            'BUY': Fore.GREEN,
            'SELL': Fore.RED,
            'HOLD': Fore.YELLOW
        }.get(analysis.get('signal', 'HOLD'), Fore.WHITE)
        
        print(f"\n{Fore.CYAN}🤖 AI Analysis Result:{Style.RESET_ALL}")
        print(f"   Signal: {signal_color}{analysis.get('signal', 'N/A')}{Style.RESET_ALL}")
        print(f"   Confidence: {Fore.CYAN}{analysis.get('confidence', 0)}%{Style.RESET_ALL}")
        print(f"   Reasoning: {analysis.get('reasoning', 'N/A')}")
        
        all_results.append({
            'ticker': display_ticker,
            'asset_type': asset_type,
            'signal': analysis.get('signal'),
            'confidence': analysis.get('confidence'),
            'reasoning': analysis.get('reasoning'),
            'price': price_data.close if price_data else 0
        })
    
    # Summary
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║                    📈 PORTFOLIO SUMMARY                          ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  Ticker      │  Signal  │  Confidence │  Price              ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    
    buy_count = sell_count = hold_count = 0
    
    for r in all_results:
        signal_color = {
            'BUY': Fore.GREEN,
            'SELL': Fore.RED,
            'HOLD': Fore.YELLOW
        }.get(r['signal'], Fore.WHITE)
        
        if r['signal'] == 'BUY':
            buy_count += 1
        elif r['signal'] == 'SELL':
            sell_count += 1
        else:
            hold_count += 1
        
        price_str = format_currency(r['price'], 'IDR' if r['asset_type'] == 'stock_idx' else 'USD')
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {r['ticker']:<10} │{signal_color}  {r['signal']:<6}  {Style.RESET_ALL}│{Fore.CYAN}   {r['confidence']:>3}%{Style.RESET_ALL}      │  {price_str:<15} {Fore.CYAN}║{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  Summary: {Fore.GREEN}BUY: {buy_count}{Style.RESET_ALL}  {Fore.RED}SELL: {sell_count}{Style.RESET_ALL}  {Fore.YELLOW}HOLD: {hold_count}{Style.RESET_ALL}                             ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    return all_results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Multi-Asset AI Hedge Fund Trading System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Indonesian stocks
  python run_multi_asset.py --tickers BBCA,BBRI,BMRI --type stock_idx
  
  # US stocks
  python run_multi_asset.py --tickers AAPL,MSFT,NVDA --type stock_us
  
  # Forex
  python run_multi_asset.py --tickers USD/IDR,EUR/USD,GBP/JPY --type forex
  
  # Crypto
  python run_multi_asset.py --tickers BTC,ETH,SOL --type crypto
  
  # Commodities
  python run_multi_asset.py --tickers GOLD,OIL --type commodity
  
  # Mixed portfolio
  python run_multi_asset.py --tickers BBCA,USD/IDR,BTC,GOLD --auto
        """
    )
    
    parser.add_argument(
        "--tickers",
        type=str,
        required=True,
        help="Comma-separated list of tickers"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=['stock_us', 'stock_idx', 'forex', 'crypto', 'commodity', 'auto'],
        default='auto',
        help="Asset type (auto-detect if not specified)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="opencode/grok-code",
        help="AI model to use"
    )
    
    args = parser.parse_args()
    
    tickers = [t.strip() for t in args.tickers.split(",") if t.strip()]
    
    if args.type == 'auto':
        # Each ticker can have different types
        pass
    
    run_multi_asset_analysis(tickers, args.model)


if __name__ == "__main__":
    main()
