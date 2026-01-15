# AI Hedge Fund - Professional Quantitative Trading System

🤖 **Enterprise-grade AI-powered hedge fund trading system** with comprehensive portfolio optimization, risk management, and machine learning capabilities.

## 🏆 Version 2.0 - AI QUANT HEDGE FUND (FULL AI-DRIVEN)

This is Phase 2 of our journey to build a world-class quant hedge fund system. We've added:

### Current Status (v1.2.0 - Working)
- ✅ **34 Trading Strategies** (18 Retail/SMC + 6 Quantitative + 10 Legendary Investors)
- ✅ **Unified Trading System** (all strategies combined)
- ✅ **Multi-Asset Data** (Stocks, Forex, Crypto, Commodities, Indices)
- ✅ **Core Tests Pass** (18/18 tests passing)

### Coming in v2.0
- 🎯 **Comprehensive Backtesting Engine** (per-asset, per-strategy, per-timeframe)
- 🎯 **In-Memory Statistics System** (all interactions stored)
- 🎯 **Multi-Agent Framework** (8 specialized agents)
- 🎯 **Paper Trading Mode**
- 🎯 **Streamlit Dashboard**

## 🌟 Core Features

### Multi-Asset Data & Analysis
- **Stocks**: US (NYSE, NASDAQ), Indonesian (IDX), Global
- **Forex**: Major pairs with exchangerate-api
- **Cryptocurrencies**: Bitcoin, Ethereum, altcoins via CoinGecko/Binance
- **Commodities**: Gold, Oil, Natural Gas
- **Indices**: S&P 500, Dow Jones, NASDAQ, IHSG

### Quantitative Strategies
| Strategy | Description | Weight |
|----------|-------------|--------|
| Jim Simons | Statistical pattern recognition | 1.5 |
| Quantitative Momentum | Multi-timeframe momentum | 1.2 |
| Mean Reversion | Oversold/overbought detection | 1.0 |
| Factor Investing | Value/Momentum/Quality factors | 1.3 |
| Earnings Momentum | Earnings acceleration | 1.1 |
| Technical Analysis | RSI/MACD/Bollinger | 0.9 |

### AI Agents
| Agent | Style | Specialty |
|-------|-------|-----------|
| Jim Simons | Quantitative | Pattern recognition |
| Quantitative Analyst | Data-driven | Statistical analysis |
| Technical Analyst | Technical | Chart patterns |
| Factor Investor | Factor-based | Multi-factor models |
| Earnings Momentum | Fundamentals | Earnings surprises |
| Mean Reversion | Contrarian | Reversals |

## 🚀 Installation

```bash
# Clone and install
cd /home/mulky/ai-hedge-fund
pip install -e .

# For ML features (optional)
pip install scikit-learn tensorflow
```

## 📊 Quick Start

### Unified Trading System (Current)
```bash
# Single stock analysis
python3 unified_trading_system.py AAPL --days 200

# Crypto analysis
python3 unified_trading_system.py BTC --asset crypto --days 200

# Portfolio analysis
python3 unified_trading_system.py --portfolio
```

### Backtesting System (Coming v2.0)
```python
from src.backtesting.engine import BacktestEngine, BacktestConfig, Timeframe, AssetType
from datetime import datetime

engine = BacktestEngine()

# Run single backtest
config = BacktestConfig(
    symbol="AAPL",
    asset_type=AssetType.STOCK_US,
    timeframe=Timeframe.DAY_1,
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2024, 1, 1),
    initial_capital=100000
)

results = engine.run_backtest(config, "all")

# Compare all strategies
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

# Multi-timeframe analysis
results = engine.run_multi_timeframe_backtest(
    symbol="AAPL",
    asset_type=AssetType.STOCK_US,
    timeframes=[Timeframe.DAY_1, Timeframe.HOUR_4, Timeframe.HOUR_1],
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2024, 1, 1)
)
```

### Multi-Agent System (Coming v2.0)
```python
from src.agents.coordinator import AgentCoordinator
from src.agents.base_agent import AgentTask

coordinator = AgentCoordinator()
coordinator.initialize_all_agents()

# Run full analysis pipeline
result = coordinator.run_analysis_pipeline(
    symbol="AAPL",
    asset_type="stock_us"
)

# Check status
status = coordinator.get_status()
print(f"Agents: {status['agents']}, Tasks: {status['tasks_completed']}")
```

## 📁 Project Structure (v2.0)

```
ai-hedge-fund/
├── src/
│   ├── agents/                    # Multi-Agent Framework
│   │   ├── base_agent.py          # Agent base class
│   │   ├── coordinator.py         # Agent orchestration
│   │   ├── data_agent.py          # Data collection
│   │   ├── analyst_agent.py       # Technical analysis
│   │   ├── strategist_agent.py    # Signal generation
│   │   ├── risk_agent.py          # Risk assessment
│   │   ├── trader_agent.py        # Order execution
│   │   ├── sentiment_agent.py     # Sentiment analysis
│   │   ├── ml_agent.py            # ML predictions
│   │   └── portfolio_agent.py     # Portfolio optimization
│   ├── backtesting/               # Backtesting Engine
│   │   ├── engine.py              # Main backtest engine
│   │   ├── memory.py              # In-memory statistics
│   │   ├── metrics.py             # Performance metrics
│   │   └── visualization.py       # Chart generation
│   ├── core/                      # Core System
│   │   ├── statistics_manager.py  # Statistics tracking
│   │   ├── interaction_logger.py  # Interaction logging
│   │   ├── event_bus.py           # Event system
│   │   └── config.py              # Configuration
│   ├── strategies/                # Trading Strategies
│   │   ├── unified_retail_strategy.py  # 18 SMC/ICT
│   │   ├── quantitative_strategies.py  # 6 Quantitative
│   │   ├── legendary_investors.py      # 10 Legendary
│   │   └── strategy_registry.py        # Strategy management
│   ├── tools/                     # Data & Utilities
│   │   ├── unified_data_provider.py    # Multi-asset data
│   │   ├── enhanced_data_provider.py   # Multi-timeframe
│   │   └── data_cache.py               # Caching layer
│   └── trading/                   # Trading Systems
│       ├── paper_trading.py       # Paper trading
│       ├── live_trading.py        # Live trading
│       └── order_manager.py       # Order management
├── unified_trading_system.py      # Current trading system
├── backtest_runner.py             # Backtest runner (v2.0)
├── dashboard.py                   # Streamlit dashboard (v2.0)
├── agents_cli.py                  # Agent CLI (v2.0)
└── docs/
    ├── DEVELOPMENT_PLAN_v2.md     # Full development plan
    ├── architecture.md            # Architecture docs
    └── api.md                     # API documentation
```

## 🛠️ Dependencies

Managed via Poetry. Key packages:
- `pandas`, `numpy` - Data processing
- `scipy` - Scientific computing
- `scikit-learn` - Machine learning
- `yfinance` - Stock data
- `colorama`, `rich` - Terminal output
- `fastapi`, `pydantic` - API framework

## 📈 Performance Metrics

The backtesting engine calculates:
- **Return Metrics**: Total return, CAGR, monthly returns
- **Risk Metrics**: Volatility, Sharpe ratio, Sortino ratio
- **Drawdown Metrics**: Max drawdown, avg drawdown, recovery time
- **Trade Metrics**: Win rate, profit factor, avg win/loss
- **Risk Metrics**: VaR (95%, 99%), CVaR, beta

## ⚠️ Disclaimer

This is for **educational purposes only**. Not financial advice. 
Past performance does not guarantee future results.
Always do your own research before trading.

## 📝 License

MIT License - See LICENSE file for details.

---

**Built with ❤️ using Python, AI, and Quantitative Finance**
