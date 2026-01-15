#!/usr/bin/env python3
"""
Enhanced Multi-Asset AI Trading System
With Multi-Strategy Analysis and Multi-Agent Orchestration
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from colorama import Fore, Style, init

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.advanced_data_provider import data_provider, MultiSourceDataProvider
from src.agents.enhanced_agents import (
    run_multi_agent_analysis,
    ENHANCED_AGENTS
)
from src.strategies.quantitative_strategies import analyze_with_all_strategies
from src.llm.opencode_client import OpenCodeLLM

init(autoreset=True)


def print_banner():
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║              🤖 ENHANCED AI HEDGE FUND TRADING SYSTEM 🤖                          ║
║                                                                                   ║
║     Multi-Strategy + Multi-Agent Analysis | All FREE Data Sources                ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)


def get_asset_type(ticker: str) -> str:
    """Auto-detect asset type"""
    ticker = ticker.upper()
    
    popular_idx = ['BBCA', 'BBRI', 'BMRI', 'TLKM', 'UNVR', 'ASII', 'HMSP', 'PTBA']
    popular_crypto = ['BTC', 'ETH', 'SOL', 'XRP', 'ADA', 'DOGE', 'DOT', 'LINK']
    
    if ticker.endswith('.JK') or ticker in popular_idx:
        return 'stock_idx'
    elif '/' in ticker or (len(ticker) == 6 and ticker.isupper()):
        return 'forex'
    elif ticker in popular_crypto or ticker in ['BTCUSDT', 'ETHUSDT']:
        return 'crypto'
    elif ticker in ['GOLD', 'SILVER', 'OIL', 'BRENT']:
        return 'commodity'
    else:
        return 'stock_us'


def format_currency(value: float, asset_type: str) -> str:
    """Format currency based on asset type"""
    if asset_type == 'stock_idx':
        return f"Rp {value:,.0f}"
    elif asset_type == 'crypto':
        return f"${value:,.2f}"
    else:
        return f"${value:,.2f}"


def analyze_asset(
    ticker: str,
    asset_type: str,
    prices: List = None
) -> Dict[str, Any]:
    """Comprehensive analysis using all strategies and agents"""
    
    # Get price data
    if prices is None:
        if asset_type == 'stock_us':
            prices = data_provider.get_stock_price_yahoo(ticker, 90)
        elif asset_type == 'stock_idx':
            prices = data_provider.get_idx_stock_price(ticker, 90)
        elif asset_type == 'crypto':
            prices = data_provider.get_crypto_coingecko(ticker, 'usd', 90)
        else:
            prices = []
    
    # Get current price
    current_price = prices[-1].close if prices and hasattr(prices[-1], 'close') else 0
    
    # Run multi-strategy analysis
    strategy_result = analyze_with_all_strategies(prices)
    
    # Run multi-agent analysis
    agent_result = run_multi_agent_analysis(ticker, prices)
    
    # Get AI analysis using OpenCode
    llm = OpenCodeLLM("opencode/grok-code")
    
    prompt = f"""Analyze {ticker} ({asset_type.upper()}) with the following data:

Current Price: {format_currency(current_price, asset_type)}

STRATEGY ANALYSIS:
- Final Signal: {strategy_result.final_signal}
- Confidence: {strategy_result.final_confidence:.1f}%
- Consensus: {strategy_result.consensus_level}
- Strategies: {strategy_result.total_strategies} (BUY:{strategy_result.buy_count}, SELL:{strategy_result.sell_count}, HOLD:{strategy_result.hold_count})

AGENT ANALYSIS:
- Final Signal: {agent_result.final_signal}
- Confidence: {agent_result.final_confidence:.1f}%
- Consensus: {agent_result.consensus_level}
- Agents: {len(agent_result.agents_called)}

Provide:
1. Investment recommendation (BUY/SELL/HOLD)
2. Confidence score (0-100%)
3. Key reasoning (2-3 sentences)

Respond in JSON format:
{{"signal": "BUY", "confidence": 85, "reasoning": "..."}}"""
    
    try:
        ai_result = llm.structured_output(prompt, {
            "type": "object",
            "properties": {
                "signal": {"type": "string"},
                "confidence": {"type": "number"},
                "reasoning": {"type": "string"}
            }
        })
    except:
        ai_result = {
            "signal": strategy_result.final_signal,
            "confidence": strategy_result.final_confidence,
            "reasoning": "Based on quantitative and agent analysis"
        }
    
    return {
        "ticker": ticker,
        "asset_type": asset_type,
        "current_price": current_price,
        "strategy_result": {
            "total_strategies": strategy_result.total_strategies,
            "final_signal": strategy_result.final_signal,
            "confidence": strategy_result.final_confidence,
            "consensus": strategy_result.consensus_level,
            "buy_count": strategy_result.buy_count,
            "sell_count": strategy_result.sell_count,
            "hold_count": strategy_result.hold_count,
            "strategies": strategy_result.strategy_details
        },
        "agent_result": {
            "total_agents": len(agent_result.agents_called),
            "final_signal": agent_result.final_signal,
            "confidence": agent_result.final_confidence,
            "consensus": agent_result.consensus_level,
            "agents": agent_result.signals
        },
        "ai_result": ai_result
    }


def display_analysis_result(result: Dict):
    """Display analysis result in formatted output"""
    ticker = result['ticker']
    asset_type = result['asset_type']
    
    print(f"\n{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    padding = " " * (55 - len(ticker) - len(asset_type) - 15)
    print(f"{Fore.YELLOW}║  📊 ANALYSIS: {ticker.upper()} ({asset_type.upper()}){padding}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Current price
    price_str = format_currency(result['current_price'], asset_type)
    print(f"\n  💰 Current Price: {Fore.CYAN}{price_str}{Style.RESET_ALL}")
    
    # Strategy results
    sr = result['strategy_result']
    print(f"\n  {Fore.CYAN}📈 STRATEGY ANALYSIS ({sr['total_strategies']} strategies):{Style.RESET_ALL}")
    print(f"     Signal: {sr['final_signal']} | Confidence: {sr['confidence']:.1f}% | Consensus: {sr['consensus']}")
    print(f"     Breakdown: {Fore.GREEN}BUY: {sr['buy_count']}{Style.RESET_ALL} | {Fore.RED}SELL: {sr['sell_count']}{Style.RESET_ALL} | {Fore.YELLOW}HOLD: {sr['hold_count']}{Style.RESET_ALL}")
    
    # Agent results
    ar = result['agent_result']
    print(f"\n  {Fore.CYAN}🤖 AGENT ANALYSIS ({ar['total_agents']} agents):{Style.RESET_ALL}")
    for agent in ar['agents'][:4]:  # Show top 4
        color = Fore.GREEN if agent['signal'] == 'BUY' else Fore.RED if agent['signal'] == 'SELL' else Fore.YELLOW
        print(f"     • {agent['agent']}: {color}{agent['signal']}{Style.RESET_ALL} ({agent['confidence']}%)")
    
    # AI Result
    ai = result['ai_result']
    ai_color = Fore.GREEN if ai.get('signal') == 'BUY' else Fore.RED if ai.get('signal') == 'SELL' else Fore.YELLOW
    print(f"\n  {Fore.CYAN}🎯 AI FINAL VERDICT:{Style.RESET_ALL}")
    print(f"     Signal: {ai_color}{ai.get('signal', 'N/A')}{Style.RESET_ALL}")
    print(f"     Confidence: {Fore.CYAN}{ai.get('confidence', 0):.1f}%{Style.RESET_ALL}")
    print(f"     Reasoning: {ai.get('reasoning', 'N/A')}")


def display_portfolio_summary(results: List[Dict]):
    """Display portfolio summary table"""
    print(f"\n\n{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║                              📈 PORTFOLIO SUMMARY                                         ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  TICKER      │  ASSET    │  PRICE        │  SIGNAL  │  CONFIDENCE │  CONSENSUS     ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    
    buy_count = sell_count = hold_count = 0
    
    for r in results:
        ticker = r['ticker'].upper()
        asset = r['asset_type'].upper()[:8]
        price = format_currency(r['current_price'], r['asset_type'])
        
        signal = r['ai_result'].get('signal', 'HOLD')
        confidence = r['ai_result'].get('confidence', 0)
        consensus = r['strategy_result']['consensus']
        
        signal_color = Fore.GREEN if signal == 'BUY' else Fore.RED if signal == 'SELL' else Fore.YELLOW
        
        if signal == 'BUY':
            buy_count += 1
        elif signal == 'SELL':
            sell_count += 1
        else:
            hold_count += 1
        
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {ticker:<10} │  {asset:<8} │  {price:<12} │  {signal_color}{signal:<8}{Style.RESET_ALL} │  {confidence:>6.1f}%    │  {consensus:<13} ║{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  SUMMARY: {Fore.GREEN}BUY: {buy_count}{Style.RESET_ALL}  {Fore.RED}SELL: {sell_count}{Style.RESET_ALL}  {Fore.YELLOW}HOLD: {hold_count}{Style.RESET_ALL}  " + " " * 45 + f"║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Recommendations
    print(f"\n  {Fore.CYAN}📋 RECOMMENDATIONS:{Style.RESET_ALL}")
    
    for r in results:
        signal = r['ai_result'].get('signal', 'HOLD')
        if signal == 'BUY':
            ticker = r['ticker'].upper()
            price = format_currency(r['current_price'], r['asset_type'])
            confidence = r['ai_result'].get('confidence', 0)
            print(f"  {Fore.GREEN}✅ BUY {ticker}{Style.RESET_ALL} at {price} (Confidence: {confidence:.0f}%)")
        elif signal == 'SELL':
            ticker = r['ticker'].upper()
            price = format_currency(r['current_price'], r['asset_type'])
            confidence = r['ai_result'].get('confidence', 0)
            print(f"  {Fore.RED}❌ SELL {ticker}{Style.RESET_ALL} at {price} (Confidence: {confidence:.0f}%)")


def run_enhanced_analysis(tickers: list, model: str = "opencode/grok-code"):
    """Run enhanced multi-asset, multi-strategy analysis"""
    print_banner()
    
    print(f"\n{Fore.CYAN}🚀 Running Enhanced Analysis on {len(tickers)} assets...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 Using {len(ENHANCED_AGENTS)} AI Agents + 6 Quantitative Strategies{Style.RESET_ALL}\n")
    
    results = []
    
    for ticker in tickers:
        asset_type = get_asset_type(ticker)
        print(f"  Analyzing {ticker.upper()} ({asset_type.upper()})...", end=" ")
        
        try:
            result = analyze_asset(ticker, asset_type)
            results.append(result)
            print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    
    if results:
        # Display individual results
        for result in results:
            display_analysis_result(result)
        
        # Display summary
        display_portfolio_summary(results)
    
    return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Enhanced Multi-Asset AI Trading System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Indonesian stocks
  python enhanced_analyzer.py --tickers BBCA,BBRI,BMRI --type stock_idx
  
  # US stocks with all strategies
  python enhanced_analyzer.py --tickers AAPL,MSFT,NVDA --type stock_us
  
  # Crypto portfolio
  python enhanced_analyzer.py --tickers BTC,ETH,SOL --type crypto
  
  # Mixed portfolio (auto-detect)
  python enhanced_analyzer.py --tickers BBCA,USD/IDR,BTC,GOLD --auto
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
    
    run_enhanced_analysis(tickers, args.model)


if __name__ == "__main__":
    main()
