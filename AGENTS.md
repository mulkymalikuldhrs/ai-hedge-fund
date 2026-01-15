# AGENTS.md - Codebase Guidelines for AI Agents

## Current Development State (2026-01-16)

### 🎯 Phase 2: AI Quant Hedge Fund v2.0

This session we are planning the next major version with:
- **Comprehensive Backtesting System** (per-asset, per-strategy, per-timeframe)
- **In-Memory Statistics System** (all interactions stored)
- **Multi-Agent Framework** (8 specialized agents)
- **Research from Reference Projects**

### ✅ Current Status (v1.2.0)

| Component | Status |
|-----------|--------|
| 34 Trading Strategies | ✅ Working |
| Unified Trading System | ✅ Working |
| Multi-Asset Data | ✅ Working |
| Core Tests (18/18) | ✅ Passing |

### 🎯 Coming in v2.0

#### 1. Backtesting System
```python
from src.backtesting.engine import (
    BacktestEngine,
    BacktestConfig,
    Timeframe,
    AssetType
)

engine = BacktestEngine()

# Single backtest
config = BacktestConfig(
    symbol="AAPL",
    asset_type=AssetType.STOCK_US,
    timeframe=Timeframe.DAY_1,
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2024, 1, 1),
    initial_capital=100000
)
results = engine.run_backtest(config, "all")

# Multi-asset
results = engine.run_multi_asset_backtest(
    symbols=["AAPL", "MSFT", "GOOGL"],
    asset_types=[AssetType.STOCK_US] * 3,
    timeframe=Timeframe.DAY_1,
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2024, 1, 1)
)

# Multi-timeframe
results = engine.run_multi_timeframe_backtest(
    symbol="AAPL",
    asset_type=AssetType.STOCK_US,
    timeframes=[Timeframe.DAY_1, Timeframe.HOUR_4, Timeframe.HOUR_1],
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2024, 1, 1)
)
```

#### 2. In-Memory Statistics
```python
from src.backtesting.memory import BacktestMemory

memory = BacktestMemory()

# Store results
memory.store_result(backtest_result)

# Get best strategy
best = memory.get_best_strategy("AAPL")

# Get rankings
rankings = memory.get_strategy_rankings("AAPL")

# Full report
report = memory.get_full_report()
```

#### 3. Multi-Agent Framework (8 Agents)
```python
from src.agents.coordinator import AgentCoordinator

coordinator = AgentCoordinator()
coordinator.initialize_all_agents()

# Run analysis pipeline
result = coordinator.run_analysis_pipeline(
    symbol="AAPL",
    asset_type="stock_us"
)
```

### 📋 8 Specialized Agents

| Agent | Purpose | Capabilities |
|-------|---------|--------------|
| **DataAgent** | Data collection | fetch_price_data, get_fundamentals |
| **AnalystAgent** | Analysis | technical_analysis, calculate_indicators |
| **StrategistAgent** | Signals | generate_signals, combine_signals |
| **RiskAgent** | Risk management | calculate_var, assess_drawdown |
| **TraderAgent** | Order execution | submit_order, manage_positions |
| **SentimentAgent** | Sentiment | news_analysis, social_sentiment |
| **MLAgent** | ML predictions | train_model, generate_signal |
| **PortfolioAgent** | Portfolio | optimize_weights, rebalance |

### 📊 Research from Reference Projects

| Project | Key Features to Incorporate |
|---------|----------------------------|
| **Freqtrade** | Strategy framework, backtesting, dry-run, Telegram integration |
| **FinceptTerminal** | 100+ data connectors, CFA analytics, AI personas |
| **Quanta AI** | Multi-agent architecture, 6 specialized agents, memory system |
| **Quant-Nanggoe-AI** | Market regime detection, pressure normalization |
| **Zenbot** | Genetic algorithm optimizer, MongoDB persistence |

### 📁 New File Structure (v2.0)

```
ai-hedge-fund/
├── src/
│   ├── agents/
│   │   ├── base_agent.py         # BaseAgent abstract class
│   │   ├── coordinator.py        # AgentCoordinator
│   │   ├── data_agent.py         # DataAgent
│   │   ├── analyst_agent.py      # AnalystAgent
│   │   ├── strategist_agent.py   # StrategistAgent
│   │   ├── risk_agent.py         # RiskAgent
│   │   ├── trader_agent.py       # TraderAgent
│   │   ├── sentiment_agent.py    # SentimentAgent
│   │   ├── ml_agent.py           # MLAgent
│   │   └── portfolio_agent.py    # PortfolioAgent
│   ├── backtesting/
│   │   ├── engine.py             # BacktestEngine
│   │   ├── memory.py             # BacktestMemory
│   │   ├── metrics.py            # Metrics calculator
│   │   └── visualization.py      # Chart generation
│   ├── core/
│   │   ├── statistics_manager.py # StatisticsManager
│   │   ├── interaction_logger.py # InteractionLogger
│   │   ├── event_bus.py          # EventBus
│   │   └── config.py             # Configuration
│   ├── strategies/
│   │   ├── unified_retail_strategy.py
│   │   ├── quantitative_strategies.py
│   │   ├── legendary_investors.py
│   │   └── strategy_registry.py  # NEW: Strategy management
│   ├── tools/
│   │   ├── unified_data_provider.py
│   │   ├── enhanced_data_provider.py  # Multi-timeframe
│   │   └── data_cache.py         # NEW: Caching
│   └── trading/
│       ├── paper_trading.py      # PaperTradingEngine
│       ├── live_trading.py       # LiveTradingEngine
│       └── order_manager.py      # OrderManager
├── backtest_runner.py            # NEW: Backtest CLI
├── dashboard.py                  # NEW: Streamlit dashboard
├── agents_cli.py                 # NEW: Agent CLI
└── docs/
    ├── DEVELOPMENT_PLAN_v2.md    # Complete plan
    ├── architecture.md           # Architecture docs
    └── api.md                    # API docs
```

### 🚀 Development Roadmap

```
Week 1-2: Core Infrastructure
├── BacktestEngine skeleton
├── BacktestMemory system
├── InteractionLogger
└── EnhancedDataProvider (multi-timeframe)

Week 3-4: Integration
├── AgentCoordinator
├── StrategyRegistry
└── Unified backtest pipeline

Week 5-6: Advanced Features
├── ML integration (FreqAI-style)
├── Hyperparameter optimization
└── Walkforward analysis

Week 7-8: Production
├── Paper trading mode
├── Live trading integration
└── Performance monitoring
```

### 📚 Documentation

| Document | Description |
|----------|-------------|
| `docs/DEVELOPMENT_PLAN_v2.md` | Complete v2.0 development plan |
| `docs/architecture.md` | System architecture docs |
| `docs/api.md` | API reference |
| `docs/backtesting.md` | Backtesting guide |
| `docs/agents.md` | Agent documentation |

### 🔗 References

- [Building a Multi-Agent AI Trading System](https://medium.com/@ishveen/building-a-multi-agent-ai-trading-system-technical-deep-dive-into-architecture-b5ba216e70f3)
- [Freqtrade GitHub](https://github.com/freqtrade/freqtrade)
- [PyBroker](https://github.com/edtechre/pybroker)
- [VectorBT](https://github.com/polakowo/vectorbt)

### Quick Test (Current v1.2.0)

```bash
cd /home/mulky/ai-hedge-fund

# Test unified trading system
python3 unified_trading_system.py AAPL --days 200

# Test with crypto
python3 unified_trading_system.py BTC --asset crypto --days 200

# Run portfolio analysis
python3 unified_trading_system.py --portfolio

# Run tests
python3 -m pytest test_core_modules.py test_minimal.py test_isolated.py test_langchain_free.py -v
```

---

*Last Updated: 2026-01-16*

### 📋 New SMC/ICT Concepts Summary

| Concept | Class | Purpose |
|---------|-------|---------|
| OTE | `OTEAnalyzer` | Optimal Trade Entry - buy discount, sell premium |
| Kill Zones | `KillZoneAnalyzer` | Session timing (London/NY/Asian) |
| Market Profile | `MarketProfileAnalyzer` | TPO, POC, VAH, VAL analysis |
| Volume Delta | `VolumeDeltaAnalyzer` | Order flow, buying/selling pressure |
| Absorption | `AbsorptionAnalyzer` | Rejection detection at key levels |
| Displacement | `DisplacementAnalyzer` | Strong momentum break detection |
| Mitigation | `MitigationAnalyzer` | Order block mitigation tracking |
| Liquidity Void | `LiquidityVoidAnalyzer` | Unfilled FVG detection |
| Opening Range | `OpeningRangeAnalyzer` | First hour analysis |
| Divergence | `DivergenceAnalyzer` | RSI/MACD divergence detection |
| CVD | `CVDAnalyzer` | Cumulative Volume Delta |
| Trend Line | `TrendLineBreakAnalyzer` | Auto trend line + breaks |
# 1. Fix AbsorptionAnalyzer IndexError
cd /home/mulky/ai-hedge-fund
# File: src/strategies/unified_retail_strategy.py line ~741
# Change:
#   next_direction = 1 if close.iloc[i+1] > close.iloc[i] else -1
# To:
#   if i + 1 < len(close):
#       next_direction = 1 if close.iloc[i+1] > close.iloc[i] else -1
#   else:
#       next_direction = prev_direction

# 2. Test new implementations
python3 -c "
from src.strategies.unified_retail_strategy import RetailStrategyAnalyzer
import pandas as pd, numpy as np

analyzer = RetailStrategyAnalyzer()
print(f'Total strategies: {len(analyzer.strategies)}')

n = 100
np.random.seed(42)
close = pd.Series(np.cumsum(np.random.randn(n)) + 100)
result = analyzer.analyze(close+1, close-1, close, pd.Series(np.random.randint(1000,10000,n)))
print(f'Signal: {result.direction}, Confidence: {result.confidence:.2%}')
"

# 3. Run full test suite
python3 -m pytest test_core_modules.py test_minimal.py test_isolated.py test_langchain_free.py -v
```

### 📊 Strategy Count Update

| Before | After |
|--------|-------|
| 6 strategies | 18 strategies |
| Core: 6 | Core: 6 + Retail: 12 |
| `unified_retail_strategy.py`: ~1200 lines | `unified_retail_strategy.py`: ~2800 lines |

### 📋 New SMC/ICT Concepts Summary

| Concept | Class | Purpose |
|---------|-------|---------|
| OTE | `OTEAnalyzer` | Optimal Trade Entry - buy discount, sell premium |
| Kill Zones | `KillZoneAnalyzer` | Session timing (London/NY/Asian) |
| Market Profile | `MarketProfileAnalyzer` | TPO, POC, VAH, VAL analysis |
| Volume Delta | `VolumeDeltaAnalyzer` | Order flow, buying/selling pressure |
| Absorption | `AbsorptionAnalyzer` | Rejection detection at key levels |
| Displacement | `DisplacementAnalyzer` | Strong momentum break detection |
| Mitigation | `MitigationAnalyzer` | Order block mitigation tracking |
| Liquidity Void | `LiquidityVoidAnalyzer` | Unfilled FVG detection |
| Opening Range | `OpeningRangeAnalyzer` | First hour analysis |
| Divergence | `DivergenceAnalyzer` | RSI/MACD divergence detection |
| CVD | `CVDAnalyzer` | Cumulative Volume Delta |
| Trend Line | `TrendLineBreakAnalyzer` | Auto trend line + breaks |

---

## Build, Lint, and Test Commands

### Core Commands
```bash
poetry install                    # Install dependencies
poetry run python terminal.py     # Start interactive terminal
poetry run python launcher.py AAPL  # Run single asset analysis
poetry run python run_terminal.py   # Alternative terminal launcher
```

### Running Tests
```bash
poetry run pytest                 # Run all tests
poetry run pytest test_core_modules.py          # Run specific test file
poetry run pytest test_core_modules.py::test_technical_indicators  # Run single test
poetry run pytest -v              # Verbose output
poetry run pytest -k "indicator"  # Run tests matching pattern
```

### Linting and Formatting
```bash
poetry run black .                # Format all Python files
poetry run black src/ --check     # Check formatting without changes
poetry run isort .                # Sort imports
poetry run isort --check-only .   # Check import order
poetry run flake8 .               # Run flake8 linter
```

---

## Code Style Guidelines

### Python Version and Type Hints
- **Python 3.11+** required
- Use strict type hints for function signatures and variables
- Use `typing` module for complex types (`Dict`, `List`, `Optional`, `Union`)
- Avoid `Any` unless absolutely necessary

### Imports
```python
# Standard library first
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Third party
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from typing_extensions import Literal

# Local - add project root to path first
sys.path.insert(0, str(Path(__file__).parent))
from src.indicators.technical_indicators import TechnicalIndicators
```

### Naming Conventions
- **Classes**: PascalCase (`PortfolioManager`, `RiskManagementFramework`)
- **Functions/Variables**: snake_case (`calculate_var`, `initial_capital`)
- **Constants**: UPPER_SNAKE_CASE or camelCase for config objects
- **Private methods**: Leading underscore (`_internal_helper`)
- **Files**: snake_case for modules (`technical_indicators.py`)

### Pydantic Models
```python
from pydantic import BaseModel, Field
from typing_extensions import Literal

class PortfolioDecision(BaseModel):
    action: Literal["buy", "sell", "short", "cover", "hold"]
    quantity: int = Field(description="Number of shares to trade")
    confidence: int = Field(description="Confidence 0-100")
    reasoning: str = Field(description="Reasoning for the decision")
```

### File Structure
- Add shebang: `#!/usr/bin/env python3`
- Include docstrings at module and class level
- Add project root to path: `sys.path.insert(0, str(Path(__file__).parent))`
- Use `__init__.py` for package exports

### Error Handling
```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"❌ VALIDATION ERROR: {e}")
    return None
except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()
    raise
```

### Testing Patterns
- Use `assert` for validating results
- Include descriptive print statements with emojis for test output
- Mock LangChain modules when testing core functionality:
```python
sys.modules['langchain_core'] = type(sys)('langchain_core')
```

### Formatting
- Line length: **420 characters** (configured in pyproject.toml)
- Use Black for formatting
- Use isort with `black` profile for imports
- No trailing whitespace

### Project Structure
```
ai-hedge-fund/
├── src/
│   ├── agents/          # AI agent implementations
│   ├── tools/           # Data providers and utilities
│   ├── strategies/      # Trading strategies
│   ├── indicators/      # Technical indicators (34+)
│   ├── optimization/    # Portfolio optimization
│   ├── risk/            # Risk management
│   ├── ml/              # Machine learning
│   ├── paper_trading/   # Simulation engine
│   └── options/         # Options analysis
├── tests/               # Test files
└── terminal.py          # Entry points
```

---

## Module Patterns

### Data Provider Pattern
```python
class MockDataProvider:
    def fetch_data(self, ticker: str, period: str = "30d") -> pd.DataFrame:
        """Generate mock price data"""
        # Implementation
        return df
```

### Indicator Pattern
```python
class SimpleIndicators:
    def __init__(self):
        pass

    def rsi(self, closes: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI"""
        # Implementation
        return result
```

---

*Last Updated: 2026-01-16*
