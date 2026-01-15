"""
AI Hedge Fund - Unified Trading System
========================================
Complete end-to-end trading system connecting:
- Data Sources → Technical Indicators → Strategies (18 Retail + 10 Legendary) → Unified Signal

Usage:
    python3 unified_trading_system.py AAPL
    python3 unified_trading_system.py BBCA --market idx
    python3 unified_trading_system.py BTC --asset crypto
    python3 unified_trading_system.py USD/IDR --asset forex
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

import pandas as pd
import numpy as np

# Import our modules
from src.tools.unified_data_provider import UnifiedDataProvider, AssetType
from src.indicators.technical_indicators import TechnicalIndicators
from src.strategies.unified_retail_strategy import RetailStrategyAnalyzer, SignalType
from src.strategies.quantitative_strategies import analyze_with_all_strategies, StrategyType
from src.strategies.legendary_investors import (
    analyze_with_all_legendary,
    get_fundamentals_from_price,
    LegendaryConsensus
)
from src.optimization.portfolio_optimizer import PortfolioOptimizer, OptimizationMethod
from src.risk.risk_management import RiskManagementFramework, calculate_sharpe_ratio


class TradingSignal(Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"


@dataclass
class TradingDecision:
    """Complete trading decision output"""
    symbol: str
    asset_type: str
    timestamp: datetime
    
    # Price data
    current_price: float
    daily_change: float
    daily_change_pct: float
    
    # Technical indicators
    rsi: float
    macd_signal: str
    trend: str
    volatility: str
    
    # Strategy signals
    retail_signal: TradingSignal
    retail_confidence: float
    quant_signal: TradingSignal
    quant_confidence: float
    legendary_signal: TradingSignal
    legendary_confidence: float
    
    # Consensus
    final_signal: TradingSignal
    final_confidence: float
    score: int  # 0-100
    
    # Risk metrics
    sharpe_ratio: float
    var_95: float
    risk_score: int  # 0-100
    
    # Levels
    entry_zone: tuple
    stop_loss: float
    take_profit: tuple
    
    # Reasoning
    reasons: List[str]
    metadata: Dict = field(default_factory=dict)


class UnifiedTradingSystem:
    """
    Complete AI Trading System
    
    Flow:
    1. Fetch Data → 2. Calculate Indicators → 3. Run All Strategies → 4. Generate Signal
    
    Strategies Included:
    - 18 Retail/SMC Strategies (OTE, Kill Zones, Market Profile, etc.)
    - 6 Quantitative Strategies (Jim Simons, Momentum, Mean Reversion, etc.)
    - 10 Legendary Investor Strategies (Buffett, Lynch, Graham, Soros, Dalio, Burry, Fisher, Templeton, Greenblatt, O'Neil)
    
    Total: 34 Strategies!
    """
    
    def __init__(self):
        self.data_provider = UnifiedDataProvider()
        self.ti = TechnicalIndicators()
        self.retail_analyzer = RetailStrategyAnalyzer()
        self.risk = RiskManagementFramework()
        
    def analyze(
        self,
        symbol: str,
        asset_type: str = "stock",
        days: int = 100
    ) -> TradingDecision:
        """
        Main analysis function - returns complete trading decision
        
        Args:
            symbol: Trading symbol (e.g., 'AAPL', 'BBCA', 'BTC')
            asset_type: 'stock_us', 'stock_idx', 'forex', 'crypto', 'commodity', 'index'
            days: Historical data period
        
        Returns:
            TradingDecision with full analysis
        """
        print(f"\n{'='*70}")
        print(f"🤖 AI HEDGE FUND - UNIFIED TRADING SYSTEM")
        print(f"{'='*70}")
        print(f"\n📊 Analyzing: {symbol} ({asset_type})")
        
        # ===== STEP 1: FETCH DATA =====
        print(f"\n📥 STEP 1: Fetching data...")
        prices = self.data_provider.get_price(symbol, asset_type, days)
        
        if not prices or len(prices) < 30:
            raise ValueError(f"Insufficient data for {symbol}")
        
        # Convert to DataFrame
        df = self._prices_to_dataframe(prices)
        print(f"   ✅ Loaded {len(df)} days of data")
        
        close = df['close']
        high = df['high']
        low = df['low']
        volume = df['volume']
        current_price = close.iloc[-1]
        daily_change = close.iloc[-1] - close.iloc[-2]
        daily_change_pct = (daily_change / close.iloc[-2]) * 100
        
        print(f"   💰 Price: ${current_price:,.2f} ({daily_change_pct:+.2f}%)")
        
        # ===== STEP 2: TECHNICAL INDICATORS =====
        print(f"\n📈 STEP 2: Calculating technical indicators...")
        
        indicators = self._calculate_indicators(high, low, close, volume)
        print(f"   ✅ RSI: {indicators['rsi']:.1f}")
        print(f"   ✅ MACD: {indicators['macd']:.4f}")
        print(f"   ✅ Trend: {indicators['trend']}")
        
        # ===== STEP 3: RETAIL STRATEGIES (18 strategies) =====
        print(f"\n🎯 STEP 3: Running 18 retail strategies (SMC/ICT)...")
        
        retail_result = self.retail_analyzer.analyze(
            high, low, close, volume, symbol=symbol
        )
        retail_signal = self._signal_type(retail_result.direction)
        retail_confidence = retail_result.confidence
        print(f"   ✅ Retail Signal: {retail_signal.value} ({retail_confidence:.0%})")
        print(f"   ✅ Retail Score: {retail_result.score}")
        
        # ===== STEP 4: QUANTITATIVE STRATEGIES (6 strategies) =====
        print(f"\n🔬 STEP 4: Running 6 quantitative strategies...")
        
        price_list = close.tolist()
        fundamentals = get_fundamentals_from_price(price_list)
        market_data = {}  # Could add real market data
        
        quant_result = analyze_with_all_strategies(price_list, fundamentals, market_data)
        quant_signal = self._signal_type(quant_result.final_signal)
        quant_confidence = quant_result.confidence if hasattr(quant_result, 'confidence') else 0.5
        print(f"   ✅ Quant Signal: {quant_signal.value} ({quant_confidence:.0%})")
        print(f"   ✅ Quant Score: {quant_result.weighted_score:.2f}")
        
        # ===== STEP 5: LEGENDARY INVESTORS (10 strategies) =====
        print(f"\n🏆 STEP 5: Running 10 legendary investor strategies...")
        print(f"   📋 Strategies: Buffett, Lynch, Graham, Soros, Dalio, Burry, Fisher, Templeton, Greenblatt, O'Neil")
        
        legendary_result = analyze_with_all_legendary(price_list, fundamentals, market_data)
        legendary_signal = self._legendary_signal(legendary_result.final_signal)
        legendary_confidence = legendary_result.confidence
        
        print(f"   ✅ Legendary Signal: {legendary_signal.value} ({legendary_confidence:.0%})")
        print(f"   ✅ Consensus: {legendary_result.consensus_level}")
        print(f"   ✅ Best: {legendary_result.best_investor} | Worst: {legendary_result.worst_investor}")
        
        # ===== STEP 6: RISK ANALYSIS =====
        print(f"\n⚠️  STEP 6: Risk analysis...")
        
        returns = close.pct_change().dropna()
        sharpe = calculate_sharpe_ratio(returns)
        
        var_95 = self.risk.calculate_var(
            returns, 
            portfolio_value=current_price * 100,
            method="historical"
        )
        
        risk_score = min(100, max(0, 100 - (var_95 * 100)))
        print(f"   ✅ Sharpe Ratio: {sharpe:.2f}")
        print(f"   ✅ VaR (95%): {var_95:.2%}")
        print(f"   ✅ Risk Score: {risk_score}/100")
        
        # ===== STEP 7: FINAL CONSENSUS =====
        print(f"\n🎯 STEP 7: Generating final consensus from 34 strategies...")
        
        # Weighted average of all signals
        retail_weight = 0.25
        quant_weight = 0.25
        legendary_weight = 0.30
        risk_weight = 0.20
        
        retail_score = self._signal_to_score(retail_signal)
        quant_score = self._signal_to_score(quant_signal)
        legendary_score = self._signal_to_score(legendary_signal)
        
        final_score = (
            retail_score * retail_weight + 
            quant_score * quant_weight + 
            legendary_score * legendary_weight + 
            risk_score * risk_weight
        )
        
        if final_score >= 75:
            final_signal = TradingSignal.STRONG_BUY
        elif final_score >= 60:
            final_signal = TradingSignal.BUY
        elif final_score >= 45:
            final_signal = TradingSignal.HOLD
        elif final_score >= 30:
            final_signal = TradingSignal.SELL
        else:
            final_signal = TradingSignal.STRONG_SELL
        
        final_confidence = final_score / 100
        
        # Calculate levels
        atr = indicators.get('atr', current_price * 0.02)
        entry = current_price
        
        if final_signal in [TradingSignal.STRONG_BUY, TradingSignal.BUY]:
            stop_loss = entry * 0.98
            take_profit = (entry * 1.03, entry * 1.05, entry * 1.08)
        elif final_signal in [TradingSignal.STRONG_SELL, TradingSignal.SELL]:
            stop_loss = entry * 1.02
            take_profit = (entry * 0.97, entry * 0.95, entry * 0.92)
        else:
            stop_loss = entry * 0.95
            take_profit = (entry * 1.02, entry * 1.05, entry * 1.08)
        
        # Collect reasons
        reasons = []
        reasons.append(f"34 Strategies Analyzed: Retail ({retail_signal.value}), Quant ({quant_signal.value}), Legendary ({legendary_signal.value})")
        
        if indicators['rsi'] < 35:
            reasons.append(f"RSI oversold ({indicators['rsi']:.0f}) - bullish")
        elif indicators['rsi'] > 65:
            reasons.append(f"RSI overbought ({indicators['rsi']:.0f}) - bearish")
        
        if retail_result.reasons:
            reasons.append(f"Retail: {retail_result.reasons[0]}")
        
        if legendary_result.best_investor:
            reasons.append(f"Legendary: Best strategy is {legendary_result.best_investor}")
        
        if sharpe > 1:
            reasons.append(f"Strong risk-adjusted returns (Sharpe: {sharpe:.2f})")
        
        if var_95 < 0.02:
            reasons.append("Low VaR - favorable risk profile")
        
        # ===== FINAL OUTPUT =====
        print(f"\n{'='*70}")
        print(f"📋 TRADING DECISION")
        print(f"{'='*70}")
        
        signal_emoji = {
            TradingSignal.STRONG_BUY: "🟢🟢",
            TradingSignal.BUY: "🟢",
            TradingSignal.HOLD: "🟡",
            TradingSignal.SELL: "🔴",
            TradingSignal.STRONG_SELL: "🔴🔴",
        }[final_signal]
        
        print(f"\n{signal_emoji} FINAL SIGNAL: {final_signal.value}")
        print(f"📊 CONFIDENCE: {final_confidence:.0%}")
        print(f"📈 SCORE: {final_score:.0f}/100")
        
        print(f"\n💰 CURRENT PRICE: ${current_price:,.2f}")
        print(f"🎯 ENTRY ZONE: ${entry * 0.999:,.2f} - ${entry * 1.001:,.2f}")
        print(f"🛡️  STOP LOSS: ${stop_loss:,.2f}")
        print(f"🎯 TAKE PROFIT: {' / '.join([f'${tp:,.2f}' for tp in take_profit])}")
        
        print(f"\n📊 STRATEGY BREAKDOWN (34 Total):")
        print(f"   🎯 Retail Strategies (18): {retail_signal.value} ({retail_confidence:.0%})")
        print(f"   🔬 Quantitative Strategies (6): {quant_signal.value} ({quant_confidence:.0%})")
        print(f"   🏆 Legendary Investors (10): {legendary_signal.value} ({legendary_confidence:.0%})")
        print(f"   ⚠️  Risk Score: {risk_score}/100")
        
        if legendary_result.investor_signals:
            print(f"\n🏆 LEGENDARY INVESTORS:")
            for sig in sorted(legendary_result.investor_signals, key=lambda x: x.score, reverse=True)[:5]:
                print(f"   {sig.investor:20s}: {sig.signal:4s} ({sig.score}/100)")
        
        if reasons:
            print(f"\n💡 KEY REASONS:")
            for r in reasons[:5]:
                print(f"   • {r}")
        
        print(f"\n{'='*70}")
        
        return TradingDecision(
            symbol=symbol,
            asset_type=asset_type,
            timestamp=datetime.now(),
            current_price=current_price,
            daily_change=daily_change,
            daily_change_pct=daily_change_pct,
            rsi=indicators['rsi'],
            macd_signal=indicators['trend'],
            trend=indicators['trend'],
            volatility=indicators['volatility'],
            retail_signal=retail_signal,
            retail_confidence=retail_confidence,
            quant_signal=quant_signal,
            quant_confidence=quant_confidence,
            legendary_signal=legendary_signal,
            legendary_confidence=legendary_confidence,
            final_signal=final_signal,
            final_confidence=final_confidence,
            score=int(final_score),
            sharpe_ratio=sharpe,
            var_95=var_95,
            risk_score=risk_score,
            entry_zone=(entry * 0.999, entry * 1.001),
            stop_loss=stop_loss,
            take_profit=take_profit,
            reasons=reasons,
            metadata={
                'retail_analysis': retail_result.__dict__ if hasattr(retail_result, '__dict__') else {},
                'quant_analysis': {
                    'final_signal': str(quant_result.final_signal),
                    'weighted_score': quant_result.weighted_score,
                    'strategy_details_count': len(quant_result.strategy_details) if hasattr(quant_result, 'strategy_details') else 0
                },
                'legendary_analysis': {
                    'final_signal': legendary_result.final_signal,
                    'consensus_level': legendary_result.consensus_level,
                    'best_investor': legendary_result.best_investor,
                    'worst_investor': legendary_result.worst_investor,
                    'wisdom_of_crowds': legendary_result.wisdom_of_crowds,
                    'investor_signals': [
                        {
                            'investor': s.investor,
                            'signal': s.signal,
                            'score': s.score,
                            'confidence': s.confidence
                        }
                        for s in legendary_result.investor_signals
                    ]
                },
                'indicators': indicators
            }
        )
    
    def _prices_to_dataframe(self, prices: List) -> pd.DataFrame:
        """Convert PriceData list to DataFrame"""
        data = {
            'date': [p.date for p in prices],
            'open': [p.open for p in prices],
            'high': [p.high for p in prices],
            'low': [p.low for p in prices],
            'close': [p.close for p in prices],
            'volume': [p.volume for p in prices]
        }
        return pd.DataFrame(data)
    
    def _calculate_indicators(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        volume: pd.Series
    ) -> Dict[str, Any]:
        """Calculate key technical indicators"""
        indicators = {}
        
        # RSI
        rsi = self.ti.rsi(close)
        indicators['rsi'] = rsi.iloc[-1]
        
        # MACD
        macd_line, signal_line, histogram = self.ti.macd(close)
        indicators['macd'] = macd_line.iloc[-1]
        
        # ATR
        atr = self.ti.atr(high, low, close)
        indicators['atr'] = atr.iloc[-1]
        
        # Trend
        sma20 = close.rolling(20).mean().iloc[-1]
        sma50 = close.rolling(50).mean().iloc[-1]
        
        if close.iloc[-1] > sma20 > sma50:
            indicators['trend'] = "BULLISH"
        elif close.iloc[-1] < sma20 < sma50:
            indicators['trend'] = "BEARISH"
        else:
            indicators['trend'] = "NEUTRAL"
        
        # Volatility
        vol = close.pct_change().rolling(20).std().iloc[-1]
        if vol < 0.01:
            indicators['volatility'] = "LOW"
        elif vol < 0.02:
            indicators['volatility'] = "NORMAL"
        else:
            indicators['volatility'] = "HIGH"
        
        return indicators
    
    def _signal_type(self, direction) -> TradingSignal:
        """Convert strategy signal to TradingSignal enum"""
        if hasattr(direction, 'value'):
            direction = direction.value
        
        if direction in ['buy', 'BUY', 'SignalType.BUY']:
            return TradingSignal.BUY
        elif direction in ['sell', 'SELL', 'SignalType.SELL']:
            return TradingSignal.SELL
        else:
            return TradingSignal.HOLD
    
    def _legendary_signal(self, signal: str) -> TradingSignal:
        """Convert legendary signal to TradingSignal enum"""
        if signal in ['STRONG_BUY', 'STRONG_BUY']:
            return TradingSignal.STRONG_BUY
        elif signal in ['BUY']:
            return TradingSignal.BUY
        elif signal in ['SELL']:
            return TradingSignal.SELL
        elif signal in ['STRONG_SELL']:
            return TradingSignal.STRONG_SELL
        else:
            return TradingSignal.HOLD
    
    def _signal_to_score(self, signal: TradingSignal) -> float:
        """Convert signal to numeric score"""
        if signal == TradingSignal.STRONG_BUY:
            return 85
        elif signal == TradingSignal.BUY:
            return 65
        elif signal == TradingSignal.HOLD:
            return 50
        elif signal == TradingSignal.SELL:
            return 35
        elif signal == TradingSignal.STRONG_SELL:
            return 15
        return 50


def analyze_portfolio(symbols: List[Dict], days: int = 100) -> List[TradingDecision]:
    """
    Analyze multiple symbols for portfolio decisions
    """
    system = UnifiedTradingSystem()
    decisions = []
    
    print(f"\n{'='*70}")
    print(f"📊 PORTFOLIO ANALYSIS - {len(symbols)} ASSETS")
    print(f"{'='*70}")
    
    for item in symbols:
        try:
            decision = system.analyze(item['symbol'], item.get('type', 'stock'), days)
            decisions.append(decision)
        except Exception as e:
            print(f"❌ Error analyzing {item['symbol']}: {e}")
    
    decisions.sort(key=lambda x: x.final_confidence, reverse=True)
    
    print(f"\n{'='*70}")
    print(f"📋 PORTFOLIO SUMMARY")
    print(f"{'='*70}")
    
    for d in decisions:
        emoji = {
            TradingSignal.STRONG_BUY: "🟢🟢",
            TradingSignal.BUY: "🟢",
            TradingSignal.HOLD: "🟡",
            TradingSignal.SELL: "🔴",
            TradingSignal.STRONG_SELL: "🔴🔴",
        }[d.final_signal]
        
        print(f"{emoji} {d.symbol:8s} | {d.final_signal.value:12s} | {d.score:3d}/100 | ${d.current_price:,.2f}")
    
    return decisions


# ============ MAIN ============

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AI Hedge Fund - Unified Trading System (34 Strategies)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Strategies (34 Total):
  📊 18 Retail/SMC: OTE, Kill Zones, Market Profile, Volume Delta, etc.
  🔬 6 Quantitative: Jim Simons, Momentum, Mean Reversion, etc.
  🏆 10 Legendary: Buffett, Lynch, Graham, Soros, Dalio, Burry, Fisher, Templeton, Greenblatt, O'Neil

Examples:
  # Single stock analysis
  python3 unified_trading_system.py AAPL
  
  # Indonesian stock
  python3 unified_trading_system.py BBCA --market idx
  
  # Crypto analysis
  python3 unified_trading_system.py BTC --asset crypto
        """
    )
    
    parser.add_argument('symbol', nargs='?', help='Trading symbol')
    parser.add_argument('--market', '-m', default='us', choices=['us', 'idx'], help='Stock market')
    parser.add_argument('--asset', '-a', default='stock', choices=['stock', 'forex', 'crypto', 'commodity', 'index'], help='Asset type')
    parser.add_argument('--days', '-d', type=int, default=100, help='Historical data period')
    parser.add_argument('--portfolio', '-p', action='store_true', help='Portfolio mode')
    
    args = parser.parse_args()
    
    if args.symbol and not args.portfolio:
        asset_type = 'stock_us' if args.market == 'us' else 'stock_idx'
        if args.asset != 'stock':
            asset_type = args.asset
        
        system = UnifiedTradingSystem()
        decision = system.analyze(args.symbol, asset_type, args.days)
        
        result = {
            'symbol': decision.symbol,
            'signal': decision.final_signal.value,
            'confidence': decision.final_confidence,
            'score': decision.score,
            'price': decision.current_price,
            'stop_loss': decision.stop_loss,
            'take_profit': list(decision.take_profit),
            'timestamp': decision.timestamp.isoformat()
        }
        
        with open(f"{args.symbol}_analysis.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\n💾 Result saved to {args.symbol}_analysis.json")
    
    elif args.portfolio or not args.symbol:
        analyze_portfolio([
            {'symbol': 'AAPL', 'type': 'stock_us'},
            {'symbol': 'MSFT', 'type': 'stock_us'},
            {'symbol': 'BBCA', 'type': 'stock_idx'},
            {'symbol': 'GOOGL', 'type': 'stock_us'},
            {'symbol': 'BTC', 'type': 'crypto'}
        ], args.days)
    
    else:
        parser.print_help()
