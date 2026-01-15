#!/usr/bin/env python3
"""
Simple Launcher - LangChain Free Version
Minimal launcher untuk testing core functionality
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import argparse
import pandas as pd
import numpy as np

def get_mock_decision(ticker):
    """Generate mock trading decision"""
    np.random.seed(42)
    actions = ['BUY', 'SELL', 'HOLD']
    action = np.random.choice(actions)
    confidence = np.random.randint(60, 95)
    reasoning = f"Mock {action} signal for {ticker} with {confidence}% confidence"
    
    return {
        'ticker': ticker,
        'action': action,
        'confidence': confidence,
        'reasoning': reasoning
    }

def simple_analysis(tickers):
    """Simple analysis without LLM"""
    print(f"\n🚀 Analyzing {len(tickers)} assets (Mock Mode)...\n")
    
    results = []
    for ticker in tickers:
        decision = get_mock_decision(ticker)
        results.append(decision)
        
        # Print results
        action_color = {
            'BUY': '\033[92m',    # Green
            'SELL': '\033[91m',   # Red
            'HOLD': '\033[93m'    # Yellow
        }.get(decision['action'], '\033[0m')
        
        print(f"📊 {ticker}:")
        print(f"  Action: {action_color}{decision['action']}\033[0m")
        print(f"  Confidence: {decision['confidence']}%")
        print(f"  Reasoning: {decision['reasoning']}")
        print()
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description='AI Hedge Fund - Simple Launcher (No LLM)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simple_launcher.py AAPL
  python simple_launcher.py AAPL,MSFT,BTC
        """
    )
    
    parser.add_argument(
        'tickers',
        help='Comma-separated tickers'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Banner
    print("""
╔════════════════════════════════════════════╗
║     🤖 AI HEDGE FUND - SIMPLE MODE       ║
║     Mock Trading Decisions (No LLM)     ║
╚════════════════════════════════════════════╝
""")
    
    if not args.tickers:
        parser.print_help()
        return
    
    # Parse tickers
    tickers = [t.strip().upper() for t in args.tickers.split(',') if t.strip()]
    
    # Run simple analysis
    try:
        results = simple_analysis(tickers)
        
        # Summary
        buy_count = sum(1 for r in results if r['action'] == 'BUY')
        sell_count = sum(1 for r in results if r['action'] == 'SELL')
        hold_count = sum(1 for r in results if r['action'] == 'HOLD')
        
        print("=" * 50)
        print("📈 SUMMARY:")
        print(f"  🟢 BUY: {buy_count}")
        print(f"  🔴 SELL: {sell_count}")
        print(f"  🟡 HOLD: {hold_count}")
        print(f"  📊 Total: {len(results)} assets analyzed")
        print("\n✅ Simple Launcher Working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())