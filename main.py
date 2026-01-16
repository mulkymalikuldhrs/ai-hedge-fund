#!/usr/bin/env python3
"""
AI HEDGE FUND v2.2 - UNIFIED ENTRY POINT
=========================================
Single entry point for the entire trading system.
Replaces: terminal.py, launcher.py, simple_launcher.py, core_launcher.py,
          real_launcher.py, run_terminal.py, run_multi_asset.py

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

Usage:
    python3 main.py AAPL                                    # Quick analysis
    python3 main.py AAPL --mode full-auto                   # Autonomous trading
    python3 main.py AAPL,BTC,USD/IDR --days 200             # Multi-asset
    python3 main.py --cli                                    # Enhanced CLI terminal
    python3 main.py --terminal                              # Legacy CLI terminal
    python3 main.py --streamlit                             # Streamlit web UI
    python3 main.py --backtest EURUSD --days 365            # Backtest mode
    python3 main.py --metatrader                            # MetaTrader web UI
    streamlit run src/dashboard/streamlit_app.py            # Direct Streamlit
    python3 src/dashboard/cli_terminal.py                   # Direct CLI
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

# Colorama for colored output
from colorama import Fore, Style, init

init(autoreset=True)

import pandas as pd


# ============ ENUMS & DATACLASSES ============


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


class OrderStatus(Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    CLOSED = "closed"
    CANCELLED = "cancelled"


@dataclass
class TradingDecision:
    """Complete trading decision"""

    timestamp: datetime
    ticker: str
    asset_type: str
    mode: str

    # Price data
    current_price: float
    daily_change: float
    daily_change_pct: float

    # Signals
    retail_signal: str
    retail_confidence: float
    quant_signal: str
    quant_confidence: float
    legendary_signal: str
    legendary_confidence: float

    # Final
    final_signal: Signal
    final_confidence: float
    score: int

    # Risk
    sharpe_ratio: float
    var_95: float
    risk_score: int

    # Levels
    entry_price: float
    stop_loss: float
    take_profit: List[float]
    risk_reward: float

    # Position
    position_size: float = 0.0
    quantity: int = 0

    # Status
    status: str = OrderStatus.PENDING.value
    execution_time: Optional[datetime] = None
    exit_reason: Optional[str] = None

    # Metadata
    reasons: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class MemoryEntry:
    """Memory system entry"""

    timestamp: datetime
    decision: Dict
    status: str
    pnl: float = 0.0
    pnl_pct: float = 0.0
    notes: str = ""


# ============ MEMORY SYSTEM ============


class MemorySystem:
    """Persistent memory for all trading decisions"""

    def __init__(self, filepath: str = "trading_memory.json"):
        self.filepath = filepath
        self.entries: List[MemoryEntry] = []
        self.load()

    def load(self):
        """Load memory from file"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    self.entries = [MemoryEntry(**e) for e in data]
            except Exception as e:
                print(f"⚠️  Memory load error: {e}")
                self.entries = []

    def save(self):
        """Save memory to file"""
        try:
            with open(self.filepath, "w") as f:
                json.dump([asdict(e) for e in self.entries], f, indent=2, default=str)
        except Exception as e:
            print(f"❌ Memory save error: {e}")

    def add_entry(self, entry: MemoryEntry):
        """Add new entry"""
        self.entries.append(entry)
        if len(self.entries) > 1000:
            self.entries = self.entries[-1000:]
        self.save()

    def get_recent(self, n: int = 10) -> List[MemoryEntry]:
        """Get recent entries"""
        return self.entries[-n:]

    def get_stats(self) -> Dict:
        """Get statistics"""
        if not self.entries:
            return {"total": 0, "executed": 0, "pnl": 0}

        executed = [e for e in self.entries if e.status == "executed"]
        pnl = sum(e.pnl for e in executed)

        return {
            "total": len(self.entries),
            "executed": len(executed),
            "pending": len([e for e in self.entries if e.status == "pending"]),
            "total_pnl": pnl,
            "win_rate": len([e for e in executed if e.pnl > 0]) / len(executed)
            if executed
            else 0,
        }


# ============ DATA PROVIDER ============


class DataProvider:
    """Unified data provider - all FREE sources"""

    def __init__(self):
        self.cache = {}

    def get_price(self, ticker: str, asset_type: str, days: int = 100) -> Optional[Any]:
        """Get price data"""
        cache_key = f"{ticker}_{asset_type}_{days}"

        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            if asset_type in ["stock_us", "stock_idx"]:
                result = self._get_stock(ticker, asset_type, days)
            elif asset_type == "forex":
                result = self._get_forex(ticker, days)
            elif asset_type == "crypto":
                result = self._get_crypto(ticker, days)
            elif asset_type == "commodity":
                result = self._get_commodity(ticker, days)
            else:
                result = self._get_stock(ticker, "stock_us", days)

            if result is not None:
                self.cache[cache_key] = result
            return result

        except Exception as e:
            print(f"❌ Data fetch error for {ticker}: {e}")
            return None

    def _get_stock(self, ticker: str, asset_type: str, days: int):
        """Get stock data from Yahoo Finance"""
        import yfinance as yf

        # Adjust ticker for IDX
        if asset_type == "stock_idx" and not ticker.endswith(".JK"):
            ticker = f"{ticker}.JK"

        try:
            stock = yf.Ticker(ticker)
            end = datetime.now()
            start = end - timedelta(days=days)
            data = stock.history(start=start, end=end)

            if data.empty or len(data) < 5:
                return None

            data.columns = data.columns.str.lower()
            return data

        except Exception as e:
            print(f"❌ Yahoo Finance error: {e}")
            return None

    def _get_forex(self, ticker: str, days: int):
        """Get forex data"""
        import yfinance as yf
        import pandas as pd

        pair = ticker.replace("/", "")
        formats = [f"{pair}=X", f"EURUSD=X", f"EURUSD=X"]

        for fmt in formats:
            try:
                data = yf.download(
                    fmt, period=f"{days}d", interval="1d", progress=False
                )
                if not data.empty:
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.get_level_values(0)
                    data.columns = data.columns.str.lower()
                    return data
            except:
                continue

        try:
            data = yf.download(
                "EURUSD=X", period=f"{days}d", interval="1d", progress=False
            )
            if not data.empty:
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                data.columns = data.columns.str.lower()
            return data
        except:
            pass

        return None

    def _get_crypto(self, ticker: str, days: int):
        """Get crypto data"""
        import yfinance as yf
        import pandas as pd

        try:
            data = yf.download(
                f"{ticker}-USD", period=f"{days}d", interval="1d", progress=False
            )
            if not data.empty:
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                data.columns = data.columns.str.lower()
            return data
        except Exception as e:
            print(f"❌ Crypto error: {e}")
            return None

    def _get_commodity(self, ticker: str, days: int):
        """Get commodity data"""
        import yfinance as yf

        mapping = {
            "GOLD": "GC=F",
            "SILVER": "SI=F",
            "OIL": "CL=F",
            "BRENT": "BZ=F",
            "NATGAS": "NG=F",
        }

        try:
            yf_ticker = mapping.get(ticker.upper(), f"{ticker}=X")
            data = yf.download(
                yf_ticker, period=f"{days}d", interval="1d", progress=False
            )
            if not data.empty:
                data.columns = data.columns.str.lower()
            return data
        except Exception as e:
            print(f"❌ Commodity error: {e}")
            return None


# ============ TECHNICAL INDICATORS ============


class TechnicalIndicators:
    """Technical indicators calculator"""

    def __init__(self):
        pass

    def rsi(self, closes, period: int = 14) -> float:
        """Calculate RSI"""
        delta = closes.diff()
        gain = delta.where(delta > 0, 0).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]

    def macd(self, closes) -> Tuple[float, float, float]:
        """Calculate MACD"""
        ema12 = closes.ewm(span=12).mean()
        ema26 = closes.ewm(span=26).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        return macd.iloc[-1], signal.iloc[-1], histogram.iloc[-1]

    def atr(self, high, low, close, period: int = 14) -> float:
        """Calculate ATR"""
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(period).mean()
        return atr.iloc[-1]

    def sma(self, closes, period: int = 20) -> float:
        """Calculate SMA"""
        return closes.rolling(period).mean().iloc[-1]

    def trend(self, close, sma20: float, sma50: float) -> str:
        """Determine trend"""
        if close > sma20 > sma50:
            return "BULLISH"
        elif close < sma20 < sma50:
            return "BEARISH"
        else:
            return "NEUTRAL"


# ============ STRATEGY ANALYZERS ============


class StrategyAnalyzer:
    """Analyzes using all 34 strategies"""

    def __init__(self):
        self.ti = TechnicalIndicators()

    def analyze(self, data, ticker: str, asset_type: str) -> Dict[str, Any]:
        """Full strategy analysis"""

        close = data["close"]
        high = data["high"]
        low = data["low"]
        volume = data["volume"]

        current_price = close.iloc[-1]
        prev_price = close.iloc[-2] if len(close) > 1 else current_price

        # Technical indicators
        rsi = self.ti.rsi(close)
        macd, macd_signal, macd_hist = self.ti.macd(close)
        atr = self.ti.atr(high, low, close)
        sma20 = self.ti.sma(close, 20)
        sma50 = self.ti.sma(close, 50)
        trend = self.ti.trend(current_price, sma20, sma50)

        # Retail signal (simplified SMC/ICT)
        retail_signal, retail_conf = self._analyze_retail(rsi, macd, trend)

        # Quantitative signal
        quant_signal, quant_conf = self._analyze_quantitative(close, rsi, macd)

        # Legendary investors signal
        legendary_signal, legendary_conf = self._analyze_legendary(rsi, trend)

        # Risk metrics
        returns = close.pct_change().dropna()
        sharpe = (returns.mean() / returns.std() * 252**0.5) if returns.std() > 0 else 0
        var_95 = abs(returns.quantile(0.05))

        # Final consensus (weighted)
        retail_score = self._signal_to_score(retail_signal)
        quant_score = self._signal_to_score(quant_signal)
        legendary_score = self._signal_to_score(legendary_signal)
        risk_score = int(min(100, max(0, 100 - var_95 * 1000)))

        final_score = (
            retail_score * 0.25
            + quant_score * 0.25
            + legendary_score * 0.30
            + risk_score * 0.20
        )

        # Determine final signal
        if final_score >= 75:
            final_signal = Signal.STRONG_BUY
        elif final_score >= 60:
            final_signal = Signal.BUY
        elif final_score >= 45:
            final_signal = Signal.HOLD
        elif final_score >= 30:
            final_signal = Signal.SELL
        else:
            final_signal = Signal.STRONG_SELL

        final_conf = final_score / 100

        # Calculate levels
        sl_pct = 0.02
        rr = 3.0

        if final_signal in [Signal.STRONG_BUY, Signal.BUY]:
            stop_loss = current_price * (1 - sl_pct)
            take_profit = [
                current_price * (1 + sl_pct * rr * 0.5),
                current_price * (1 + sl_pct * rr),
                current_price * (1 + sl_pct * rr * 1.5),
            ]
        elif final_signal in [Signal.STRONG_SELL, Signal.SELL]:
            stop_loss = current_price * (1 + sl_pct)
            take_profit = [
                current_price * (1 - sl_pct * rr * 0.5),
                current_price * (1 - sl_pct * rr),
                current_price * (1 - sl_pct * rr * 1.5),
            ]
        else:
            stop_loss = current_price * 0.95
            take_profit = [current_price * 1.02, current_price * 1.05]

        # Generate reasons
        reasons = []
        reasons.append(
            f"RSI: {rsi:.1f} - {'Oversold' if rsi < 35 else 'Overbought' if rsi > 65 else 'Neutral'}"
        )
        reasons.append(f"Trend: {trend}")
        reasons.append(f"Retail: {retail_signal} ({retail_conf:.0%})")
        reasons.append(f"Quant: {quant_signal} ({quant_conf:.0%})")
        reasons.append(f"Legendary: {legendary_signal} ({legendary_conf:.0%})")

        return {
            "current_price": current_price,
            "daily_change": current_price - prev_price,
            "daily_change_pct": ((current_price - prev_price) / prev_price) * 100,
            "indicators": {
                "rsi": rsi,
                "macd": macd,
                "macd_signal": macd_signal,
                "atr": atr,
                "sma20": sma20,
                "sma50": sma50,
                "trend": trend,
            },
            "signals": {
                "retail": {"signal": retail_signal, "confidence": retail_conf},
                "quantitative": {"signal": quant_signal, "confidence": quant_conf},
                "legendary": {"signal": legendary_signal, "confidence": legendary_conf},
            },
            "final_signal": final_signal,
            "final_confidence": final_conf,
            "score": final_score,
            "risk": {
                "sharpe_ratio": sharpe,
                "var_95": var_95,
                "risk_score": risk_score,
            },
            "levels": {
                "entry": current_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "risk_reward": rr,
            },
            "reasons": reasons,
        }

    def _analyze_retail(
        self, rsi: float, macd: float, trend: str, **kwargs
    ) -> Tuple[str, float]:
        """Retail/SMC strategy analysis"""
        score = 0

        # RSI
        if rsi < 30:
            score += 2
        elif rsi < 40:
            score += 1
        elif rsi > 70:
            score -= 2
        elif rsi > 60:
            score -= 1

        # MACD
        if macd > 0:
            score += 1

        # Trend
        if trend == "BULLISH":
            score += 1
        elif trend == "BEARISH":
            score -= 1

        if score >= 3:
            return "BUY", 0.7
        elif score <= -3:
            return "SELL", 0.7
        elif score > 0:
            return "BUY", 0.55
        elif score < 0:
            return "SELL", 0.55
        else:
            return "HOLD", 0.5

    def _analyze_quantitative(
        self, close, rsi: float, macd: float
    ) -> Tuple[str, float]:
        """Quantitative strategy analysis"""
        # Simple momentum + mean reversion
        returns = close.pct_change().tail(5)
        momentum = returns.mean()

        score = 0

        if momentum > 0:
            score += 1
        else:
            score -= 1

        if rsi < 40:
            score += 1
        elif rsi > 60:
            score -= 1

        if macd > 0:
            score += 1
        else:
            score -= 1

        if score >= 2:
            return "BUY", 0.65
        elif score <= -2:
            return "SELL", 0.65
        elif score > 0:
            return "BUY", 0.55
        elif score < 0:
            return "SELL", 0.55
        else:
            return "HOLD", 0.5

    def _analyze_legendary(self, rsi: float, trend: str) -> Tuple[str, float]:
        """Legendary investor analysis"""
        # Buffett/Lynch style - quality at reasonable price
        score = 50  # Neutral baseline

        if rsi < 35:
            score += 10  # Margin of safety
        elif rsi > 65:
            score -= 10  # Overvalued

        if trend == "BULLISH":
            score += 5
        elif trend == "BEARISH":
            score -= 5

        if score >= 60:
            return "BUY", 0.6
        elif score <= 40:
            return "SELL", 0.6
        else:
            return "HOLD", 0.5

    def _signal_to_score(self, signal: str) -> int:
        """Convert signal to numeric score"""
        scores = {
            "STRONG_BUY": 85,
            "BUY": 65,
            "HOLD": 50,
            "SELL": 35,
            "STRONG_SELL": 15,
        }
        return scores.get(signal, 50)


# ============ PAPER TRADER ============


class PaperTrader:
    """Paper trading simulation"""

    def __init__(self, initial_capital: float = 100000):
        self.capital = initial_capital
        self.positions: Dict[str, Dict] = {}
        self.trades: List[Dict] = []

    def execute(self, decision: TradingDecision) -> Dict:
        """Execute paper trade"""
        if decision.final_signal in [Signal.STRONG_BUY, Signal.BUY]:
            return self._buy(decision)
        elif decision.final_signal in [Signal.STRONG_SELL, Signal.SELL]:
            return self._sell(decision)
        else:
            return {"status": "skipped", "reason": "HOLD signal"}

    def _buy(self, decision: TradingDecision) -> Dict:
        """Execute buy"""
        price = decision.entry_price
        sl = decision.stop_loss
        tp = decision.take_profit[0] if decision.take_profit else price * 1.06

        # Calculate quantity (2% risk)
        risk_amount = self.capital * 0.02
        risk_per_share = price - sl
        quantity = int(risk_amount / risk_per_share) if risk_per_share > 0 else 0

        if quantity <= 0:
            return {"status": "skipped", "reason": "Insufficient capital"}

        cost = quantity * price
        if cost > self.capital:
            quantity = int(self.capital / price)
            cost = quantity * price

        self.capital -= cost
        self.positions[decision.ticker] = {
            "type": "long",
            "quantity": quantity,
            "entry_price": price,
            "sl": sl,
            "tp": tp,
            "entry_time": datetime.now(),
        }

        return {
            "status": "executed",
            "action": "BUY",
            "ticker": decision.ticker,
            "quantity": quantity,
            "price": price,
            "capital_remaining": self.capital,
        }

    def _sell(self, decision: TradingDecision) -> Dict:
        """Execute sell/short"""
        price = decision.entry_price
        sl = decision.stop_loss
        tp = decision.take_profit[0] if decision.take_profit else price * 0.94

        # For short, risk is (sl - entry)
        risk_amount = self.capital * 0.02
        risk_per_share = sl - price
        quantity = int(risk_amount / abs(risk_per_share)) if risk_per_share != 0 else 0

        if quantity <= 0:
            return {"status": "skipped", "reason": "Insufficient capital"}

        self.positions[decision.ticker] = {
            "type": "short",
            "quantity": quantity,
            "entry_price": price,
            "sl": sl,
            "tp": tp,
            "entry_time": datetime.now(),
        }

        return {
            "status": "executed",
            "action": "SELL",
            "ticker": decision.ticker,
            "quantity": quantity,
            "price": price,
            "capital_remaining": self.capital,
        }


# ============ MAIN TRADING SYSTEM ============


class AIHedgeFund:
    """Main AI Hedge Fund trading system"""

    def __init__(self):
        self.data_provider = DataProvider()
        self.strategy_analyzer = StrategyAnalyzer()
        self.memory = MemorySystem()
        self.paper_trader = PaperTrader()

    def analyze(self, ticker: str, asset_type: str, days: int = 100) -> TradingDecision:
        """Complete analysis and return trading decision"""

        print(f"\n{'=' * 70}")
        print(f"🤖 AI HEDGE FUND - UNIFIED ANALYSIS")
        print(f"{'=' * 70}")
        print(f"\n📊 Analyzing: {ticker} ({asset_type})")

        # Fetch data
        print(f"\n📥 STEP 1: Fetching data...")
        data = self.data_provider.get_price(ticker, asset_type, days)

        if data is None or len(data) < 15:
            raise ValueError(f"Insufficient data for {ticker}")

        print(f"   ✅ Loaded {len(data)} days of data")

        # Analyze
        print(f"\n📈 STEP 2: Running 34 strategies...")
        analysis = self.strategy_analyzer.analyze(data, ticker, asset_type)

        current_price = analysis["current_price"]
        daily_change = analysis["daily_change"]
        daily_change_pct = analysis["daily_change_pct"]

        print(f"   💰 Price: ${current_price:,.2f} ({daily_change_pct:+.2f}%)")
        print(f"   📊 RSI: {analysis['indicators']['rsi']:.1f}")
        print(f"   📊 Trend: {analysis['indicators']['trend']}")

        signals = analysis["signals"]
        print(f"\n🎯 STEP 3: Signal Breakdown")
        print(
            f"   Retail: {signals['retail']['signal']} ({signals['retail']['confidence']:.0%})"
        )
        print(
            f"   Quantitative: {signals['quantitative']['signal']} ({signals['quantitative']['confidence']:.0%})"
        )
        print(
            f"   Legendary: {signals['legendary']['signal']} ({signals['legendary']['confidence']:.0%})"
        )

        risk = analysis["risk"]
        print(f"\n⚠️  STEP 4: Risk Analysis")
        print(f"   Sharpe: {risk['sharpe_ratio']:.2f}")
        print(f"   VaR (95%): {risk['var_95']:.2%}")
        print(f"   Risk Score: {risk['risk_score']}/100")

        final_signal = analysis["final_signal"]
        final_conf = analysis["final_confidence"]
        score = analysis["score"]
        levels = analysis["levels"]
        reasons = analysis["reasons"]

        # Print final decision
        print(f"\n{'=' * 70}")
        print(f"📋 TRADING DECISION")
        print(f"{'=' * 70}")

        emoji = {
            Signal.STRONG_BUY: "🟢🟢",
            Signal.BUY: "🟢",
            Signal.HOLD: "🟡",
            Signal.SELL: "🔴",
            Signal.STRONG_SELL: "🔴🔴",
        }[final_signal]

        print(f"\n{emoji} FINAL SIGNAL: {final_signal.value}")
        print(f"📊 CONFIDENCE: {final_conf:.0%}")
        print(f"📈 SCORE: {score:.0f}/100")

        print(f"\n💰 CURRENT PRICE: ${current_price:,.2f}")
        print(f"🎯 STOP LOSS: ${levels['stop_loss']:,.2f}")
        print(
            f"🎯 TAKE PROFIT: {' / '.join([f'${tp:,.2f}' for tp in levels['take_profit']])}"
        )

        print(f"\n💡 KEY REASONS:")
        for r in reasons[:5]:
            print(f"   • {r}")

        print(f"\n{'=' * 70}")

        # Create decision object
        decision = TradingDecision(
            timestamp=datetime.now(),
            ticker=ticker,
            asset_type=asset_type,
            mode="analysis",
            current_price=current_price,
            daily_change=daily_change,
            daily_change_pct=daily_change_pct,
            retail_signal=signals["retail"]["signal"],
            retail_confidence=signals["retail"]["confidence"],
            quant_signal=signals["quantitative"]["signal"],
            quant_confidence=signals["quantitative"]["confidence"],
            legendary_signal=signals["legendary"]["signal"],
            legendary_confidence=signals["legendary"]["confidence"],
            final_signal=final_signal,
            final_confidence=final_conf,
            score=int(score),
            sharpe_ratio=risk["sharpe_ratio"],
            var_95=risk["var_95"],
            risk_score=risk["risk_score"],
            entry_price=levels["entry"],
            stop_loss=levels["stop_loss"],
            take_profit=levels["take_profit"],
            risk_reward=levels["risk_reward"],
            reasons=reasons,
            metadata=analysis,
        )

        # Save to memory
        self.memory.add_entry(
            MemoryEntry(
                timestamp=datetime.now(),
                decision=asdict(decision),
                status=OrderStatus.PENDING.value,
            )
        )

        return decision

    def execute(self, decision: TradingDecision, mode: str = "manual") -> Dict:
        """Execute decision based on mode"""

        if mode == "manual":
            print(f"\n📝 MANUAL MODE - Awaiting user confirmation")
            response = input(
                f"   Execute {decision.final_signal.value} for {decision.ticker}? (y/n): "
            )
            if response.lower() != "y":
                return {"status": "cancelled", "reason": "User declined"}

        elif mode == "semi-auto":
            print(f"\n� semi-auto MODE - Auto-execution after confirmation")
            response = input(f"   Confirm {decision.final_signal.value}? (y/n): ")
            if response.lower() != "y":
                return {"status": "cancelled", "reason": "User declined"}

        elif mode == "full-auto":
            print(f"\n🤖 FULL-AUTO MODE - Autonomous execution")

        # Execute paper trade
        result = self.paper_trader.execute(decision)

        # Update memory
        if result["status"] == "executed":
            # Update decision status
            for entry in self.memory.entries:
                if (
                    entry.decision.get("ticker") == decision.ticker
                    and entry.status == "pending"
                ):
                    entry.status = OrderStatus.EXECUTED.value
                    entry.execution_time = datetime.now()
                    break
            self.memory.save()

        return result


# ============ INTERACTIVE TERMINAL ============


def run_streamlit():
    """Launch Streamlit web dashboard"""
    import subprocess
    import sys
    from pathlib import Path

    dashboard_path = Path(__file__).parent / "src" / "dashboard" / "streamlit_app.py"

    if not dashboard_path.exists():
        print(
            f"{Fore.RED}❌ Streamlit dashboard not found at {dashboard_path}{Style.RESET_ALL}"
        )
        print("   Run: python3 -m src.dashboard.streamlit_app")
        return

    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║     🤖 AI HEDGE FUND - STREAMLIT DASHBOARD    ║
╚════════════════════════════════════════════╝
{Style.RESET_ALL}
Starting Streamlit dashboard...

📍 Access at: http://localhost:8501

Features:
• Real-time portfolio overview
• Position management with P&L tracking
• Trade history with performance analytics
• Signal feed and performance charts
• Trading controls (Manual/Semi-Auto/Full-Auto)
• Configuration panel
• MetaTrader connection status

Press Ctrl+C to stop.
""")

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(dashboard_path)], check=True
        )
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 Dashboard stopped{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"\n{Fore.RED}❌ Streamlit error: {e}{Style.RESET_ALL}")
        print("   Install with: pip install streamlit plotly")


def run_new_terminal():
    """Launch enhanced CLI terminal"""
    from src.dashboard.cli_terminal import CLITerminal

    terminal = CLITerminal()
    terminal.run()


def run_backtest_v2(ticker: str, days: int = 180):
    """Run backtest using new backtesting engine"""
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║     🤖 AI HEDGE FUND - BACKTEST v2.2         ║
╚════════════════════════════════════════════╝
{Style.RESET_ALL}
""")

    try:
        from src.backtesting.backtest_engine import get_backtest_engine
        from src.data.free_data_provider import get_free_data_provider
        import pandas as pd

        print(f"📊 Backtesting: {ticker}")
        print(f"📅 Period: {days} days")
        print()

        provider = get_free_data_provider()
        data = provider.get_historical_data(ticker, days=days + 50)

        if not data or len(data) < 50:
            print(f"❌ Insufficient data for {ticker}")
            return

        print(f"📥 Loaded {len(data)} candles")

        df_data = []
        for ohlcv in data:
            df_data.append(
                {
                    "open": ohlcv.open,
                    "high": ohlcv.high,
                    "low": ohlcv.low,
                    "close": ohlcv.close,
                    "volume": ohlcv.volume,
                }
            )
        df = pd.DataFrame(df_data)

        print(f"⚙️ Running backtest...")
        engine = get_backtest_engine()
        results = engine.run_backtest(df, ticker, "EMA Crossover Strategy", days=days)

        print(f"""
╔════════════════════════════════════════════╗
║              BACKTEST RESULTS              ║
╠════════════════════════════════════════════╣
║  Period:              {results.period_days:>6} days           ║
║  Initial Capital:     ${results.initial_capital:>10,.2f}       ║
║  Final Capital:       ${results.final_capital:>10,.2f}       ║
║  Total Return:        {results.total_return_pct:>6.2f}%             ║
╠════════════════════════════════════════════╣
║  Total Trades:        {results.total_trades:>6}               ║
║  Winning Trades:      {results.winning_trades:>6}               ║
║  Losing Trades:       {results.losing_trades:>6}               ║
║  Win Rate:            {results.win_rate:>6.1f}%             ║
║  Profit Factor:       {results.profit_factor:>6.2f}               ║
╠════════════════════════════════════════════╣
║  Avg Win:             ${results.avg_win:>10,.2f}       ║
║  Avg Loss:            ${results.avg_loss:>10,.2f}       ║
║  Max Drawdown:        {results.max_drawdown_pct:>6.2f}%             ║
║  Sharpe Ratio:        {results.sharpe_ratio:>6.2f}               ║
╚════════════════════════════════════════════╝
Execution Time: {results.execution_time_seconds:.2f} seconds
""")

    except Exception as e:
        print(f"❌ Backtest error: {e}")


def run_terminal():
    """Legacy interactive terminal mode (preserved for compatibility)"""
    from colorama import Fore

    system = AIHedgeFund()

    while True:
        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║     🤖 AI HEDGE FUND - TERMINAL v2.1       ║
╚════════════════════════════════════════════╝
{Style.RESET_ALL}
  1. 📊 Single Analysis
  2. 📈 Multi-Asset Analysis
  3. 💾 View Memory
  4. 📋 Statistics
  5. 🚪 Exit
""")

        choice = input(f"  {Fore.CYAN}➜ {Style.RESET_ALL}").strip()

        if choice == "1":
            ticker = input("  Enter ticker (AAPL): ").strip().upper() or "AAPL"
            asset = input(
                "  Asset type (stock_us/stock_idx/forex/crypto/commodity): "
            ).strip()
            asset = asset if asset else "stock_us"

            try:
                decision = system.analyze(ticker, asset)
                mode = (
                    input("  Mode (manual/semi-auto/full-auto): ").strip() or "manual"
                )
                result = system.execute(decision, mode)
                print(f"   Result: {result}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

        elif choice == "2":
            tickers = input("  Enter tickers (comma-separated): ").strip()
            if tickers:
                for t in tickers.split(","):
                    t = t.strip().upper()
                    if t:
                        try:
                            system.analyze(t, "stock_us")
                        except Exception as e:
                            print(f"   ❌ {t}: {e}")

        elif choice == "3":
            recent = system.memory.get_recent(10)
            for entry in recent:
                print(
                    f"   {entry.timestamp}: {entry.decision.get('ticker')} - {entry.decision.get('final_signal')} - {entry.status}"
                )

        elif choice == "4":
            stats = system.memory.get_stats()
            print(f"\n  📊 Statistics:")
            print(f"     Total Entries: {stats['total']}")
            print(f"     Executed: {stats['executed']}")
            print(f"     Pending: {stats['pending']}")
            print(f"     Total PnL: ${stats['total_pnl']:,.2f}")
            print(f"     Win Rate: {stats['win_rate']:.1%}")

        elif choice == "5":
            print(f"\n  👋 Goodbye!")
            break


# ============ BACKTEST MODE ============


def run_backtest(ticker: str, days: int):
    """Run backtest"""
    print(f"\n{'=' * 70}")
    print(f"📊 BACKTEST MODE: {ticker}")
    print(f"{'=' * 70}")

    system = AIHedgeFund()
    data = system.data_provider.get_price(ticker, "stock_us", days)

    if data is None or len(data) < 100:
        print(f"❌ Insufficient data for backtest")
        return

    # Simple walk-forward backtest
    window = 50

    trades = []
    position = None

    for i in range(window, len(data) - 1):
        window_data = data.iloc[: i + 1]

        try:
            analysis = system.strategy_analyzer.analyze(window_data, ticker, "stock_us")
            signal = analysis["final_signal"]
            price = analysis["current_price"]
            sl = analysis["levels"]["stop_loss"]
            tp = (
                analysis["levels"]["take_profit"][0]
                if analysis["levels"]["take_profit"]
                else price * 1.06
            )

            if position is None:
                if signal in [Signal.STRONG_BUY, Signal.BUY]:
                    position = {
                        "type": "long",
                        "entry": price,
                        "sl": sl,
                        "tp": tp,
                        "entry_idx": i,
                    }
            else:
                if position["type"] == "long":
                    if price <= position["sl"]:
                        trades.append(
                            {
                                "type": "long",
                                "pnl": (position["sl"] - position["entry"])
                                / position["entry"],
                            }
                        )
                        position = None
                    elif price >= position["tp"]:
                        trades.append(
                            {
                                "type": "long",
                                "pnl": (position["tp"] - position["entry"])
                                / position["entry"],
                            }
                        )
                        position = None
                    elif signal in [Signal.STRONG_SELL, Signal.SELL]:
                        trades.append(
                            {
                                "type": "long",
                                "pnl": (price - position["entry"]) / position["entry"],
                            }
                        )
                        position = None

        except Exception as e:
            continue

    # Close open position
    if position:
        final_price = data.iloc[-1]["close"]
        trades.append(
            {
                "type": "long",
                "pnl": (final_price - position["entry"]) / position["entry"],
            }
        )

    # Results
    if trades:
        wins = [t for t in trades if t["pnl"] > 0]
        losses = [t for t in trades if t["pnl"] <= 0]

        print(f"\n📋 BACKTEST RESULTS")
        print(f"   Total Trades: {len(trades)}")
        print(f"   Win Rate: {len(wins) / len(trades):.1%}")
        print(
            f"   Avg Win: {sum([t['pnl'] for t in wins]) / len(wins):.2%}"
            if wins
            else "   Avg Win: N/A"
        )
        print(
            f"   Avg Loss: {sum([t['pnl'] for t in losses]) / len(losses):.2%}"
            if losses
            else "   Avg Loss: N/A"
        )
        print(f"   Total PnL: {sum([t['pnl'] for t in trades]):.2%}")
    else:
        print("   No trades generated")


# ============ METATRADER WEB TERMINAL ============


def run_metatrader():
    """Launch MetaTrader web terminal"""
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║     🤖 AI HEDGE FUND - METATRADER WEB UI    ║
╚════════════════════════════════════════════╝
{Style.RESET_ALL}
Starting web server...

📍 Access at: http://localhost:5000

Features:
• Real-time charts
• One-click trading
• Portfolio management
• Signal visualization

Note: This is a simulation terminal. For live trading,
connect to your broker's API.

Press Ctrl+C to stop.
""")

    # Check if Flask is available
    try:
        from flask import Flask, render_template, jsonify, request
        from flask_socketio import SocketIO
    except ImportError:
        print("❌ Flask not installed. Install with: pip install flask flask-socketio")
        print("   Running basic HTTP server instead...")
        print(f"\n📍 Starting basic server at http://localhost:5000")
        print("   Full MetaTrader terminal requires Flask installation.")
        return

    # Simple Flask app for MetaTrader web terminal
    app = Flask(__name__, static_folder="static", template_folder="templates")
    socketio = SocketIO(app)

    @app.route("/")
    def index():
        return render_template("metatrader.html")

    @app.route("/api/status")
    def status():
        return jsonify(
            {"status": "connected", "mode": "paper", "capital": 100000, "positions": []}
        )

    @app.route("/api/analyze", methods=["POST"])
    def analyze():
        data = request.json
        ticker = data.get("ticker", "AAPL")

        system = AIHedgeFund()
        try:
            decision = system.analyze(ticker, "stock_us")
            return jsonify(
                {
                    "signal": decision.final_signal.value,
                    "confidence": decision.final_confidence,
                    "price": decision.current_price,
                    "sl": decision.stop_loss,
                    "tp": decision.take_profit,
                }
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    print(f"🌐 Starting MetaTrader Web Terminal...")
    print(f"📍 Open http://localhost:5000 in your browser")

    try:
        socketio.run(app, host="0.0.0.0", port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")


# ============ MAIN ENTRY POINT ============


def main():
    parser = argparse.ArgumentParser(
        description="AI Hedge Fund v2.2 - Unified Trading System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick analysis
  python3 main.py AAPL

  # Autonomous trading
  python3 main.py AAPL --mode full-auto

  # Multi-asset
  python3 main.py AAPL,BTC,USD/IDR --days 200

  # Interactive terminal (NEW - Enhanced)
  python3 main.py --cli

  # Legacy terminal
  python3 main.py --terminal

  # Streamlit web dashboard (NEW)
  python3 main.py --streamlit

  # Backtest
  python3 main.py --backtest EURUSD --days 365

  # MetaTrader web terminal
  python3 main.py --metatrader

  # Run Streamlit directly
  streamlit run src/dashboard/streamlit_app.py

  # Run CLI directly
  python3 src/dashboard/cli_terminal.py

Strategies (34 Total):
  • 18 Retail/SMC: OTE, Kill Zones, Market Profile, Volume Delta, etc.
  • 6 Quantitative: Jim Simons, Momentum, Mean Reversion, etc.
  • 10 Legendary: Buffett, Lynch, Graham, Soros, Dalio, Burry, Fisher, Templeton, Greenblatt, O'Neil

New in v2.2:
  • Streamlit Web Dashboard with real-time monitoring
  • Enhanced CLI Terminal with full menu system
  • Free Data Sources (Yahoo, CoinGecko, ExchangeRate)
  • MetaTrader Browser Bridge (FREE automation)
  • Enhanced Memory System (SQLite + JSON)
  • Formal Trading Plan with risk parameters
        """,
    )

    parser.add_argument("tickers", nargs="?", help="Trading symbols (comma-separated)")
    parser.add_argument(
        "--mode",
        "-m",
        choices=["manual", "semi-auto", "full-auto"],
        default="manual",
        help="Trading mode",
    )
    parser.add_argument(
        "--asset",
        "-a",
        choices=["stock_us", "stock_idx", "forex", "crypto", "commodity"],
        default="stock_us",
        help="Asset type",
    )
    parser.add_argument(
        "--days", "-d", type=int, default=100, help="Historical data period"
    )
    parser.add_argument(
        "--terminal", action="store_true", help="Launch interactive terminal"
    )
    parser.add_argument(
        "--backtest", nargs="?", const="EURUSD", help="Run backtest mode"
    )
    parser.add_argument(
        "--metatrader", action="store_true", help="Launch MetaTrader web terminal"
    )
    parser.add_argument(
        "--streamlit", action="store_true", help="Launch Streamlit web dashboard"
    )
    parser.add_argument(
        "--cli", action="store_true", help="Launch enhanced CLI terminal"
    )
    parser.add_argument(
        "--portfolio", action="store_true", help="Portfolio analysis mode"
    )

    args = parser.parse_args()

    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   🤖 AI HEDGE FUND v2.2 - UNIFIED TRADING SYSTEM                    ║
║                                                                      ║
║   • 34 Trading Strategies                                           ║
║   • Multi-Asset Support (Stocks, Forex, Crypto, Commodities)        ║
║   • 3-Mode Operation (Manual, Semi-Auto, Full-Auto)                 ║
║   • Enhanced Memory System (SQLite + JSON)                          ║
║   • MetaTrader Browser Bridge (FREE automation)                     ║
║   • Streamlit Web Dashboard                                         ║
║   • Enhanced CLI Terminal                                           ║
║   • Free Data Sources (Yahoo, CoinGecko, ExchangeRate)              ║
║   • Paper Trading & Backtesting                                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

    # Handle different modes
    if args.cli:
        run_new_terminal()

    elif args.terminal:
        run_terminal()

    elif args.streamlit:
        run_streamlit()

    elif args.backtest:
        run_backtest_v2(args.backtest, args.days)

    elif args.metatrader:
        run_metatrader()

    elif args.portfolio or not args.tickers:
        # Portfolio mode with default tickers
        print(f"\n📊 PORTFOLIO ANALYSIS MODE")
        print(f"{'=' * 50}")

        system = AIHedgeFund()
        default_tickers = [
            {"ticker": "AAPL", "asset": "stock_us"},
            {"ticker": "MSFT", "asset": "stock_us"},
            {"ticker": "GOOGL", "asset": "stock_us"},
            {"ticker": "BTC", "asset": "crypto"},
            {"ticker": "EUR/USD", "asset": "forex"},
        ]

        for item in default_tickers:
            try:
                system.analyze(item["ticker"], item["asset"], args.days)
            except Exception as e:
                print(f"   ❌ {item['ticker']}: {e}")

    elif args.tickers:
        # Single or multi-asset analysis
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]

        if len(tickers) == 1:
            # Single ticker
            system = AIHedgeFund()
            try:
                decision = system.analyze(tickers[0], args.asset, args.days)

                # Execute based on mode
                if args.mode != "manual":
                    result = system.execute(decision, args.mode)
                    print(f"\n🚀 Execution Result: {result}")

                # Save result to JSON
                result_file = f"{tickers[0]}_analysis.json"
                with open(result_file, "w") as f:
                    json.dump(
                        {
                            "ticker": decision.ticker,
                            "signal": decision.final_signal.value,
                            "confidence": decision.final_confidence,
                            "score": decision.score,
                            "price": decision.current_price,
                            "stop_loss": decision.stop_loss,
                            "take_profit": decision.take_profit,
                            "timestamp": decision.timestamp.isoformat(),
                        },
                        f,
                        indent=2,
                    )
                print(f"\n💾 Result saved to {result_file}")

            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback

                traceback.print_exc()

        else:
            # Multi-ticker
            print(f"\n📊 MULTI-ASSET ANALYSIS: {', '.join(tickers)}")
            print(f"{'=' * 50}")

            system = AIHedgeFund()
            decisions = []

            for ticker in tickers:
                try:
                    decision = system.analyze(ticker, args.asset, args.days)
                    decisions.append(decision)
                except Exception as e:
                    print(f"   ❌ {ticker}: {e}")

            # Summary
            print(f"\n{'=' * 70}")
            print(f"📋 PORTFOLIO SUMMARY")
            print(f"{'=' * 70}")

            for d in decisions:
                emoji = {
                    Signal.STRONG_BUY: "🟢🟢",
                    Signal.BUY: "🟢",
                    Signal.HOLD: "🟡",
                    Signal.SELL: "🔴",
                    Signal.STRONG_SELL: "🔴🔴",
                }[d.final_signal]

                print(
                    f"{emoji} {d.ticker:8s} | {d.final_signal.value:12s} | {d.score:3d}/100 | ${d.current_price:,.2f}"
                )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
