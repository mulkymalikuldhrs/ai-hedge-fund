# AI HEDGE FUND - FEATURES ANALYSIS
## Extracting Best Features from Freqtrade & Zenbot

## 📊 Source Analysis

### Freqtrade (Python)
- Location: `/home/mulky/freqtrade`
- Type: Crypto trading bot
- Key Strengths: Backtesting, Hyperopt, FreqAI (ML)

### Zenbot (Node.js)  
- Location: `/home/mulky/zenbot-4.1.4`
- Type: Crypto trading bot
- Key Strengths: 20+ strategies, indicator library, extensible

---

## 🎯 Features to Integrate

### 1. Technical Indicators Library

#### From Zenbot (39 indicators)
| Indicator | File | Use Case |
|-----------|------|----------|
| RSI | `lib/rsi.js` | Overbought/oversold |
| MACD | `lib/ta_macd.js` | Trend momentum |
| Bollinger Bands | `lib/bollinger.js` | Volatility |
| EMA/SMA | `lib/ema.js`, `lib/sma.js` | Moving averages |
| Stochastic | `lib/slow_stochastic.js` | Momentum |
| Stochastic RSI | `lib/srsi.js` | Combined signal |
| CCI | `lib/cci.js` | Commodity channel |
| ADX | `lib/adx.js` | Trend strength |
| Keltner Channel | `lib/kc.js` | Volatility bands |
| ATR | `lib/highest.js`, `lib/lowest.js` | Volatility |
| VWAP | `lib/vwap.js` | Volume-weighted |
| Ichimoku | `extensions/strategies/ichimoku/` | Multi-timeframe |
| Williams %R | `lib/ta_willr.js` | Momentum |
| Ultimate Oscillator | `lib/ta_ultosc.js` | Multi-timeframe |
| PPO | `lib/ta_ppo.js` | Momentum |
| TRIX | `lib/ta_trix.js` | Trend |
| Volume Indicators | `lib/ta_volume.js`, `lib/cmf.js` | Volume |
| CMO, MFI, ROC | Various | Momentum |

#### Implementation Plan
```python
# src/indicators/technical_indicators.py

import pandas as pd
import numpy as np

class TechnicalIndicators:
    """Comprehensive technical indicators library"""
    
    @staticmethod
    def sma(prices: pd.Series, period: int) -> pd.Series:
        return prices.rolling(window=period).mean()
    
    @staticmethod
    def ema(prices: pd.Series, period: int) -> pd.Series:
        return prices.ewm(span=period).mean()
    
    @staticmethod
    def rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    @staticmethod
    def bollinger_bands(prices: pd.Series, period: int = 20, std: int = 2):
        sma = prices.rolling(window=period).mean()
        std_dev = prices.rolling(window=period).std()
        upper = sma + (std_dev * std)
        lower = sma - (std_dev * std)
        return upper, sma, lower
    
    @staticmethod
    def stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
                   k_period: int = 14, d_period: int = 3):
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        k = 100 * (close - lowest_low) / (highest_high - lowest_low)
        d = k.rolling(window=d_period).mean()
        return k, d
    
    @staticmethod
    def stochastic_rsi(prices: pd.Series, period: int = 14, k_period: int = 3, d_period: int = 3):
        rsi_vals = TechnicalIndicators.rsi(prices, period)
        lowest = rsi_vals.rolling(window=period).min()
        highest = rsi_vals.rolling(window=period).max()
        k = 100 * (rsi_vals - lowest) / (highest - lowest)
        d = k.rolling(window=d_period).mean()
        return k, d
    
    @staticmethod
    def cci(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 20):
        typical_price = (high + low + close) / 3
        sma = typical_price.rolling(window=period).mean()
        mean_deviation = typical_price.rolling(window=period).apply(
            lambda x: np.mean(np.abs(x - x.mean())), raw=True
        )
        return (typical_price - sma) / (0.015 * mean_deviation)
    
    @staticmethod
    def adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14):
        plus_dm = high.diff()
        minus_dm = -low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        
        tr = pd.concat([
            high - low,
            abs(high - close.shift(1)),
            abs(low - close.shift(1))
        ], axis=1).max(axis=1)
        
        atr = tr.rolling(window=period).mean()
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()
        return plus_di, minus_di, adx
    
    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14):
        tr = pd.concat([
            high - low,
            abs(high - close.shift(1)),
            abs(low - close.shift(1))
        ], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()
    
    @staticmethod
    def vwap(high: pd.Series, low: pd.Series, close: pd.Series, 
             volume: pd.Series, period: int = 14):
        typical_price = (high + low + close) / 3
        cumulative_tp = (typical_price * volume).rolling(window=period).sum()
        cumulative_vol = volume.rolling(window=period).sum()
        return cumulative_tp / cumulative_vol
    
    @staticmethod
    def ichimoku(high: pd.Series, low: pd.Series, periods: dict = None):
        if periods is None:
            periods = {'tenkan': 9, 'kijun': 26, 'senkou': 52}
        
        tenkan = (high.rolling(window=periods['tenkan']).max() + 
                  low.rolling(window=periods['tenkan']).min()) / 2
        kijun = (high.rolling(window=periods['kijun']).max() + 
                 low.rolling(window=periods['kijun']).min()) / 2
        senkou_a = ((tenkan + kijun) / 2).shift(periods['kijun'])
        senkou_b = ((high.rolling(window=periods['senkou']).max() + 
                     low.rolling(window=periods['senkou']).min()) / 2).shift(periods['kijun'])
        chikou = close.shift(-periods['kijun'])
        
        return tenkan, kijun, senkou_a, senkou_b, chikou
    
    @staticmethod
    def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
        obv = [0]
        for i in range(1, len(close)):
            if close.iloc[i] > close.iloc[i-1]:
                obv.append(obv[-1] + volume.iloc[i])
            elif close.iloc[i] < close.iloc[i-1]:
                obv.append(obv[-1] - volume.iloc[i])
            else:
                obv.append(obv[-1])
        return pd.Series(obv, index=close.index)
    
    @staticmethod
    def williams_r(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14):
        highest_high = high.rolling(window=period).max()
        lowest_low = low.rolling(window=period).min()
        return -100 * (highest_high - close) / (highest_high - lowest_low)
    
    @staticmethod
    def ultimate_oscillator(high: pd.Series, low: pd.Series, close: pd.Series,
                            short: int = 7, medium: int = 14, long: int = 28):
        bp = close - pd.Series([min(low.iloc[i], close.iloc[i-1]) if i > 0 else low.iloc[0] 
                                for i in range(len(close))])
        tr = pd.concat([
            high - low,
            abs(high - close.shift(1)),
            abs(low - close.shift(1))
        ], axis=1).max(axis=1)
        
        avg7 = bp.rolling(window=short).sum() / tr.rolling(window=short).sum()
        avg14 = bp.rolling(window=medium).sum() / tr.rolling(window=medium).sum()
        avg28 = bp.rolling(window=long).sum() / tr.rolling(window=long).sum()
        
        return 100 * (4 * avg7 + 2 * avg14 + avg28) / 7
```

---

### 2. Backtesting System

#### From Freqtrade
| Feature | Description |
|---------|-------------|
| `backtesting.py` | Full backtesting engine (77KB!) |
| Hyperopt | Parameter optimization |
| Backtest caching | Speed up repeated tests |
| Strategy analysis | Entry/exit analysis |

#### Implementation Plan
```python
# src/backtesting/backtest_engine.py

class BacktestEngine:
    """Freqtrade-inspired backtesting engine"""
    
    def __init__(self, initial_capital: float = 10000):
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.metrics = {}
    
    def run_backtest(self, strategy, data: pd.DataFrame, 
                     fee: float = 0.001, verbose: bool = False):
        """
        Run backtest on historical data
        
        Args:
            strategy: Strategy object with entry/exit signals
            data: OHLCV dataframe
            fee: Trading fee (0.1% default)
            verbose: Print progress
        """
        # Generate signals
        signals = strategy.generate_signals(data)
        
        # Simulate trading
        for i, (date, row) in enumerate(data.iterrows()):
            signal = signals.iloc[i]
            price = row['close']
            
            if signal == 'BUY' and not self.in_position(row['ticker']):
                self.enter_position(row['ticker'], price, fee)
            elif signal == 'SELL' and self.in_position(row['ticker']):
                self.exit_position(row['ticker'], price, fee)
        
        return self.calculate_metrics()
    
    def calculate_metrics(self) -> dict:
        """Calculate backtest metrics"""
        returns = self.get_returns()
        
        return {
            'total_return': self.get_total_return(),
            'sharpe_ratio': self.get_sharpe_ratio(returns),
            'sortino_ratio': self.get_sortino_ratio(returns),
            'max_drawdown': self.get_max_drawdown(),
            'win_rate': self.get_win_rate(),
            'profit_factor': self.get_profit_factor(),
            'avg_trade': self.get_avg_trade(),
            'num_trades': len(self.trades),
            'calmar_ratio': self.get_calmar_ratio()
        }
```

---

### 3. Hyperparameter Optimization

#### From Freqtrade (Hyperopt)
| Parameter Type | Description |
|---------------|-------------|
| Buy/Sell Spaces | Strategy parameters |
| Protection Spaces | Stop loss, ROI |
| Trailing Spaces | Trailing stop parameters |

#### Implementation Plan
```python
# src/optimization/hyperopt.py

from scipy.optimize import minimize
from dataclasses import dataclass
from typing import Callable
import random

@dataclass
class HyperoptSpace:
    """Parameter search space definition"""
    name: str
    low: float
    high: float
    step: float = 0.01
    type: str = "float"  # float, int, categorical

class Hyperopt:
    """Hyperparameter optimizer"""
    
    def __init__(self, objective: Callable, spaces: list):
        self.objective = objective
        self.spaces = spaces
    
    def optimize(self, n_trials: int = 100, method: str = "random") -> dict:
        """
        Run hyperparameter optimization
        
        Args:
            n_trials: Number of trials
            method: "random", "grid", or "bayesian"
        """
        best_result = None
        best_score = float('-inf')
        
        for i in range(n_trials):
            # Generate trial parameters
            params = self._sample_params()
            
            # Evaluate
            score = self.objective(params)
            
            if score > best_score:
                best_score = score
                best_result = params
        
        return {
            'best_params': best_result,
            'best_score': best_score,
            'n_trials': n_trials
        }
    
    def _sample_params(self) -> dict:
        """Sample parameters from search space"""
        return {
            space.name: random.uniform(space.low, space.high)
            for space in self.spaces
        }
```

---

### 4. Trade Execution

#### From Freqtrade & Zenbot
| Feature | Freqtrade | Zenbot |
|---------|-----------|--------|
| Market orders | ✅ | ✅ |
| Limit orders | ✅ | ✅ |
| Stop loss | ✅ | ✅ |
| Take profit | ✅ | ✅ |
| Trailing stop | ✅ | ✅ |
| ROI (return on investment) | ✅ | - |

#### Implementation Plan
```python
# src/execution/trade_executor.py

from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"

class TrailingType(Enum):
    PERCENT = "percent"
    ABSOLUTE = "absolute"

@dataclass
class TradeConfig:
    """Trade configuration"""
    entry_type: OrderType
    exit_type: OrderType
    stop_loss_pct: float = None
    stop_loss_abs: float = None
    take_profit_pct: float = None
    trailing_stop: bool = False
    trailing_stop_pct: float = None
    roi_target_pct: float = None
    roi_time: int = None  # minutes

class TradeExecutor:
    """Execute trades with proper risk management"""
    
    def __init__(self, config: TradeConfig, fee: float = 0.001):
        self.config = config
        self.fee = fee
    
    def calculate_position_size(self, capital: float, price: float, 
                                 risk_pct: float = 0.02) -> float:
        """Calculate position size based on risk"""
        risk_amount = capital * risk_pct
        return risk_amount / price
    
    def execute_entry(self, ticker: str, price: float, quantity: float,
                      order_type: OrderType = OrderType.MARKET):
        """Execute entry trade"""
        cost = price * quantity
        fee_amount = cost * self.fee
        net_quantity = quantity - (quantity * self.fee)
        
        return {
            'ticker': ticker,
            'side': 'LONG',
            'entry_price': price,
            'quantity': net_quantity,
            'entry_fee': fee_amount,
            'timestamp': datetime.now()
        }
    
    def calculate_stop_loss(self, entry_price: float, direction: str,
                            stop_pct: float = 0.02) -> float:
        """Calculate stop loss price"""
        if direction == 'LONG':
            return entry_price * (1 - stop_pct)
        else:
            return entry_price * (1 + stop_pct)
    
    def calculate_trailing_stop(self, entry_price: float, current_price: float,
                                 high_water_mark: float, direction: str,
                                 trailing_pct: float = 0.02) -> float:
        """Calculate trailing stop price"""
        if direction == 'LONG':
            new_high = max(high_water_mark, current_price)
            return new_high * (1 - trailing_pct)
        else:
            new_low = min(high_water_mark, current_price)
            return new_low * (1 + trailing_pct)
```

---

### 5. Strategy Templates

#### From Zenbot (Ready-to-use strategies)
| Strategy | Indicators | Description |
|----------|------------|-------------|
| `macd` | MACD, RSI | Crossover strategy |
| `rsi` | RSI | Overbought/oversold |
| `bollinger` | Bollinger Bands | Mean reversion |
| `cci_srsi` | CCI + Stochastic RSI | Combined |
| `ichimoku` | Ichimoku Cloud | Multi-timeframe |
| `momentum` | Momentum | Trend following |
| `dema` | Double EMA | Fast/slow crossover |
| `neural` | Neural network | ML-based |

#### Implementation Plan
```python
# src/strategies/template.py

from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd

class StrategyTemplate(ABC):
    """Base strategy template (inspired by Zenbot)"""
    
    name = "base_strategy"
    description = "Base strategy template"
    
    def __init__(self, params: Dict = None):
        self.params = params or self.get_default_params()
        self.validate_params()
    
    @abstractmethod
    def get_default_params(self) -> Dict:
        """Return default parameters"""
        pass
    
    @abstractmethod
    def validate_params(self):
        """Validate parameters are within bounds"""
        pass
    
    @abstractmethod
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add indicators to dataframe"""
        pass
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate BUY/SELL/HOLD signals"""
        pass
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Full strategy analysis"""
        df = data.copy()
        df = self.calculate_indicators(df)
        signals = self.generate_signals(df)
        
        return {
            'signals': signals,
            'data': df,
            'params': self.params
        }


# Example: MACD Strategy
class MACDStrategy(StrategyTemplate):
    """MACD Crossover Strategy (from Zenbot)"""
    
    name = "macd"
    description = "Buy when MACD crosses above signal, sell when below"
    
    def get_default_params(self) -> Dict:
        return {
            'ema_short_period': 12,
            'ema_long_period': 26,
            'signal_period': 9,
            'up_trend_threshold': 0,
            'down_trend_threshold': 0,
            'overbought_rsi_periods': 25,
            'overbought_rsi': 70
        }
    
    def validate_params(self):
        assert 1 <= self.params['ema_short_period'] <= 20
        assert 20 <= self.params['ema_long_period'] <= 100
        assert 1 <= self.params['signal_period'] <= 20
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        from src.indicators.technical_indicators import TechnicalIndicators
        
        close = data['close']
        
        # Calculate MACD
        macd, signal, histogram = TechnicalIndicators.macd(
            close, 
            self.params['ema_short_period'],
            self.params['ema_long_period'],
            self.params['signal_period']
        )
        data['macd'] = macd
        data['macd_signal'] = signal
        data['macd_histogram'] = histogram
        
        # Calculate RSI
        data['rsi'] = TechnicalIndicators.rsi(
            close, 
            self.params['overbought_rsi_periods']
        )
        
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        signals = []
        
        for i in range(len(data)):
            if i == 0:
                signals.append('HOLD')
                continue
            
            curr_hist = data['macd_histogram'].iloc[i]
            prev_hist = data['macd_histogram'].iloc[i-1]
            rsi = data['rsi'].iloc[i]
            
            # Check overbought
            if rsi >= self.params['overbought_rsi']:
                signals.append('SELL')
                continue
            
            # MACD crossover
            if curr_hist > self.params['up_trend_threshold'] and prev_hist <= self.params['up_trend_threshold']:
                signals.append('BUY')
            elif curr_hist < -self.params['down_trend_threshold'] and prev_hist >= -self.params['down_trend_threshold']:
                signals.append('SELL')
            else:
                signals.append('HOLD')
        
        return pd.Series(signals, index=data.index)
```

---

### 6. Configuration System

#### From Freqtrade (config.json)
```json
{
  "strategy": "DefaultStrategy",
  "max_position_adjustments": 1,
  "internals": {
    "process_throttle_secs": 5,
    "interval": 60
  },
  "telegram": {
    "enabled": true,
    "token": "YOUR_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  },
  "api_server": {
    "enabled": true,
    "listen_ip": "0.0.0.0",
    "listen_port": 8080
  }
}
```

---

### 7. Performance Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| Sharpe Ratio | (Return - RiskFree) / StdDev | Risk-adjusted return |
| Sortino Ratio | (Return - RiskFree) / DownsideStdDev | Downside risk |
| Calmar Ratio | Annual Return / Max Drawdown | Drawdown risk |
| Profit Factor | Gross Profit / Gross Loss | Win/Loss ratio |
| Win Rate | Winning Trades / Total Trades | Success rate |
| Avg Trade | Total P&L / Num Trades | Average profit |

---

## 📋 Integration Priority

### High Priority (v1.2.0)
1. ✅ Technical indicators library (30+ indicators)
2. ✅ Backtesting engine
3. ✅ Performance metrics

### Medium Priority (v1.3.0)
4. Strategy templates (MACD, RSI, Bollinger)
5. Trade executor with stop loss/take profit
6. Configuration management

### Low Priority (v1.4.0+)
7. Hyperparameter optimization
8. Paper trading simulation
9. Web dashboard integration

---

## 📁 Files to Create

| File | Purpose | Priority |
|------|---------|----------|
| `src/indicators/__init__.py` | Indicators package | High |
| `src/indicators/technical_indicators.py` | 30+ indicators | High |
| `src/backtesting/backtest_engine.py` | Backtesting | High |
| `src/backtesting/metrics.py` | Performance metrics | High |
| `src/strategies/templates.py` | Strategy templates | Medium |
| `src/execution/trade_executor.py` | Trade execution | Medium |
| `src/optimization/hyperopt.py` | Hyperparameter opt | Low |
| `src/config/manager.py` | Configuration | Low |

---

## 🔗 References

### Freqtrade
- Source: `/home/mulky/freqtrade`
- Key files: `backtesting.py`, `optimize/`, `strategy/`
- License: MIT

### Zenbot
- Source: `/home/mulky/zenbot-4.1.4`
- Key files: `lib/*.js`, `extensions/strategies/`
- License: AGPL-3.0

---

**Analysis Date**: 2026-01-14  
**Status**: Feature extraction complete
**Next Step**: Implementation in `src/indicators/`
