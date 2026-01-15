#!/usr/bin/env python3
"""
AI Hedge Fund - Simple Launcher
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from colorama import Fore, Style, init
import argparse

init(autoreset=True)


def main():
    parser = argparse.ArgumentParser(
        description='AI Hedge Fund Trading System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick analysis (auto-detect)
  python launcher.py AAPL,MSFT,BTC

  # Specific type
  python launcher.py BBCA,BBRI --type stock_idx
  python launcher.py BTC,ETH --type crypto
  python launcher.py USD/IDR --type forex
  python launcher.py GOLD --type commodity
        """
    )
    
    parser.add_argument(
        'tickers',
        type=str,
        nargs='?',
        help='Comma-separated tickers'
    )
    parser.add_argument(
        '--type', '-t',
        type=str,
        default='auto',
        choices=['stock_us', 'stock_idx', 'forex', 'crypto', 'commodity', 'auto'],
        help='Asset type'
    )
    parser.add_argument(
        '--model', '-m',
        type=str,
        default='opencode/grok-code',
        help='AI model'
    )
    
    args = parser.parse_args()
    
    # Banner
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║     🤖 AI HEDGE FUND TRADING SYSTEM      ║
║     Multi-Strategy + Multi-Agent         ║
╚════════════════════════════════════════════╝
{Style.RESET_ALL}""")
    
    if not args.tickers:
        parser.print_help()
        return
    
    # Parse tickers
    tickers = [t.strip().upper() for t in args.tickers.split(',') if t.strip()]
    
    # Run enhanced analysis
    print(f"\n{Fore.YELLOW}🚀 Analyzing {len(tickers)} assets...{Style.RESET_ALL}\n")
    
    from enhanced_analyzer import run_enhanced_analysis
    run_enhanced_analysis(tickers, args.model)


if __name__ == "__main__":
    main()
