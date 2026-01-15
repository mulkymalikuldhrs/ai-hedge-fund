# AI Quant Hedge Fund - Development Plan v2.0

## Vision Statement

Build a **Full AI-Driven, Multi-Agent Quant Hedge Fund System** that combines:
- **34+ Trading Strategies** (18 Retail/SMC + 6 Quantitative + 10 Legendary Investors)
- **Comprehensive Backtesting Engine** (per-asset, per-strategy, per-timeframe)
- **In-Memory Statistics System** (all interactions stored for analysis)
- **Multi-Agent Architecture** (Data, Analyst, Strategist, Risk, Trader, Sentiment agents)
- **Production-Ready Infrastructure** (paper trading, live trading, monitoring)

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Backtesting System](#2-backtesting-system)
3. [In-Memory Statistics System](#3-in-memory-statistics-system)
4. [Multi-Agent Framework](#4-multi-agent-framework)
5. [Data Management](#5-data-management)
6. [Feature Integration from Reference Projects](#6-feature-integration-from-reference-projects)
7. [Development Roadmap](#7-development-roadmap)
8. [File Structure](#8-file-structure)
9. [API Design](#9-api-design)
10. [Research & References](#10-research--references)

---

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AI QUANT HEDGE FUND SYSTEM v2.0                      │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 1: PRESENTATION                                                  │
│  ├── CLI Interface (terminal.py)                                        │
│  ├── Web Dashboard (Streamlit/React)                                    │
│  └── Telegram Bot Integration                                           │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 2: ORCHESTRATION                                                 │
│  ├── Multi-Agent Coordinator                                            │
│  ├── Event Bus (message passing)                                        │
│  └── State Management (memory system)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 3: AGENTS (8 Specialized Agents)                                 │
│  ├── Data Agent      → Market data collection                           │
│  ├── Analyst Agent   → Technical/Fundamental analysis                   │
│  ├── Strategist Agent → Signal generation                               │
│  ├── Risk Agent      → VaR, CVaR, drawdown monitoring                   │
│  ├── Trader Agent    → Order execution                                  │
│  ├── Sentiment Agent → News/Social sentiment                            │
│  ├── ML Agent        → Machine learning predictions                     │
│  └── Portfolio Agent → Portfolio optimization                           │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 4: CORE SERVICES                                                 │
│  ├── Backtesting Engine                                                │
│  ├── In-Memory Statistics System                                        │
│  ├── Strategy Registry                                                 │
│  ├── Data Provider Abstraction                                          │
│  └── Risk Management Framework                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 5: DATA LAYER                                                    │
│  ├── Price Data (OHLCV)                                                 │
│  ├── Strategy Metadata                                                  │
│  ├── Backtest Results                                                   │
│  └── System Logs                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Key Components

| Component | Purpose | Status |
|-----------|---------|--------|
| `unified_trading_system.py` | Main trading system | ✅ Working |
| `BacktestEngine` | Backtesting with all strategies | 🔲 To Build |
| `MemorySystem` | In-memory statistics storage | 🔲 To Build |
| `AgentCoordinator` | Multi-agent orchestration | 🔲 To Build |
| `StrategyRegistry` | Strategy management | 🔲 To Build |
| `DataProvider` | Unified data access | ✅ Working |

---

## 2. Backtesting System

### 2.1 Backtest Engine Architecture

```python
# src/backtesting/engine.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import pandas as pd
import numpy as np
from collections import defaultdict

class Timeframe(Enum):
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    DAY_1 = "1d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"

class AssetType(Enum):
    STOCK_US = "stock_us"
    STOCK_IDX = "stock_idx"
    FOREX = "forex"
    CRYPTO = "crypto"
    COMMODITY = "commodity"
    INDEX = "index"
    OPTIONS = "options"
    CRYPTO_PERP = "crypto_perp"

@dataclass
class BacktestConfig:
    """Configuration for backtest run"""
    symbol: str
    asset_type: AssetType
    timeframe: Timeframe
    start_date: datetime
    end_date: datetime
    initial_capital: float = 100000.0
    fee_rate: float = 0.001  # 0.1% trading fee
    slippage: float = 0.0005  # 0.05% slippage
    risk_free_rate: float = 0.02  # 2% annual

@dataclass
class Trade:
    """Single trade record"""
    entry_date: datetime
    exit_date: datetime
    entry_price: float
    exit_price: float
    position_size: float
    direction: str  # "long" or "short"
    strategy: str
    pnl: float
    pnl_pct: float
    fees: float
    slippage_cost: float

@dataclass
class BacktestResult:
    """Complete backtest result for one strategy on one asset"""
    config: BacktestConfig
    strategy_name: str
    
    # Performance Metrics
    total_return: float
    annual_return: float
    volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    max_drawdown_duration: int  # days
    
    # Trading Metrics
    total_trades: int
    win_rate: float
    profit_factor: float
    expectancy: float
    avg_trade_duration: float
    best_trade: float
    worst_trade: float
    
    # Equity
    equity_curve: pd.Series
    trades: List[Trade]
    
    # Time breakdown
    daily_returns: pd.Series
    monthly_returns: pd.Series
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary for storage"""
        return {
            'config': {
                'symbol': self.config.symbol,
                'asset_type': self.config.asset_type.value,
                'timeframe': self.config.timeframe.value,
                'start_date': self.config.start_date.isoformat(),
                'end_date': self.config.end_date.isoformat(),
                'initial_capital': self.config.initial_capital
            },
            'strategy_name': self.strategy_name,
            'metrics': {
                'total_return': self.total_return,
                'annual_return': self.annual_return,
                'sharpe_ratio': self.sharpe_ratio,
                'sortino_ratio': self.sortino_ratio,
                'calmar_ratio': self.calmar_ratio,
                'max_drawdown': self.max_drawdown,
                'win_rate': self.win_rate,
                'profit_factor': self.profit_factor,
                'total_trades': self.total_trades
            }
        }

class BacktestEngine:
    """
    Professional backtesting engine with:
    - Per-asset, per-strategy, per-timeframe analysis
    - In-memory statistics storage
    - Multiple strategy comparison
    - Detailed metrics calculation
    """
    
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.strategies = {}  # Registered strategies
        self.memory = BacktestMemory()  # In-memory storage
        
        # Register built-in strategies
        self._register_builtin_strategies()
    
    def _register_builtin_strategies(self):
        """Register all 34 trading strategies"""
        from src.strategies.unified_retail_strategy import RetailStrategyAnalyzer
        from src.strategies.quantitative_strategies import StrategyOrchestrator
        from src.strategies.legendary_investors import LegendaryConsensus
        
        self.strategies['retail_smc'] = RetailStrategyAnalyzer()
        self.strategies['quantitative'] = StrategyOrchestrator()
        self.strategies['legendary'] = LegendaryConsensus()
    
    def run_backtest(
        self,
        config: BacktestConfig,
        strategy_name: str = "all"
    ) -> Dict[str, BacktestResult]:
        """
        Run backtest for specified configuration
        
        Args:
            config: Backtest configuration
            strategy_name: Strategy to test, or "all" for all strategies
            
        Returns:
            Dict mapping strategy_name -> BacktestResult
        """
        # Fetch historical data
        data = self._fetch_data(config)
        
        # Generate signals for each strategy
        if strategy_name == "all":
            results = {}
            for name, strategy in self.strategies.items():
                result = self._run_single_strategy(config, data, name, strategy)
                results[name] = result
                self.memory.store_result(result)  # Store in memory
            return results
        else:
            strategy = self.strategies[strategy_name]
            result = self._run_single_strategy(config, data, strategy_name, strategy)
            self.memory.store_result(result)
            return {strategy_name: result}
    
    def _run_single_strategy(
        self,
        config: BacktestConfig,
        data: pd.DataFrame,
        strategy_name: str,
        strategy
    ) -> BacktestResult:
        """Run backtest for a single strategy"""
        # Generate signals
        signals = self._generate_signals(strategy, data, config)
        
        # Simulate trading
        equity_curve, trades = self._simulate_trading(
            data, signals, config
        )
        
        # Calculate metrics
        result = self._calculate_metrics(
            config, strategy_name, equity_curve, trades
        )
        
        return result
    
    def _generate_signals(
        self,
        strategy,
        data: pd.DataFrame,
        config: BacktestConfig
    ) -> pd.Series:
        """Generate trading signals from strategy"""
        # Strategy-specific signal generation
        if hasattr(strategy, 'analyze'):
            high = data['high'] if 'high' in data.columns else data['close'] + 0.01
            low = data['low'] if 'low' in data.columns else data['close'] - 0.01
            close = data['close']
            volume = data['volume'] if 'volume' in data.columns else pd.Series(1000000, index=data.index)
            
            result = strategy.analyze(high, low, close, volume)
            return pd.Series(result.direction, index=data.index)
        
        return pd.Series('hold', index=data.index)
    
    def _simulate_trading(
        self,
        data: pd.DataFrame,
        signals: pd.Series,
        config: BacktestConfig
    ) -> tuple:
        """Simulate trading based on signals"""
        cash = config.initial_capital
        position = 0  # 0 = no position, >0 = long, <0 = short
        position_size = 0
        equity = [config.initial_capital]
        trades = []
        
        for i, (date, row) in enumerate(data.iterrows()):
            price = row['close']
            signal = signals.iloc[i] if i < len(signals) else 'hold'
            
            # Calculate fees and slippage
            fee = 0
            slippage_cost = 0
            
            # Entry logic
            if position == 0 and signal in ['buy', 'BUY', 'long']:
                position_size = cash * 0.95 / price  # 5% cash reserve
                cost = position_size * price
                fee = cost * config.fee_rate
                slippage_cost = cost * config.slippage
                cash -= cost + fee + slippage_cost
                position = position_size
                entry_price = price
                
            # Exit logic
            elif position > 0 and signal in ['sell', 'SELL', 'short', 'close']:
                revenue = position * price
                fee = revenue * config.fee_rate
                slippage_cost = revenue * config.slippage
                pnl = revenue - cash - position * entry_price - fee - slippage_cost
                cash = revenue - fee - slippage_cost
                
                trades.append(Trade(
                    entry_date=data.index[i-10] if i >= 10 else data.index[0],
                    exit_date=date,
                    entry_price=entry_price,
                    exit_price=price,
                    position_size=position,
                    direction="long",
                    strategy="unknown",
                    pnl=pnl,
                    pnl_pct=pnl / (position * entry_price),
                    fees=fee,
                    slippage_cost=slippage_cost
                ))
                
                position = 0
                position_size = 0
            
            # Update equity
            equity.append(cash + position * price)
        
        return pd.Series(equity, index=data.index[:len(equity)]), trades
    
    def _calculate_metrics(
        self,
        config: BacktestConfig,
        strategy_name: str,
        equity_curve: pd.Series,
        trades: List[Trade]
    ) -> BacktestResult:
        """Calculate all performance metrics"""
        returns = equity_curve.pct_change().dropna()
        
        # Basic metrics
        total_return = (equity_curve.iloc[-1] / config.initial_capital) - 1
        annual_return = total_return / (len(equity_curve) / 252) if len(equity_curve) > 252 else total_return
        volatility = returns.std() * np.sqrt(252)
        
        # Risk metrics
        risk_free_daily = config.risk_free_rate / 252
        excess_returns = returns - risk_free_daily
        sharpe_ratio = (excess_returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
        
        downside_returns = returns[returns < 0]
        sortino_ratio = (excess_returns.mean() / downside_returns.std()) * np.sqrt(252) if len(downside_returns) > 0 and downside_returns.std() > 0 else 0
        
        # Drawdown calculation
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Find max drawdown duration
        dd_periods = (drawdown < 0).astype(int).groupby((drawdown < 0).astype(int).diff().abs().cumsum())
        max_dd_duration = dd_periods.size().max() if len(dd_periods) > 0 else 0
        
        calmar_ratio = abs(annual_return / max_drawdown) if max_drawdown != 0 else 0
        
        # Trading metrics
        total_trades = len(trades)
        if total_trades > 0:
            winning_trades = [t for t in trades if t.pnl > 0]
            losing_trades = [t for t in trades if t.pnl <= 0]
            
            win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
            gross_profit = sum(t.pnl for t in winning_trades)
            gross_loss = abs(sum(t.pnl for t in losing_trades))
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
            
            expectancy = (win_rate * np.mean([t.pnl_pct for t in winning_trades]) - 
                         (1 - win_rate) * np.mean([abs(t.pnl_pct) for t in losing_trades]))
            
            best_trade = max(t.pnl_pct for t in trades) if trades else 0
            worst_trade = min(t.pnl_pct for t in trades) if trades else 0
        else:
            win_rate = 0
            profit_factor = 0
            expectancy = 0
            best_trade = 0
            worst_trade = 0
        
        # Monthly returns
        monthly_returns = equity_curve.resample('M').last().pct_change()
        
        return BacktestResult(
            config=config,
            strategy_name=strategy_name,
            total_return=total_return,
            annual_return=annual_return,
            volatility=volatility,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            max_drawdown=max_drawdown,
            max_drawdown_duration=max_dd_duration,
            total_trades=total_trades,
            win_rate=win_rate,
            profit_factor=profit_factor,
            expectancy=expectancy,
            avg_trade_duration=0,
            best_trade=best_trade,
            worst_trade=worst_trade,
            equity_curve=equity_curve,
            trades=trades,
            daily_returns=returns,
            monthly_returns=monthly_returns
        )
    
    def run_multi_asset_backtest(
        self,
        symbols: List[str],
        asset_types: List[AssetType],
        timeframe: Timeframe,
        start_date: datetime,
        end_date: datetime,
        strategy_name: str = "all"
    ) -> Dict[str, Dict[str, BacktestResult]]:
        """
        Run backtest across multiple assets
        
        Returns:
            Dict[symbol][strategy_name] -> BacktestResult
        """
        results = {}
        
        for symbol, asset_type in zip(symbols, asset_types):
            config = BacktestConfig(
                symbol=symbol,
                asset_type=asset_type,
                timeframe=timeframe,
                start_date=start_date,
                end_date=end_date
            )
            
            symbol_results = self.run_backtest(config, strategy_name)
            results[symbol] = symbol_results
        
        return results
    
    def run_multi_timeframe_backtest(
        self,
        symbol: str,
        asset_type: AssetType,
        timeframes: List[Timeframe],
        start_date: datetime,
        end_date: datetime,
        strategy_name: str = "all"
    ) -> Dict[str, Dict[str, BacktestResult]]:
        """
        Run backtest across multiple timeframes for one asset
        
        Returns:
            Dict[timeframe][strategy_name] -> BacktestResult
        """
        results = {}
        
        for timeframe in timeframes:
            config = BacktestConfig(
                symbol=symbol,
                asset_type=asset_type,
                timeframe=timeframe,
                start_date=start_date,
                end_date=end_date
            )
            
            tf_results = self.run_backtest(config, strategy_name)
            results[timeframe.value] = tf_results
        
        return results
    
    def compare_strategies(
        self,
        symbol: str,
        asset_type: AssetType,
        timeframe: Timeframe,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """
        Compare all strategies for given configuration
        
        Returns:
            DataFrame with strategy comparison
        """
        config = BacktestConfig(
            symbol=symbol,
            asset_type=asset_type,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date
        )
        
        results = self.run_backtest(config, "all")
        
        comparison = []
        for strategy_name, result in results.items():
            comparison.append({
                'Strategy': strategy_name,
                'Total Return': f"{result.total_return:.2%}",
                'Sharpe Ratio': f"{result.sharpe_ratio:.2f}",
                'Max Drawdown': f"{result.max_drawdown:.2%}",
                'Win Rate': f"{result.win_rate:.2%}",
                'Total Trades': result.total_trades,
                'Profit Factor': f"{result.profit_factor:.2f}"
            })
        
        return pd.DataFrame(comparison)
```

### 2.2 Backtest Memory System

```python
# src/backtesting/memory.py

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict
import json

@dataclass
class BacktestSession:
    """Stores all interactions from one backtest session"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    configs: List[Dict] = field(default_factory=list)
    results: List[Dict] = field(default_factory=list)
    logs: List[Dict] = field(default_factory=list)
    
    def add_config(self, config: Dict):
        self.configs.append(config)
    
    def add_result(self, result: Dict):
        self.results.append(result)
    
    def add_log(self, level: str, message: str, details: Dict = None):
        self.logs.append({
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'details': details or {}
        })
    
    def complete(self):
        self.end_time = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'configs': self.configs,
            'results_count': len(self.results),
            'logs_count': len(self.logs)
        }

class BacktestMemory:
    """
    In-memory statistics storage for all backtest interactions
    
    Stores:
    - All backtest results (per-asset, per-strategy, per-timeframe)
    - System logs
    - Session history
    - Aggregated statistics
    """
    
    def __init__(self):
        # Session management
        self.current_session: Optional[BacktestSession] = None
        self.sessions: Dict[str, BacktestSession] = {}
        
        # Results storage
        self.results: Dict[str, List] = defaultdict(list)  # key: "symbol:strategy:tf"
        self.equity_curves: Dict[str, pd.DataFrame] = {}
        self.trades: Dict[str, List] = defaultdict(list)
        
        # Aggregated statistics
        self.best_strategies: Dict[str, Dict] = {}  # per symbol
        self.worst_strategies: Dict[str, Dict] = {}
        self.strategy_rankings: Dict[str, List] = {}
        self.asset_performance: Dict[str, Dict] = {}
        
        # Timeframe analysis
        self.timeframe_performance: Dict[str, Dict] = {}  # tf -> metrics
        
        # Cross-strategy analysis
        self.correlation_matrix: pd.DataFrame = None
        self.strategy_similarities: Dict[str, Dict] = {}
    
    def start_session(self, session_id: str = None) -> str:
        """Start a new backtest session"""
        import uuid
        session_id = session_id or f"session_{uuid.uuid4().hex[:8]}"
        self.current_session = BacktestSession(
            session_id=session_id,
            start_time=datetime.now()
        )
        self.sessions[session_id] = self.current_session
        return session_id
    
    def end_session(self):
        """End current session"""
        if self.current_session:
            self.current_session.complete()
            self.current_session = None
    
    def store_result(self, result: 'BacktestResult'):
        """Store backtest result in memory"""
        key = f"{result.config.symbol}:{result.strategy_name}:{result.config.timeframe.value}"
        self.results[key].append(result)
        
        # Store trades
        self.trades[key].extend(result.trades)
        
        # Update session
        if self.current_session:
            self.current_session.add_result(result.to_dict())
        
        # Update aggregated statistics
        self._update_aggregates(result)
    
    def _update_aggregates(self, result: 'BacktestResult'):
        """Update aggregated statistics"""
        symbol = result.config.symbol
        strategy = result.strategy_name
        
        # Best/worst strategies per symbol
        if symbol not in self.best_strategies:
            self.best_strategies[symbol] = {'strategy': None, 'sharpe': -float('inf')}
            self.worst_strategies[symbol] = {'strategy': None, 'sharpe': float('inf')}
        
        if result.sharpe_ratio > self.best_strategies[symbol]['sharpe']:
            self.best_strategies[symbol] = {
                'strategy': strategy,
                'sharpe': result.sharpe_ratio,
                'return': result.total_return
            }
        
        if result.sharpe_ratio < self.worst_strategies[symbol]['sharpe']:
            self.worst_strategies[symbol] = {
                'strategy': strategy,
                'sharpe': result.sharpe_ratio,
                'return': result.total_return
            }
        
        # Strategy rankings
        if symbol not in self.strategy_rankings:
            self.strategy_rankings[symbol] = []
        
        self.strategy_rankings[symbol].append({
            'strategy': strategy,
            'sharpe': result.sharpe_ratio,
            'return': result.total_return,
            'max_dd': result.max_drawdown
        })
        
        # Sort by Sharpe ratio
        self.strategy_rankings[symbol].sort(
            key=lambda x: x['sharpe'], reverse=True
        )
    
    def get_best_strategy(self, symbol: str) -> Dict:
        """Get best performing strategy for a symbol"""
        return self.best_strategies.get(symbol, {'strategy': None, 'sharpe': 0})
    
    def get_strategy_rankings(self, symbol: str) -> List[Dict]:
        """Get strategy rankings for a symbol"""
        return self.strategy_rankings.get(symbol, [])
    
    def get_asset_summary(self, symbol: str) -> Dict:
        """Get performance summary for an asset"""
        key_prefix = f"{symbol}:"
        symbol_results = {
            k: v for k, v in self.results.items() 
            if k.startswith(key_prefix)
        }
        
        if not symbol_results:
            return {'error': 'No results found'}
        
        returns = []
        sharpes = []
        for results_list in symbol_results.values():
            for r in results_list:
                returns.append(r.total_return)
                sharpes.append(r.sharpe_ratio)
        
        return {
            'symbol': symbol,
            'avg_return': np.mean(returns),
            'avg_sharpe': np.mean(sharpes),
            'strategies_tested': len(symbol_results),
            'best_strategy': self.get_best_strategy(symbol),
            'results_count': sum(len(v) for v in symbol_results.values())
        }
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """Calculate correlation matrix of strategy returns"""
        if not self.results:
            return pd.DataFrame()
        
        # Build returns DataFrame
        returns_df = pd.DataFrame()
        for key, results_list in self.results.items():
            if results_list:
                strategy_name = key.split(':')[1]
                returns_df[strategy_name] = results_list[0].daily_returns
        
        self.correlation_matrix = returns_df.corr()
        return self.correlation_matrix
    
    def export_session(self, session_id: str = None) -> Dict:
        """Export session data for persistence"""
        session = self.sessions.get(session_id) or self.current_session
        if not session:
            return {'error': 'No session found'}
        
        return session.to_dict()
    
    def get_full_report(self) -> Dict:
        """Generate comprehensive report of all stored data"""
        return {
            'timestamp': datetime.now().isoformat(),
            'sessions': {
                sid: s.to_dict() for sid, s in self.sessions.items()
            },
            'results_summary': {
                'total_results': sum(len(v) for v in self.results.values()),
                'symbols_tested': len(set(k.split(':')[0] for k in self.results.keys())),
                'strategies_tested': len(set(k.split(':')[1] for k in self.results.keys()))
            },
            'best_strategies': self.best_strategies,
            'strategy_rankings': self.strategy_rankings,
            'asset_summaries': {
                symbol: self.get_asset_summary(symbol) 
                for symbol in set(k.split(':')[0] for k in self.results.keys())
            }
        }
```

---

## 3. In-Memory Statistics System

### 3.1 Statistics Manager

```python
# src/core/statistics_manager.py

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import json
import pandas as pd
import numpy as np

class MetricType(Enum):
    PERFORMANCE = "performance"
    TRADING = "trading"
    RISK = "risk"
    STRATEGY = "strategy"

@dataclass
class Metric:
    """Individual metric record"""
    name: str
    value: float
    timestamp: datetime
    metadata: Dict = None

class StatisticsManager:
    """
    Central manager for all system statistics
    
    Tracks:
    - Backtest results
    - Trading performance
    - Risk metrics
    - Agent activity
    - System health
    """
    
    def __init__(self):
        # Metrics storage
        self.metrics: Dict[str, List[Metric]] = defaultdict(list)
        
        # Performance tracking
        self.backtest_results: List[Dict] = []
        self.trade_history: List[Dict] = []
        self.portfolio_history: List[Dict] = []
        
        # Agent tracking
        self.agent_activity: Dict[str, List[Dict]] = defaultdict(list)
        
        # System metrics
        self.system_metrics: Dict[str, float] = {}
        
        # Time-series storage for dashboards
        self.timeseries: Dict[str, pd.Series] = {}
    
    def record_metric(self, name: str, value: float, metadata: Dict = None):
        """Record a single metric"""
        self.metrics[name].append(Metric(
            name=name,
            value=value,
            timestamp=datetime.now(),
            metadata=metadata
        ))
    
    def record_backtest(self, result: Dict):
        """Record backtest result"""
        self.backtest_results.append({
            **result,
            'timestamp': datetime.now().isoformat()
        })
        self.record_metric('backtest_count', len(self.backtest_results))
    
    def record_trade(self, trade: Dict):
        """Record executed trade"""
        self.trade_history.append({
            **trade,
            'timestamp': datetime.now().isoformat()
        })
        self.record_metric('trade_count', len(self.trade_history))
    
    def record_agent_activity(self, agent_name: str, activity: Dict):
        """Record agent activity"""
        self.agent_activity[agent_name].append({
            **activity,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_metric_history(self, name: str, limit: int = 100) -> List[Metric]:
        """Get history of a metric"""
        return self.metrics[name][-limit:]
    
    def get_statistics_summary(self) -> Dict:
        """Get summary of all statistics"""
        return {
            'backtest_results': len(self.backtest_results),
            'trade_history': len(self.trade_history),
            'agent_count': len(self.agent_activity),
            'metric_types': len(self.metrics),
            'timestamp': datetime.now().isoformat()
        }
    
    def export_for_dashboard(self) -> Dict:
        """Export data for dashboard visualization"""
        return {
            'backtest_results': self.backtest_results[-100:],  # Last 100
            'trade_history': self.trade_history[-100:],
            'equity_curve': self._build_equity_curve(),
            'metric_summaries': {
                name: {
                    'current': values[-1].value if values else 0,
                    'mean': np.mean([m.value for m in values]) if values else 0,
                    'std': np.std([m.value for m in values]) if values else 0
                }
                for name, values in self.metrics.items()
            }
        }
    
    def _build_equity_curve(self) -> List[Dict]:
        """Build equity curve from trade history"""
        if not self.trade_history:
            return []
        
        equity = 100000  # Starting capital
        curve = []
        
        for trade in self.trade_history:
            equity *= (1 + trade.get('pnl_pct', 0))
            curve.append({
                'timestamp': trade['timestamp'],
                'equity': equity
            })
        
        return curve
```

### 3.2 System Interaction Logger

```python
# src/core/interaction_logger.py

from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass, field
import json
from collections import deque

@dataclass
class Interaction:
    """Single system interaction record"""
    interaction_type: str  # 'backtest', 'trade', 'analysis', 'query'
    actor: str  # 'system', 'user', 'agent'
    action: str
    input_params: Dict = field(default_factory=dict)
    output: Dict = field(default_factory=dict)
    duration_ms: float = 0
    success: bool = True
    error_message: str = None
    timestamp: datetime = field(default_factory=datetime.now)

class InteractionLogger:
    """
    Logger for all system interactions
    
    Stores:
    - User queries and system responses
    - Agent activities and decisions
    - Backtest runs and results
    - Trade executions
    - System errors and warnings
    """
    
    def __init__(self, max_interactions: int = 10000):
        # Interaction history (circular buffer)
        self.interactions: deque = deque(maxlen=max_interactions)
        
        # Aggregated stats
        self.interaction_counts: Dict[str, int] = {}
        self.error_counts: Dict[str, int] = {}
        self.avg_duration: Dict[str, float] = {}
        
        # Per-type storage
        self.backtest_interactions: deque = deque(maxlen=1000)
        self.trade_interactions: deque = deque(maxlen=5000)
        self.query_interactions: deque = deque(maxlen=2000)
        self.agent_interactions: deque = deque(maxlen=5000)
    
    def log(
        self,
        interaction_type: str,
        actor: str,
        action: str,
        input_params: Dict = None,
        output: Dict = None,
        duration_ms: float = 0,
        success: bool = True,
        error_message: str = None
    ):
        """Log a system interaction"""
        interaction = Interaction(
            interaction_type=interaction_type,
            actor=actor,
            action=action,
            input_params=input_params or {},
            output=output or {},
            duration_ms=duration_ms,
            success=success,
            error_message=error_message
        )
        
        self.interactions.append(interaction)
        
        # Update aggregated stats
        self.interaction_counts[interaction_type] = \
            self.interaction_counts.get(interaction_type, 0) + 1
        
        if not success:
            self.error_counts[interaction_type] = \
                self.error_counts.get(interaction_type, 0) + 1
        
        # Track per-type
        if interaction_type == 'backtest':
            self.backtest_interactions.append(interaction)
        elif interaction_type == 'trade':
            self.trade_interactions.append(interaction)
        elif interaction_type == 'query':
            self.query_interactions.append(interaction)
        elif interaction_type == 'agent':
            self.agent_interactions.append(interaction)
    
    def get_recent(self, n: int = 10) -> list:
        """Get recent interactions"""
        return list(self.interactions)[-n:]
    
    def get_summary(self) -> Dict:
        """Get interaction summary"""
        return {
            'total_interactions': len(self.interactions),
            'by_type': dict(self.interaction_counts),
            'errors': dict(self.error_counts),
            'avg_duration': dict(self.avg_duration)
        }
    
    def get_error_log(self) -> list:
        """Get all errors"""
        return [i for i in self.interactions if not i.success]
```

---

## 4. Multi-Agent Framework

### 4.1 Agent Base Class

```python
# src/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

class AgentState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    THINKING = "thinking"
    ERROR = "error"

@dataclass
class AgentMessage:
    """Message between agents"""
    sender: str
    receiver: str
    message_type: str
    content: Dict
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AgentTask:
    """Task assigned to an agent"""
    task_id: str
    task_type: str
    input_data: Dict
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, config: Dict = None):
        self.name = name
        self.config = config or {}
        self.state = AgentState.IDLE
        self.last_activity: Optional[datetime] = None
        self.task_history: List[AgentTask] = []
        self.memory: Dict[str, Any] = {}
        
        # Message handlers
        self.handlers: Dict[str, callable] = {}
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize agent resources"""
        pass
    
    @abstractmethod
    def execute(self, task: AgentTask) -> Dict:
        """Execute a task"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities"""
        pass
    
    def register_handler(self, message_type: str, handler: callable):
        """Register message handler"""
        self.handlers[message_type] = handler
    
    def send_message(self, receiver: str, message_type: str, content: Dict) -> AgentMessage:
        """Send message to another agent"""
        msg = AgentMessage(
            sender=self.name,
            receiver=receiver,
            message_type=message_type,
            content=content
        )
        # Message bus will handle delivery
        return msg
    
    def update_state(self, new_state: AgentState):
        """Update agent state"""
        self.state = new_state
        self.last_activity = datetime.now()
```

### 4.2 Agent Implementations

```python
# src/agents/data_agent.py

from .base_agent import BaseAgent, AgentTask, AgentState
from src.tools.unified_data_provider import UnifiedDataProvider

class DataAgent(BaseAgent):
    """Agent responsible for market data collection"""
    
    def __init__(self, config: Dict = None):
        super().__init__("DataAgent", config)
        self.data_provider = UnifiedDataProvider()
        self.cached_data: Dict[str, Any] = {}
    
    def initialize(self) -> bool:
        """Initialize data provider"""
        try:
            # Test connection
            test_prices = self.data_provider.get_price("AAPL", "stock_us", 10)
            return len(test_prices) > 0
        except Exception as e:
            print(f"DataAgent init failed: {e}")
            return False
    
    def get_capabilities(self) -> List[str]:
        return [
            "fetch_price_data",
            "fetch_historical_data",
            "get_fundamentals",
            "get_market_news",
            "validate_data"
        ]
    
    def execute(self, task: AgentTask) -> Dict:
        """Execute data-related tasks"""
        self.state = AgentState.RUNNING
        
        task_type = task.task_type
        result = {"success": False}
        
        if task_type == "fetch_price_data":
            symbol = task.input_data.get("symbol")
            asset_type = task.input_data.get("asset_type", "stock_us")
            days = task.input_data.get("days", 100)
            
            prices = self.data_provider.get_price(symbol, asset_type, days)
            
            result = {
                "success": True,
                "data": {
                    "symbol": symbol,
                    "prices": [{"date": p.date, "close": p.close} for p in prices],
                    "count": len(prices)
                }
            }
            self.cached_data[f"{symbol}:{asset_type}"] = prices
        
        elif task_type == "get_fundamentals":
            symbol = task.input_data.get("symbol")
            # Extract fundamentals from price data
            if f"{symbol}:stock_us" in self.cached_data:
                prices = self.cached_data[f"{symbol}:stock_us"]
                from src.strategies.legendary_investors import get_fundamentals_from_price
                price_list = [p.close for p in prices]
                result["fundamentals"] = get_fundamentals_from_price(price_list)
                result["success"] = True
        
        self.state = AgentState.IDLE
        return result


# src/agents/analyst_agent.py

from .base_agent import BaseAgent, AgentTask
from src.indicators.technical_indicators import TechnicalIndicators

class AnalystAgent(BaseAgent):
    """Agent for technical and fundamental analysis"""
    
    def __init__(self, config: Dict = None):
        super().__init__("AnalystAgent", config)
        self.indicators = TechnicalIndicators()
    
    def initialize(self) -> bool:
        return True
    
    def get_capabilities(self) -> List[str]:
        return [
            "technical_analysis",
            "fundamental_analysis",
            "calculate_indicators",
            "detect_patterns"
        ]
    
    def execute(self, task: AgentTask) -> Dict:
        """Execute analysis tasks"""
        from src.strategies.unified_retail_strategy import RetailStrategyAnalyzer
        import pandas as pd
        import numpy as np
        
        task_type = task.task_type
        result = {"success": False}
        
        if task_type == "technical_analysis":
            price_data = task.input_data.get("price_data", [])
            
            if not price_data:
                result["error"] = "No price data provided"
                return result
            
            close = pd.Series([p["close"] for p in price_data])
            high = close + 0.01  # Approximate
            low = close - 0.01
            volume = pd.Series([p.get("volume", 1000000) for p in price_data])
            
            # Calculate indicators
            rsi = self.indicators.rsi(close).iloc[-1]
            macd_line, signal, hist = self.indicators.macd(close)
            atr = self.indicators.atr(high, low, close).iloc[-1]
            
            # Run retail strategies
            retail = RetailStrategyAnalyzer()
            retail_result = retail.analyze(high, low, close, volume)
            
            result = {
                "success": True,
                "analysis": {
                    "rsi": rsi,
                    "macd": macd_line.iloc[-1],
                    "atr": atr,
                    "signal": retail_result.direction,
                    "confidence": retail_result.confidence
                }
            }
        
        return result


# src/agents/strategist_agent.py

from .base_agent import BaseAgent, AgentTask

class StrategistAgent(BaseAgent):
    """Agent for signal generation and strategy selection"""
    
    def __init__(self, config: Dict = None):
        super().__init__("StrategistAgent", config)
        self.active_strategies = []
    
    def initialize(self) -> bool:
        return True
    
    def get_capabilities(self) -> List[str]:
        return [
            "generate_signals",
            "combine_signals",
            "select_strategy",
            "optimize_parameters"
        ]
    
    def execute(self, task: AgentTask) -> Dict:
        """Generate trading signals"""
        task_type = task.task_type
        result = {"success": False}
        
        if task_type == "generate_signals":
            analysis_results = task.input_data.get("analysis", {})
            
            # Combine signals from different sources
            signals = {
                "retail": analysis_results.get("signal"),
                "quantitative": task.input_data.get("quant_signal"),
                "legendary": task.input_data.get("legendary_signal")
            }
            
            # Weighted voting
            weights = {
                "retail": 0.25,
                "quantitative": 0.25,
                "legendary": 0.50
            }
            
            # Calculate final signal
            signal_scores = {"BUY": 0, "SELL": 0, "HOLD": 0}
            for source, signal in signals.items():
                if signal:
                    signal_scores[signal] += weights.get(source, 0.33)
            
            final_signal = max(signal_scores, key=signal_scores.get)
            confidence = signal_scores[final_signal]
            
            result = {
                "success": True,
                "signal": final_signal,
                "confidence": confidence,
                "signal_breakdown": signals
            }
        
        return result


# src/agents/risk_agent.py

from .base_agent import BaseAgent, AgentTask
from src.risk.risk_management import RiskManagementFramework, calculate_sharpe_ratio
import pandas as pd

class RiskAgent(BaseAgent):
    """Agent for risk management"""
    
    def __init__(self, config: Dict = None):
        super().__init__("RiskAgent", config)
        self.risk_framework = RiskManagementFramework()
    
    def initialize(self) -> bool:
        return True
    
    def get_capabilities(self) -> List[str]:
        return [
            "calculate_var",
            "calculate_sharpe",
            "check_position_limits",
            "assess_drawdown"
        ]
    
    def execute(self, task: AgentTask) -> Dict:
        """Perform risk assessment"""
        task_type = task.task_type
        result = {"success": False}
        
        if task_type == "assess_risk":
            returns = task.input_data.get("returns", [])
            
            if not returns:
                result["error"] = "No returns data"
                return result
            
            returns_series = pd.Series(returns)
            
            # Calculate risk metrics
            sharpe = calculate_sharpe_ratio(returns_series)
            var_95 = self.risk_framework.calculate_var(
                returns_series, 
                portfolio_value=100000,
                method="historical"
            )
            
            # Calculate max drawdown
            cumulative = (1 + returns_series).cumprod()
            running_max = cumulative.cummax()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min()
            
            # Risk score (0-100)
            risk_score = min(100, max(0, 100 - (var_95 * 100)))
            
            result = {
                "success": True,
                "risk_metrics": {
                    "sharpe_ratio": sharpe,
                    "var_95": var_95,
                    "max_drawdown": max_drawdown,
                    "risk_score": risk_score
                },
                "recommendation": "LOW_RISK" if risk_score > 70 else "MEDIUM_RISK" if risk_score > 40 else "HIGH_RISK"
            }
        
        return result
```

### 4.3 Agent Coordinator

```python
# src/agents/coordinator.py

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from .base_agent import BaseAgent, AgentTask, AgentMessage
from .data_agent import DataAgent
from .analyst_agent import AnalystAgent
from .strategist_agent import StrategistAgent
from .risk_agent import RiskAgent
from ..core.interaction_logger import InteractionLogger

@dataclass
class CoordinatorState:
    """State of the coordinator"""
    agents_registered: int = 0
    tasks_completed: int = 0
    messages_sent: int = 0
    last_coordination: Optional[datetime] = None

class AgentCoordinator:
    """
    Central coordinator for all agents
    
    Responsibilities:
    - Agent registration and lifecycle
    - Task distribution
    - Message routing
    - State management
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.state = CoordinatorState()
        self.logger = InteractionLogger()
        self.task_queue: List[AgentTask] = []
    
    def register_agent(self, agent: BaseAgent) -> bool:
        """Register an agent with the coordinator"""
        if agent.name in self.agents:
            print(f"Agent {agent.name} already registered")
            return False
        
        if not agent.initialize():
            print(f"Failed to initialize agent {agent.name}")
            return False
        
        self.agents[agent.name] = agent
        self.state.agents_registered += 1
        
        self.logger.log(
            interaction_type="agent",
            actor="coordinator",
            action="register_agent",
            input_params={"agent_name": agent.name}
        )
        
        return True
    
    def initialize_all_agents(self) -> bool:
        """Initialize all default agents"""
        # Register default agents
        self.register_agent(DataAgent())
        self.register_agent(AnalystAgent())
        self.register_agent(StrategistAgent())
        self.register_agent(RiskAgent())
        
        return len(self.agents) > 0
    
    def submit_task(self, task: AgentTask):
        """Submit a task for execution"""
        self.task_queue.append(task)
    
    def coordinate(self) -> Dict:
        """
        Main coordination loop
        
        Returns:
            Dict with analysis results
        """
        if not self.task_queue:
            return {"error": "No tasks in queue"}
        
        task = self.task_queue.pop(0)
        self.state.tasks_completed += 1
        self.state.last_coordination = datetime.now()
        
        # Route task to appropriate agent
        task_type = task.task_type
        
        if task_type in ["fetch_price_data", "get_fundamentals"]:
            agent = self.agents.get("DataAgent")
        elif task_type in ["technical_analysis", "fundamental_analysis"]:
            agent = self.agents.get("AnalystAgent")
        elif task_type in ["generate_signals", "select_strategy"]:
            agent = self.agents.get("StrategistAgent")
        elif task_type in ["assess_risk", "check_position_limits"]:
            agent = self.agents.get("RiskAgent")
        else:
            return {"error": f"Unknown task type: {task_type}"}
        
        if not agent:
            return {"error": f"No agent available for task: {task_type}"}
        
        # Execute task
        import time
        start = time.time()
        
        result = agent.execute(task)
        
        duration_ms = (time.time() - start) * 1000
        
        self.logger.log(
            interaction_type="agent",
            actor=agent.name,
            action=task_type,
            input_params=task.input_data,
            output=result,
            duration_ms=duration_ms,
            success=result.get("success", False)
        )
        
        return result
    
    def run_analysis_pipeline(self, symbol: str, asset_type: str = "stock_us") -> Dict:
        """
        Run complete analysis pipeline
        
        1. Data Agent: Fetch price data
        2. Analyst Agent: Technical analysis
        3. Strategist Agent: Generate signals
        4. Risk Agent: Risk assessment
        """
        # Step 1: Get data
        data_task = AgentTask(
            task_id=f"task_{datetime.now().timestamp()}",
            task_type="fetch_price_data",
            input_data={"symbol": symbol, "asset_type": asset_type, "days": 200}
        )
        
        self.submit_task(data_task)
        data_result = self.coordinate()
        
        if not data_result.get("success"):
            return {"error": "Failed to fetch data", "details": data_result}
        
        # Step 2: Analyze
        analysis_task = AgentTask(
            task_id=f"task_{datetime.now().timestamp()}",
            task_type="technical_analysis",
            input_data={"price_data": data_result.get("data", {}).get("prices", [])}
        )
        
        self.submit_task(analysis_task)
        analysis_result = self.coordinate()
        
        # Step 3: Generate signals
        signal_task = AgentTask(
            task_id=f"task_{datetime.now().timestamp()}",
            task_type="generate_signals",
            input_data={"analysis": analysis_result.get("analysis", {})}
        )
        
        self.submit_task(signal_task)
        signal_result = self.coordinate()
        
        # Step 4: Risk assessment
        if analysis_result.get("success"):
            returns = [0.01] * 100  # Placeholder
            risk_task = AgentTask(
                task_id=f"task_{datetime.now().timestamp()}",
                task_type="assess_risk",
                input_data={"returns": returns}
            )
            
            self.submit_task(risk_task)
            risk_result = self.coordinate()
        else:
            risk_result = {"risk_metrics": {}}
        
        # Combine results
        return {
            "success": True,
            "symbol": symbol,
            "data": data_result.get("data", {}),
            "analysis": analysis_result.get("analysis", {}),
            "signal": signal_result,
            "risk": risk_result.get("risk_metrics", {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict:
        """Get coordinator status"""
        return {
            "agents_registered": self.state.agents_registered,
            "tasks_completed": self.state.tasks_completed,
            "agents": list(self.agents.keys()),
            "queue_size": len(self.task_queue)
        }
```

---

## 5. Data Management

### 5.1 Unified Data Provider with Caching

```python
# src/tools/enhanced_data_provider.py

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import numpy as np
from ..tools.unified_data_provider import UnifiedDataProvider, AssetType

class Timeframe(Enum):
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    DAY_1 = "1d"
    WEEK_1 = "1w"

@dataclass
class DataRequest:
    """Data request specification"""
    symbol: str
    asset_type: str
    timeframe: Timeframe
    start_date: datetime
    end_date: datetime
    columns: List[str] = None

class EnhancedDataProvider:
    """
    Enhanced data provider with:
    - Multi-timeframe support
    - Data caching
    - Automatic resampling
    - Quality validation
    """
    
    def __init__(self):
        self.base_provider = UnifiedDataProvider()
        self.cache: Dict[str, pd.DataFrame] = {}
        self.data_freshness: Dict[str, datetime] = {}
    
    def get_data(self, request: DataRequest) -> pd.DataFrame:
        """Get data with requested timeframe"""
        cache_key = f"{request.symbol}:{request.asset_type}:{request.timeframe.value}"
        
        # Check cache
        if cache_key in self.cache:
            df = self.cache[cache_key]
            # Filter by date range
            return self._filter_date_range(df, request.start_date, request.end_date)
        
        # Fetch base data
        base_data = self.base_provider.get_price(
            request.symbol,
            request.asset_type,
            365  # Get 1 year for resampling
        )
        
        if not base_data:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = self._prices_to_dataframe(base_data)
        
        # Resample to requested timeframe
        if request.timeframe != Timeframe.DAY_1:
            df = self._resample(df, request.timeframe)
        
        # Cache
        self.cache[cache_key] = df
        self.data_freshness[cache_key] = datetime.now()
        
        return self._filter_date_range(df, request.start_date, request.end_date)
    
    def _prices_to_dataframe(self, prices: List) -> pd.DataFrame:
        """Convert price list to DataFrame"""
        data = {
            'date': [p.date for p in prices],
            'open': [p.open for p in prices],
            'high': [p.high for p in prices],
            'low': [p.low for p in prices],
            'close': [p.close for p in prices],
            'volume': [p.volume for p in prices]
        }
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df
    
    def _resample(self, df: pd.DataFrame, timeframe: Timeframe) -> pd.DataFrame:
        """Resample data to different timeframe"""
        rule = self._timeframe_to_rule(timeframe)
        
        resampled = pd.DataFrame({
            'open': df['open'].resample(rule).first(),
            'high': df['high'].resample(rule).max(),
            'low': df['low'].resample(rule).min(),
            'close': df['close'].resample(rule).last(),
            'volume': df['volume'].resample(rule).sum()
        })
        
        return resampled.dropna()
    
    def _timeframe_to_rule(self, timeframe: Timeframe) -> str:
        """Convert timeframe enum to pandas rule"""
        mapping = {
            Timeframe.MINUTE_1: '1min',
            Timeframe.MINUTE_5: '5min',
            Timeframe.MINUTE_15: '15min',
            Timeframe.MINUTE_30: '30min',
            Timeframe.HOUR_1: '1H',
            Timeframe.HOUR_4: '4H',
            Timeframe.DAY_1: '1D',
            Timeframe.WEEK_1: '1W'
        }
        return mapping.get(timeframe, '1D')
    
    def _filter_date_range(
        self, 
        df: pd.DataFrame, 
        start: datetime, 
        end: datetime
    ) -> pd.DataFrame:
        """Filter DataFrame by date range"""
        mask = (df.index >= start) & (df.index <= end)
        return df[mask]
```

---

## 6. Feature Integration from Reference Projects

### 6.1 Features from Freqtrade

| Feature | Implementation | Priority |
|---------|---------------|----------|
| Strategy base class | `Strategy` abstract class | HIGH |
| Hyperparameter optimization | `BacktestEngine` + grid search | MEDIUM |
| Dry-run mode | Paper trading simulation | HIGH |
| Telegram integration | Telegram bot | LOW |

### 6.2 Features from Fincept Terminal

| Feature | Implementation | Priority |
|---------|---------------|----------|
| 100+ Data connectors | `EnhancedDataProvider` | MEDIUM |
| CFA-level analytics | `RiskManagementFramework` | HIGH |
| AI investor personas | `LegendaryInvestors` | DONE |
| Visual workflow builder | Streamlit dashboard | LOW |

### 6.3 Features from Quanta AI

| Feature | Implementation | Priority |
|---------|---------------|----------|
| Multi-agent architecture | `AgentCoordinator` | HIGH |
| Memory system | `BacktestMemory` | HIGH |
| Risk management | `RiskAgent` | HIGH |
| Sentiment analysis | Integration point | MEDIUM |

### 6.4 Features from Zenbot

| Feature | Implementation | Priority |
|---------|---------------|----------|
| Genetic algorithm optimizer | Future enhancement | LOW |
| MongoDB persistence | Optional | LOW |
| Visual backtesting | Streamlit charts | MEDIUM |

---

## 7. Development Roadmap

### Phase 1: Core Infrastructure (Week 1-2)

```
✅ Week 1
├── BacktestEngine skeleton
├── BacktestMemory system
├── InteractionLogger
└── EnhancedDataProvider (multi-timeframe)

Week 2
├── DataAgent implementation
├── AnalystAgent implementation
├── StrategistAgent implementation
└── RiskAgent implementation
```

### Phase 2: Integration (Week 3-4)

```
Week 3
├── AgentCoordinator
├── StrategyRegistry
└── Unified backtest pipeline

Week 4
├── CLI interface enhancement
├── Streamlit dashboard
└── Telegram bot integration
```

### Phase 3: Advanced Features (Week 5-6)

```
Week 5
├── ML integration (FreqAI-style)
├── Hyperparameter optimization
└── Walkforward analysis

Week 6
├── Portfolio backtesting
├── Correlation analysis
└── Stress testing
```

### Phase 4: Production (Week 7-8)

```
Week 7
├── Paper trading mode
├── Live trading integration
└── Performance monitoring

Week 8
├── Documentation
├── Testing
└── Deployment
```

---

## 8. File Structure

```
ai-hedge-fund/
├── src/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── coordinator.py
│   │   ├── data_agent.py
│   │   ├── analyst_agent.py
│   │   ├── strategist_agent.py
│   │   ├── risk_agent.py
│   │   ├── trader_agent.py
│   │   ├── sentiment_agent.py
│   │   ├── ml_agent.py
│   │   └── portfolio_agent.py
│   ├── backtesting/
│   │   ├── engine.py
│   │   ├── memory.py
│   │   ├── metrics.py
│   │   └── visualization.py
│   ├── core/
│   │   ├── statistics_manager.py
│   │   ├── interaction_logger.py
│   │   ├── event_bus.py
│   │   └── config.py
│   ├── strategies/
│   │   ├── unified_retail_strategy.py
│   │   ├── quantitative_strategies.py
│   │   ├── legendary_investors.py
│   │   └── strategy_registry.py
│   ├── tools/
│   │   ├── unified_data_provider.py
│   │   ├── enhanced_data_provider.py
│   │   └── data_cache.py
│   └── trading/
│       ├── paper_trading.py
│       ├── live_trading.py
│       └── order_manager.py
├── tests/
│   ├── test_backtesting/
│   ├── test_agents/
│   └── test_integration/
├── scripts/
│   ├── run_backtest.py
│   ├── run_analysis.py
│   └── generate_report.py
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── examples.md
├── unified_trading_system.py
├── backtest_runner.py
├── dashboard.py
└── requirements.txt
```

---

## 9. API Design

### 9.1 Backtest API

```python
# Quick start
from src.backtesting.engine import BacktestEngine, BacktestConfig, Timeframe, AssetType
from datetime import datetime

engine = BacktestEngine()

# Run single backtest
config = BacktestConfig(
    symbol="AAPL",
    asset_type=AssetType.STOCK_US,
    timeframe=Timeframe.DAY_1,
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2024, 1, 1)
)

results = engine.run_backtest(config, "all")

# Compare strategies
comparison = engine.compare_strategies(
    symbol="AAPL",
    asset_type=AssetType.STOCK_US,
    timeframe=Timeframe.DAY_1,
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2024, 1, 1)
)

# Multi-asset backtest
results = engine.run_multi_asset_backtest(
    symbols=["AAPL", "MSFT", "GOOGL"],
    asset_types=[AssetType.STOCK_US] * 3,
    timeframe=Timeframe.DAY_1,
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2024, 1, 1)
)
```

### 9.2 Agent API

```python
from src.agents.coordinator import AgentCoordinator
from src.agents.base_agent import AgentTask

coordinator = AgentCoordinator()
coordinator.initialize_all_agents()

# Run analysis pipeline
result = coordinator.run_analysis_pipeline(
    symbol="AAPL",
    asset_type="stock_us"
)

# Check status
status = coordinator.get_status()
```

### 9.3 Memory API

```python
from src.backtesting.memory import BacktestMemory

memory = BacktestMemory()

# Get best strategy for symbol
best = memory.get_best_strategy("AAPL")

# Get strategy rankings
rankings = memory.get_strategy_rankings("AAPL")

# Get full report
report = memory.get_full_report()

# Export session
session_data = memory.export_session()
```

---

## 10. Research & References

### 10.1 Key Papers & Resources

| Topic | Source | Reference |
|-------|--------|-----------|
| Multi-Agent Systems | Medium | [Building a Multi-Agent AI Trading System](https://medium.com/@ishveen/building-a-multi-agent-ai-trading-system-technical-deep-dive-into-architecture-b5ba216e70f3) |
| Backtesting Framework | GitHub | [Freqtrade Backtesting](https://github.com/freqtrade/freqtrade) |
| ML Trading | GitHub | [PyBroker](https://github.com/edtechre/pybroker) |
| VectorBT | GitHub | [VectorBT](https://github.com/polakowo/vectorbt) |
| Backtesting Best Practices | PapersWithBacktest | [Python Backtesting Considerations](https://paperswithbacktest.org/wiki/backtesting-systematic-trading-strategies-in-python-considerations-and-open-source-frameworks) |

### 10.2 Inspiration from Reference Projects

```
1. Freqtrade (https://github.com/freqtrade/freqtrade)
   - Strategy framework
   - Backtesting system
   - Dry-run mode
   - Telegram integration

2. FinceptTerminal (https://github.com/Fincept-Team/FinceptTerminal)
   - 100+ data connectors
   - CFA analytics
   - AI investor personas
   - Desktop app architecture

3. Quanta AI (https://github.com/quanta-ai/quanta_ai)
   - Multi-agent architecture
   - 6 specialized agents
   - Memory system
   - Risk management

4. Quant Nanggoe AI (https://github.com/Quant-Nanggoe/Quant-Nanggoe-AI)
   - Market regime detection
   - Pressure normalization
   - Darwinian strategy evolution

5. Zenbot (https://github.com/cinar/zenbot)
   - Genetic algorithm optimizer
   - MongoDB persistence
   - Visual backtesting
```

### 10.3 Implementation Patterns

1. **Event-Driven Architecture**
   - Used in Freqtrade, QSTrader
   - Enables real-time processing
   - Decouples components

2. **Memory-Based Agents**
   - Short-term: Current task context
   - Long-term: Strategy performance history
   - Episodic: Trade-by-trade records
   - Semantic: Market knowledge

3. **Strategy Pattern**
   - BaseStrategy abstract class
   - Register strategies at runtime
   - Hot-swap strategies

4. **Timeframe Abstraction**
   - Unified data access
   - Automatic resampling
   - Cross-timeframe analysis

---

## Appendices

### A. Configuration Reference

```python
# config/default_config.yaml

backtesting:
  initial_capital: 100000
  fee_rate: 0.001
  slippage: 0.0005
  risk_free_rate: 0.02

agents:
  data_agent:
    cache_size: 1000
    refresh_interval: 300
  
  risk_agent:
    var_confidence: 0.95
    max_drawdown_limit: 0.20

strategies:
  retail_smc:
    enabled: true
    weight: 0.25
  
  quantitative:
    enabled: true
    weight: 0.25
  
  legendary:
    enabled: true
    weight: 0.50
```

### B. Performance Metrics Reference

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Sharpe Ratio | (Rp - Rf) / σp | Risk-adjusted return |
| Sortino Ratio | (Rp - Rf) / σd | Downside risk only |
| Calmar Ratio | Annual Return / | Max Drawdown |
| Profit Factor | Gross Profit / Gross Loss | Win quality |
| Expectancy | (Win% × AvgWin) - (Loss% × AvgLoss) | Per-trade expected value |

### C. Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| E001 | Invalid symbol | Check symbol exists |
| E002 | Insufficient data | Increase date range |
| E003 | Strategy error | Check strategy config |
| E004 | Data fetch failed | Check API connection |
| E005 | Memory limit | Clear cache |

---

*Document Version: 2.0*
*Last Updated: 2026-01-16*
*Next Review: 2026-01-23*
