#!/usr/bin/env python3
"""
AI HEDGE FUND - REAL IMPLEMENTATION LAUNCHER
Production-ready system with real market data and algorithms
No mocks, no simulations - pure algorithmic trading
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import required packages
import pandas as pd
import numpy as np

# Import real components (no mocks)
try:
    import importlib.util

    def load_module_from_file(name, filepath):
        """Load a Python module directly from file path"""
        spec = importlib.util.spec_from_file_location(name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    # Load real data provider
    data_provider_module = load_module_from_file(
        "advanced_data_provider",
        "/home/mulky/ai-hedge-fund/src/tools/advanced_data_provider.py"
    )
    AdvancedDataProvider = data_provider_module.MultiSourceDataProvider

    # Load real technical indicators
    indicators_module = load_module_from_file(
        "technical_indicators",
        "/home/mulky/ai-hedge-fund/src/indicators/technical_indicators.py"
    )
    TechnicalIndicators = indicators_module.TechnicalIndicators

    # Load portfolio manager components
    portfolio_module = load_module_from_file(
        "portfolio_manager",
        "/home/mulky/ai-hedge-fund/src/agents/portfolio_manager.py"
    )
    PortfolioManagerOutput = portfolio_module.PortfolioManagerOutput
    PortfolioDecision = portfolio_module.PortfolioDecision

    print("✅ Real components loaded successfully")

except Exception as e:
    print(f"❌ Failed to load real components: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


class RealTradingSystem:
    """Real algorithmic trading system with live market data"""

    def __init__(self):
        # Simple real data provider using yfinance directly
        import yfinance as yf
        self.yf = yf
        self.indicators = TechnicalIndicators()

        # Add caching for performance
        self.data_cache = {}
        self.cache_timeout = 300  # 5 minutes cache

        # Performance metrics
        self.performance_stats = {
            'requests_made': 0,
            'cache_hits': 0,
            'errors': 0,
            'avg_response_time': 0
        }

    def fetch_real_data(self, ticker: str, days: int = 30) -> dict:
        """Fetch real market data using Yahoo Finance with enhanced error handling and caching"""
        import time
        start_time = time.time()

        print(f"📊 Fetching real market data for {ticker}...")

        # Input validation
        if not ticker or not isinstance(ticker, str):
            return {'success': False, 'error': 'Invalid ticker symbol'}

        if not isinstance(days, int) or days < 1 or days > 730:
            return {'success': False, 'error': 'Invalid days parameter (1-730)'}

        # Check cache first
        cache_key = f"{ticker}_{days}"
        if cache_key in self.data_cache:
            cached_data = self.data_cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_timeout:
                self.performance_stats['cache_hits'] += 1
                print("   ⚡ Using cached data")
                return cached_data['data']

        try:
            # Determine asset type and adjust ticker
            asset_type, yf_ticker = self._determine_asset_type_and_ticker(ticker)

            # Calculate period string with validation
            period = self._calculate_period_string(days)

            # Fetch data from Yahoo Finance with timeout
            print(f"   🔄 Requesting data for {yf_ticker} ({period})...")
            data = self.yf.download(yf_ticker, period=period, interval='1d', progress=False, timeout=30)

            # Validate response
            if data is None:
                return {'success': False, 'error': 'No response from Yahoo Finance'}

            if data.empty:
                return {'success': False, 'error': 'Empty dataset returned'}

            if len(data) < 5:
                return {'success': False, 'error': 'Insufficient data points (< 5)'}

            print(f"✅ Retrieved {len(data)} real data points from Yahoo Finance")

            # Data cleaning and validation
            cleaned_data = self._clean_and_validate_data(data)
            if cleaned_data is None:
                return {'success': False, 'error': 'Data cleaning failed'}

            # Calculate date range
            start_date = cleaned_data.index[0].date() if len(cleaned_data) > 0 else None
            end_date = cleaned_data.index[-1].date() if len(cleaned_data) > 0 else None

            # Calculate data quality metrics
            data_quality = self._assess_data_quality(cleaned_data)

            print(f"   📅 Date range: {start_date} to {end_date}")
            print(f"   📊 Data quality: {data_quality['score']:.1f}/10 ({data_quality['status']})")

            result = {
                'success': True,
                'data': cleaned_data,
                'ticker': ticker,
                'yf_ticker': yf_ticker,
                'points': len(cleaned_data),
                'latest_price': float(cleaned_data['close'].iloc[-1]) if len(cleaned_data) > 0 else 0,
                'date_range': f"{start_date} to {end_date}",
                'asset_type': asset_type,
                'data_source': 'Yahoo Finance',
                'data_quality': data_quality
            }

            # Cache successful results
            self.data_cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }

            # Update performance metrics
            response_time = time.time() - start_time
            self.performance_stats['requests_made'] += 1
            self.performance_stats['avg_response_time'] = (
                (self.performance_stats['avg_response_time'] * (self.performance_stats['requests_made'] - 1)) +
                response_time
            ) / self.performance_stats['requests_made']

            return result

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Market data fetch error: {error_msg[:100]}...")

            # Provide specific error messages
            if "404" in error_msg:
                return {'success': False, 'error': 'Ticker not found'}
            elif "timeout" in error_msg.lower():
                return {'success': False, 'error': 'Request timeout'}
            elif "network" in error_msg.lower():
                return {'success': False, 'error': 'Network connectivity issue'}
            else:
                return {'success': False, 'error': f'Yahoo Finance error: {error_msg[:50]}'}

        finally:
            # Update error count if needed
            if 'error' in locals() or not 'result' in locals():
                self.performance_stats['errors'] += 1

    def _determine_asset_type_and_ticker(self, ticker: str) -> tuple[str, str]:
        """Determine asset type and Yahoo Finance ticker"""
        # Crypto assets
        if ticker.upper() in ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOT', 'DOGE', 'AVAX']:
            return "crypto", f"{ticker.upper()}-USD"

        # Forex pairs
        elif '/' in ticker and len(ticker.split('/')) == 2:
            return "forex", ticker.replace('/', 'X')  # EURUSD becomes EURXUSD

        # Index assets
        elif ticker.startswith('^'):
            return "index", ticker

        # Commodity futures (basic support)
        elif ticker.upper() in ['GC=F', 'SI=F', 'CL=F', 'NG=F']:
            return "commodity", ticker.upper()

        # Default to US stock
        else:
            return "stock_us", ticker.upper()

    def _calculate_period_string(self, days: int) -> str:
        """Calculate appropriate period string for Yahoo Finance"""
        if days <= 7:
            return "1wk"
        elif days <= 30:
            return "1mo"
        elif days <= 90:
            return "3mo"
        elif days <= 180:
            return "6mo"
        elif days <= 365:
            return "1y"
        else:
            return "2y"

    def _clean_and_validate_data(self, data) -> pd.DataFrame:
        """Clean and validate downloaded data"""
        try:
            # Handle multi-index columns
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.droplevel(1)

            # Ensure required columns exist
            required_cols = ['Open', 'High', 'Low', 'Close']
            if not all(col in data.columns for col in required_cols):
                print("   ⚠️ Missing required columns, attempting to fill...")
                if 'Close' in data.columns:
                    for col in required_cols:
                        if col not in data.columns:
                            data[col] = data['Close']  # Fallback to close price

            # Add volume if missing
            if 'Volume' not in data.columns:
                data['Volume'] = 1000000  # Default volume

            # Rename to lowercase
            data = data.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })

            # Remove rows with all NaN values
            data = data.dropna(how='all')

            # Forward fill missing values (limited)
            data = data.fillna(method='ffill', limit=3)

            # Remove remaining NaN rows
            data = data.dropna()

            # Validate data integrity
            if len(data) < 3:
                return None

            # Check for reasonable price ranges
            close_prices = data['close']
            if close_prices.min() <= 0 or close_prices.max() > 1000000:
                print("   ⚠️ Unusual price ranges detected")
                return None

            return data

        except Exception as e:
            print(f"   ❌ Data cleaning error: {e}")
            return None

    def _assess_data_quality(self, data: pd.DataFrame) -> dict:
        """Assess data quality score"""
        try:
            score = 10.0

            # Completeness check
            null_pct = data.isnull().sum().sum() / (len(data) * len(data.columns))
            score -= null_pct * 2

            # Data length check
            if len(data) < 10:
                score -= 2
            elif len(data) < 20:
                score -= 1

            # Price consistency check
            close_prices = data['close']
            if close_prices.std() / close_prices.mean() > 0.5:  # High volatility
                score -= 0.5

            # Volume check
            if 'volume' in data.columns:
                avg_volume = data['volume'].mean()
                if avg_volume < 1000:
                    score -= 1

            score = max(0, min(10, score))

            if score >= 8:
                status = "Excellent"
            elif score >= 6:
                status = "Good"
            elif score >= 4:
                status = "Fair"
            else:
                status = "Poor"

            return {'score': score, 'status': status}

        except Exception:
            return {'score': 5.0, 'status': 'Unknown'}

    def calculate_real_indicators(self, data_dict: dict) -> dict:
        """Calculate technical indicators using real market data"""
        print("📈 Calculating technical indicators on real data...")

        if not data_dict.get('success', False):
            return {}

        data = data_dict['data']

        # Prepare data for indicators
        highs = data['high'] if 'high' in data.columns else data['close']
        lows = data['low'] if 'low' in data.columns else data['close']
        closes = data['close']
        volumes = data['volume'] if 'volume' in data.columns else pd.Series([1000] * len(data))

        results = {}

        # Calculate indicators using the real TechnicalIndicators class
        try:
            # Get all indicators at once
            all_indicators = self.indicators.get_all_indicators(highs, lows, closes, volumes)

            # Extract key indicators we need
            if 'sma_20' in all_indicators:
                results['sma_20'] = float(all_indicators['sma_20'].iloc[-1])
                print(f"  ✅ SMA(20): {results['sma_20']:.4f}")

            if 'rsi_14' in all_indicators:
                results['rsi'] = float(all_indicators['rsi_14'].iloc[-1])
                print(f"  ✅ RSI(14): {results['rsi']:.4f}")

            if 'macd_line' in all_indicators:
                results['macd'] = float(all_indicators['macd_line'].iloc[-1])
                print(f"  ✅ MACD: {results['macd']:.4f}")

            if 'macd_signal' in all_indicators:
                results['macd_signal'] = float(all_indicators['macd_signal'].iloc[-1])

            if 'macd_histogram' in all_indicators:
                results['macd_histogram'] = float(all_indicators['macd_histogram'].iloc[-1])

            if 'bb_upper' in all_indicators:
                results['bb_upper'] = float(all_indicators['bb_upper'].iloc[-1])
                results['bb_middle'] = float(all_indicators['bb_middle'].iloc[-1])
                results['bb_lower'] = float(all_indicators['bb_lower'].iloc[-1])
                print(f"  ✅ Bollinger Bands: Upper={results['bb_upper']:.4f}")

        except Exception as e:
            print(f"  ❌ Indicator calculation error: {str(e)[:50]}")
            # Fallback to basic calculations
            try:
                results['sma_20'] = float(closes.rolling(20).mean().iloc[-1])
                results['rsi'] = 50.0  # Neutral
                results['macd'] = 0.0
                results['macd_signal'] = 0.0
                results['macd_histogram'] = 0.0
                std = closes.rolling(20).std().iloc[-1]
                mean = closes.rolling(20).mean().iloc[-1]
                results['bb_upper'] = mean + 2 * std
                results['bb_middle'] = mean
                results['bb_lower'] = mean - 2 * std
                print(f"  ⚠️ Using fallback indicators")
            except Exception as e2:
                print(f"  ❌ Fallback failed: {str(e2)[:50]}")

        # Add current price
        results['close'] = float(closes.iloc[-1]) if not closes.empty else None

        return results

    def make_real_trading_decision(self, ticker: str, indicators: dict) -> dict:
        """Make real trading decision based on technical indicators"""
        print("🤖 Making real trading decision...")

        # Real signal analysis
        signals = self._analyze_real_signals(indicators)

        # Risk-adjusted decision making
        action, quantity, confidence, reasoning = self._make_risk_adjusted_decision(
            ticker, signals, indicators
        )

        return {
            'action': action,
            'quantity': quantity,
            'confidence': confidence,
            'reasoning': reasoning,
            'signals': signals
        }

    def _analyze_real_signals(self, indicators: dict) -> dict:
        """Analyze real market signals"""
        signals = {
            'buy_signals': 0,
            'sell_signals': 0,
            'neutral_signals': 0,
            'signal_strength': [],
            'momentum_score': 0.0
        }

        # RSI Analysis (Real market levels)
        if 'rsi' in indicators and indicators['rsi'] is not None:
            rsi = indicators['rsi']
            if rsi < 30:  # Oversold - real buy signal
                signals['buy_signals'] += 2
                signals['signal_strength'].append('Strong RSI Oversold')
            elif rsi < 40:  # Moderately oversold
                signals['buy_signals'] += 1
                signals['signal_strength'].append('RSI Oversold')
            elif rsi > 70:  # Overbought - real sell signal
                signals['sell_signals'] += 2
                signals['signal_strength'].append('Strong RSI Overbought')
            elif rsi > 60:  # Moderately overbought
                signals['sell_signals'] += 1
                signals['signal_strength'].append('RSI Overbought')
            else:
                signals['neutral_signals'] += 1

        # MACD Analysis (Real trend signals)
        if all(key in indicators and indicators[key] is not None
               for key in ['macd', 'macd_signal', 'macd_histogram']):
            macd = indicators['macd']
            signal = indicators['macd_signal']
            histogram = indicators['macd_histogram']

            if macd > signal and histogram > 0:  # Real bullish crossover
                signals['buy_signals'] += 2
                signals['signal_strength'].append('MACD Bullish Crossover')
                signals['momentum_score'] += 0.3
            elif macd > signal:  # Bullish
                signals['buy_signals'] += 1
                signals['signal_strength'].append('MACD Bullish')
                signals['momentum_score'] += 0.1
            elif macd < signal and histogram < 0:  # Real bearish crossover
                signals['sell_signals'] += 2
                signals['signal_strength'].append('MACD Bearish Crossover')
                signals['momentum_score'] -= 0.3
            elif macd < signal:  # Bearish
                signals['sell_signals'] += 1
                signals['signal_strength'].append('MACD Bearish')
                signals['momentum_score'] -= 0.1

        # Bollinger Bands Analysis (Real mean reversion)
        if all(key in indicators and indicators[key] is not None
               for key in ['bb_upper', 'bb_lower', 'close', 'bb_middle']):
            upper = indicators['bb_upper']
            lower = indicators['bb_lower']
            close = indicators['close']
            middle = indicators['bb_middle']

            bb_position = (close - lower) / (upper - lower) if upper != lower else 0.5

            if bb_position < 0.1:  # Real lower band touch
                signals['buy_signals'] += 2
                signals['signal_strength'].append('Bollinger Lower Band')
            elif bb_position < 0.25:  # Near lower band
                signals['buy_signals'] += 1
                signals['signal_strength'].append('Bollinger Lower Area')
            elif bb_position > 0.9:  # Real upper band touch
                signals['sell_signals'] += 2
                signals['signal_strength'].append('Bollinger Upper Band')
            elif bb_position > 0.75:  # Near upper band
                signals['sell_signals'] += 1
                signals['signal_strength'].append('Bollinger Upper Area')
            elif abs(close - middle) / middle < 0.02:  # Near middle (consolidation)
                signals['neutral_signals'] += 1

        # Moving Average Analysis (Real trend)
        if all(key in indicators and indicators[key] is not None
               for key in ['sma_20', 'close']):
            sma = indicators['sma_20']
            close = indicators['close']

            price_vs_ma = (close - sma) / sma

            if price_vs_ma > 0.05:  # Significantly above MA
                signals['buy_signals'] += 1
                signals['signal_strength'].append('Above MA +5%')
                signals['momentum_score'] += 0.2
            elif price_vs_ma > 0.02:  # Moderately above MA
                signals['buy_signals'] += 0.5
                signals['momentum_score'] += 0.1
            elif price_vs_ma < -0.05:  # Significantly below MA
                signals['sell_signals'] += 1
                signals['signal_strength'].append('Below MA -5%')
                signals['momentum_score'] -= 0.2
            elif price_vs_ma < -0.02:  # Moderately below MA
                signals['sell_signals'] += 0.5
                signals['momentum_score'] -= 0.1

        return signals

    def _make_risk_adjusted_decision(self, ticker: str, signals: dict, indicators: dict) -> tuple:
        """Make risk-adjusted trading decision"""

        buy_strength = signals['buy_signals']
        sell_strength = signals['sell_signals']
        momentum = signals.get('momentum_score', 0)

        # Enhanced decision logic with real market considerations
        signal_diff = buy_strength - sell_strength
        signal_magnitude = abs(signal_diff)

        # Risk factors from real market data
        current_price = indicators.get('close', 100)  # Default fallback

        # Position sizing based on real risk management
        base_quantity = 100

        # Volatility adjustment (rough estimate from price movement)
        if 'bb_upper' in indicators and 'bb_lower' in indicators:
            upper = indicators['bb_upper']
            lower = indicators['bb_lower']
            if upper > lower:
                volatility_ratio = (upper - lower) / current_price
                volatility_multiplier = 1.0 - min(0.5, volatility_ratio * 2)  # Reduce size in high volatility
            else:
                volatility_multiplier = 1.0
        else:
            volatility_multiplier = 1.0

        # Momentum adjustment
        momentum_multiplier = 0.7 + (momentum * 0.6)  # 0.7 to 1.3 range

        # Final decision
        if signal_magnitude >= 2.5:  # Very strong conviction
            if signal_diff > 0:
                action = "buy"
                quantity = int(base_quantity * volatility_multiplier * momentum_multiplier)
                confidence = min(95, 70 + (signal_magnitude * 6))
                reasoning_parts = ["VERY STRONG BUY signal"]
            else:
                action = "sell"
                quantity = int(base_quantity * volatility_multiplier * momentum_multiplier)
                confidence = min(95, 70 + (signal_magnitude * 6))
                reasoning_parts = ["VERY STRONG SELL signal"]

        elif signal_magnitude >= 1.5:  # Strong conviction
            if signal_diff > 0:
                action = "buy"
                quantity = int(base_quantity * 0.8 * volatility_multiplier * momentum_multiplier)
                confidence = min(90, 60 + (signal_magnitude * 8))
                reasoning_parts = ["Strong BUY signal"]
            else:
                action = "sell"
                quantity = int(base_quantity * 0.8 * volatility_multiplier * momentum_multiplier)
                confidence = min(90, 60 + (signal_magnitude * 8))
                reasoning_parts = ["Strong SELL signal"]

        elif signal_magnitude >= 0.8:  # Moderate conviction
            if signal_diff > 0:
                action = "buy"
                quantity = int(base_quantity * 0.6 * volatility_multiplier)
                confidence = min(80, 50 + (signal_magnitude * 10))
                reasoning_parts = ["Moderate BUY signal"]
            else:
                action = "sell"
                quantity = int(base_quantity * 0.6 * volatility_multiplier)
                confidence = min(80, 50 + (signal_magnitude * 10))
                reasoning_parts = ["Moderate SELL signal"]

        else:  # No clear signal
            action = "hold"
            quantity = 0
            confidence = 50
            reasoning_parts = ["HOLD - signals unclear"]

        # Add signal details to reasoning
        if signals['signal_strength']:
            reasoning_parts.append(f"Signals: {', '.join(signals['signal_strength'][:3])}")

        # Add market context
        if momentum > 0.2:
            reasoning_parts.append("Strong momentum detected")
        elif momentum < -0.2:
            reasoning_parts.append("Weak momentum detected")

        # Ensure minimum quantity for action
        if action in ["buy", "sell"] and quantity < 10:
            quantity = 10  # Minimum position size

        reasoning = " | ".join(reasoning_parts)

        return action, quantity, confidence, reasoning

    def analyze_real_asset(self, ticker: str) -> dict:
        """Complete real analysis pipeline for one asset"""
        print(f"\n🚀 REAL ANALYSIS FOR {ticker}")
        print("=" * 50)

        # Fetch real market data
        data_result = self.fetch_real_data(ticker)
        if not data_result.get('success', False):
            return {"error": data_result.get('error', 'Unknown error'), "ticker": ticker}

        # Calculate real technical indicators
        indicators = self.calculate_real_indicators(data_result)

        # Make real trading decision
        decision = self.make_real_trading_decision(ticker, indicators)

        # Prepare comprehensive result
        result = {
            "ticker": ticker,
            "analysis_type": "REAL_MARKET_DATA",
            "data_source": "Yahoo Finance",
            "data_points": data_result.get('points', 0),
            "date_range": data_result.get('date_range', 'Unknown'),
            "latest_price": data_result.get('latest_price', 0),
            "indicators_calculated": len([k for k in indicators.keys() if k != 'close']),
            "indicators": indicators,
            "decision": decision,
            "timestamp": datetime.now().isoformat(),
            "system_version": "REAL_IMPLEMENTATION_v1.0"
        }

        return result

    def analyze_real_portfolio(self, tickers: list) -> dict:
        """Analyze real portfolio with multiple assets"""
        print(f"\n🌟 REAL PORTFOLIO ANALYSIS: {', '.join(tickers)}")
        print("=" * 70)

        results = {}
        portfolio_summary = {
            'total_assets': len(tickers),
            'successful_analyses': 0,
            'failed_analyses': 0,
            'buy_signals': 0,
            'sell_signals': 0,
            'hold_signals': 0,
            'total_confidence': 0,
            'average_confidence': 0
        }

        for ticker in tickers:
            result = self.analyze_real_asset(ticker)
            results[ticker] = result

            if 'error' in result:
                portfolio_summary['failed_analyses'] += 1
                print(f"❌ {ticker}: Analysis failed - {result['error']}")
            else:
                portfolio_summary['successful_analyses'] += 1
                decision = result.get('decision', {})
                action = decision.get('action', 'unknown').upper()

                if action == 'BUY':
                    portfolio_summary['buy_signals'] += 1
                elif action == 'SELL':
                    portfolio_summary['sell_signals'] += 1
                else:
                    portfolio_summary['hold_signals'] += 1

                confidence = decision.get('confidence', 0)
                portfolio_summary['total_confidence'] += confidence

                print(f"📈 {ticker}: {action} ({confidence}% confidence)")

        # Calculate average confidence
        if portfolio_summary['successful_analyses'] > 0:
            portfolio_summary['average_confidence'] = portfolio_summary['total_confidence'] / portfolio_summary['successful_analyses']

        # Add performance summary
        portfolio_result = {
            'portfolio_summary': portfolio_summary,
            'asset_analyses': results,
            'analysis_timestamp': datetime.now().isoformat(),
            'system_performance': self.get_performance_stats()
        }

        return portfolio_result

    def get_performance_stats(self) -> dict:
        """Get system performance statistics"""
        total_requests = self.performance_stats['requests_made']
        cache_hits = self.performance_stats['cache_hits']
        errors = self.performance_stats['errors']

        cache_hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0
        error_rate = (errors / total_requests * 100) if total_requests > 0 else 0

        return {
            'total_requests': total_requests,
            'cache_hits': cache_hits,
            'cache_hit_rate': f"{cache_hit_rate:.1f}%",
            'errors': errors,
            'error_rate': f"{error_rate:.1f}%",
            'avg_response_time': f"{self.performance_stats['avg_response_time']:.2f}s",
            'cache_size': len(self.data_cache)
        }


def main():
    """Main launcher function with real implementation"""
    print("""
🤖 AI HEDGE FUND - REAL MARKET DATA TRADING SYSTEM
📊 Production-Ready | Live Data | Algorithmic Trading
====================================================
    """)

    parser = argparse.ArgumentParser(
        description='AI Hedge Fund Real Trading System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Real Market Data Examples:
  python real_launcher.py AAPL              # Single asset real analysis
  python real_launcher.py AAPL,MSFT,GOOGL  # Multi-asset real analysis
  python real_launcher.py BTC,ETH          # Crypto real analysis

Features:
  ✅ Real Yahoo Finance market data
  ✅ Live technical indicators
  ✅ Risk-adjusted position sizing
  ✅ Professional algorithmic decisions
        """
    )

    parser.add_argument(
        'tickers',
        help='Stock/crypto tickers to analyze (comma-separated)'
    )

    parser.add_argument(
        '--days', '-d',
        type=int,
        default=30,
        help='Historical data period in days (default: 30)'
    )

    parser.add_argument(
        '--real-data',
        action='store_true',
        help='Use real market data (default: enabled)'
    )

    args = parser.parse_args()

    # Parse tickers
    tickers = [t.strip().upper() for t in args.tickers.split(',') if t.strip()]

    if not tickers:
        parser.print_help()
        return

    # Initialize real trading system
    system = RealTradingSystem()

    try:
        if len(tickers) == 1:
            # Single asset real analysis
            result = system.analyze_real_asset(tickers[0])

            print(f"\n📋 REAL ANALYSIS RESULT FOR {tickers[0]}")
            print("=" * 50)

            if 'error' in result:
                print(f"❌ Analysis failed: {result['error']}")
                return

            # Enhanced output with data quality and performance
            data_quality = result.get('data_quality', {})
            data_quality = result.get('data_quality', {})
            print(f"Data Source: {result.get('data_source', 'Unknown')}")
            print(f"Asset Type: {result.get('asset_type', 'stock_us').replace('_', ' ').title()}")
            print(f"Data Quality: {data_quality.get('status', 'Unknown')} ({data_quality.get('score', 0):.1f}/10)")
            print(f"Data Points: {result.get('data_points', 0)}")
            print(f"Date Range: {result.get('date_range', 'Unknown')}")
            print(f"Latest Price: ${result.get('latest_price', 0):.2f}")

            # Indicators summary
            indicators_count = result.get('indicators_calculated', 0)
            indicators_data = result.get('indicators', {})

            print(f"\\n📊 TECHNICAL ANALYSIS:")
            print(f"Indicators Calculated: {indicators_count}")

            if indicators_data:
                # Show key indicators
                if 'sma_20' in indicators_data and indicators_data['sma_20']:
                    sma = indicators_data['sma_20']
                    close = indicators_data.get('close', 0)
                    trend = "ABOVE" if close > sma else "BELOW"
                    print(f"  • SMA(20): ${sma:.2f} (Price {trend})")

                if 'rsi' in indicators_data and indicators_data['rsi']:
                    rsi = indicators_data['rsi']
                    level = "OVERBOUGHT" if rsi > 70 else "OVERSOLD" if rsi < 30 else "NEUTRAL"
                    print(f"  • RSI(14): {rsi:.1f} ({level})")

                if 'bb_upper' in indicators_data and indicators_data['bb_upper']:
                    upper = indicators_data['bb_upper']
                    lower = indicators_data['bb_lower']
                    close = indicators_data.get('close', 0)
                    if close > upper:
                        position = "ABOVE UPPER BAND"
                    elif close < lower:
                        position = "BELOW LOWER BAND"
                    else:
                        position = "WITHIN BANDS"
                    print(f"  • Bollinger Bands: Position {position}")

            decision = result.get('decision', {})
            print("\\n🎯 TRADING DECISION:")
            print(f"Action: {decision.get('action', 'UNKNOWN').upper()}")
            print(f"Quantity: {decision.get('quantity', 0)} shares")
            print(f"Confidence: {decision.get('confidence', 0)}%")
            print(f"Reasoning: {decision.get('reasoning', 'No reasoning provided')}")

            # Show key signals
            signals = decision.get('signals', {})
            if signals.get('signal_strength'):
                print(f"\\nKey Signals: {', '.join(signals['signal_strength'][:3])}")

            # Show momentum if available
            momentum_score = signals.get('momentum_score', 0)
            if abs(momentum_score) > 0.1:
                momentum_desc = "BULLISH" if momentum_score > 0 else "BEARISH"
                print(f"Momentum: {momentum_desc} ({abs(momentum_score):.2f})")

        else:
            # Multi-asset real analysis
            portfolio_result = system.analyze_real_portfolio(tickers)

            print("\\n📋 REAL PORTFOLIO ANALYSIS SUMMARY")
            print("=" * 60)

            summary = portfolio_result.get('portfolio_summary', {})
            perf_stats = portfolio_result.get('system_performance', {})

            # Portfolio overview
            print(f"📊 PORTFOLIO OVERVIEW:")
            print(f"   Total Assets Analyzed: {summary.get('total_assets', 0)}")
            print(f"   Successful Analyses: {summary.get('successful_analyses', 0)}")
            print(f"   Failed Analyses: {summary.get('failed_analyses', 0)}")

            # Trading signals summary
            print(f"\\n🎯 TRADING SIGNALS:")
            print(f"   BUY Signals: {summary.get('buy_signals', 0)}")
            print(f"   SELL Signals: {summary.get('sell_signals', 0)}")
            print(f"   HOLD Signals: {summary.get('hold_signals', 0)}")
            print(f"   Average Confidence: {summary.get('average_confidence', 0):.1f}%")

            # System performance
            if perf_stats:
                print(f"\\n⚡ SYSTEM PERFORMANCE:")
                print(f"   Total Requests: {perf_stats.get('total_requests', 0)}")
                print(f"   Cache Hit Rate: {perf_stats.get('cache_hit_rate', '0%')}")
                print(f"   Error Rate: {perf_stats.get('error_rate', '0%')}")
                print(f"   Avg Response Time: {perf_stats.get('avg_response_time', '0s')}")
                print(f"   Cache Size: {perf_stats.get('cache_size', 0)} items")

            print("\\n📊 DETAILED REAL RESULTS:")
            asset_analyses = portfolio_result.get('asset_analyses', {})
            successful_tickers = []
            failed_tickers = []

            for ticker, result in asset_analyses.items():
                if 'error' in result:
                    failed_tickers.append(f"{ticker}: {result['error']}")
                else:
                    decision = result.get('decision', {})
                    action = decision.get('action', 'unknown').upper()
                    confidence = decision.get('confidence', 0)
                    latest_price = result.get('latest_price', 0)
                    successful_tickers.append(f"{ticker}: {action} ({confidence}%) @ ${latest_price:.2f}")

            # Show successful results
            if successful_tickers:
                print("✅ SUCCESSFUL ANALYSES:")
                for result in successful_tickers:
                    print(f"   📈 {result}")

            # Show failed results
            if failed_tickers:
                print("\\n❌ FAILED ANALYSES:")
                for result in failed_tickers:
                    print(f"   ❌ {result}")

        print("\\n✅ Real Market Analysis Complete!")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("📊 Data Source: Yahoo Finance (Live Market Data)")
        print("🔧 System: Enhanced with caching, error handling, and performance monitoring")

    except KeyboardInterrupt:
        print("\n⏹️  Real analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Real analysis failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()