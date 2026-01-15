# Changelog

All notable changes to AI Hedge Fund project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-01-16

### 🚀 New Features Implemented

#### Multi-Timeframe Analyzer
- **Higher Timeframe Bias Detection** - Analyzes 4H, 1D, 1W for market trend
- **Cross-Timeframe Signal Combination** - Combines HTF and LTF signals
- **Market Structure Analysis** - Identifies higher highs/lower lows
- **Liquidity Level Detection** - Find buy/sell side liquidity
- **Key Levels** - Support, resistance, pivot points

```python
from src.analysis.mtf_analyzer import create_mtf_analyzer

analyzer = create_mtf_analyzer()
signal = analyzer.analyze("EURUSD", htf="4H", ltf="15m")
```

#### Paper Trading Mode
- **Realistic Simulation** - Slippage, commission, execution delays
- **Risk Management** - Max positions, position size limits, daily loss limits
- **Order Types** - Market, limit, stop orders
- **Trade History** - Complete P&L tracking and statistics
- **Event Callbacks** - Subscribe to order/position events

```python
from src.paper_trading.paper_trader import create_paper_trader

trader = create_paper_trader(initial_capital=100000)
trader.place_order("EURUSD", "BUY", 1.0, sl=1.0800, tp=1.1000)
stats = trader.get_statistics()
```

#### Telegram Integration
- **Real-time Notifications** - Trade signals, position updates
- **Daily Reports** - Win rate, profit factor, P&L summary
- **Error Alerts** - System errors and warnings
- **Async Support** - Non-blocking message queue

```python
from src.integrations.telegram_notifier import create_telegram_notifier

notifier = create_telegram_notifier(bot_token, chat_id, enabled=True)
await notifier.send_signal(signal, mode="semi_auto")
```

#### Docker Deployment
- **Production Dockerfile** - Optimized for deployment
- **Docker Compose** - Full stack with Redis, Prometheus, Grafana
- **Nginx Reverse Proxy** - SSL termination, load balancing

#### Professional Trading Terminal
- **Bloomberg-style UI** - Dark theme, real-time updates
- **Interactive Charts** - Plotly candlestick with indicators
- **Live Positions** - P&L tracking, SL/TP management
- **Strategy Signals** - 10 strategy signals with confidence
- **Watchlist** - Real-time price updates

```bash
# Start trading terminal
python3 src/ui/web/trading_terminal.py
# Open http://localhost:8050
```

#### Autonomous Development System
- **Task Tracking** - Progress tracking and documentation
- **Auto-Commit** - Every change is committed
- **Session Reports** - Development summary

### 📁 New Files

| File | Purpose |
|------|---------|
| `src/utils/autonomous_dev.py` | Autonomous development workflow |
| `src/analysis/mtf_analyzer.py` | Multi-timeframe analyzer |
| `src/paper_trading/paper_trader.py` | Paper trading simulator |
| `src/integrations/telegram_notifier.py` | Telegram notifications |
| `Dockerfile.production` | Production Docker image |
| `docker-compose.yml` | Full deployment stack |
| `docs/API.md` | Complete API documentation |
| `CREDITS.md` | Developer credits & data sources |

### ✅ Testing

- **43 Tests Passing** (18 core + 25 v2.0 components)
- All new modules tested independently
- Integration tests for paper trader
- MTF analyzer demo working
- Telegram integration tested

### 📝 Documentation

- **CREDITS.md** - Complete attribution
  - Lead Developer: Mulky Malikul Dhaher
  - Data Sources: Yahoo Finance, CoinGecko, Alpha Vantage, MT5, Binance
  - Open Source References: Freqtrade, Backtrader, QuantConnect, FinRL

- **API.md** - Comprehensive API documentation
  - Paper Trader API
  - MTF Analyzer API
  - Trading Terminal endpoints
  - WebSocket API
  - Examples and code snippets

### 🎯 Components Complete

| Component | Status | Location |
|-----------|--------|----------|
| MT5 Broker | ✅ | `src/execution/mt5_broker.py` |
| Portfolio Models | ✅ | `src/monitoring/portfolio_models.py` |
| Portfolio Monitor | ✅ | `src/monitoring/portfolio_monitor.py` |
| Mode Manager | ✅ | `src/modes/mode_manager.py` |
| Execution Controller | ✅ | `src/modes/execution_controller.py` |
| MTF Analyzer | ✅ | `src/analysis/mtf_analyzer.py` |
| Paper Trader | ✅ | `src/paper_trading/paper_trader.py` |
| Telegram Notifier | ✅ | `src/integrations/telegram_notifier.py` |
| Trading Terminal | ✅ | `src/ui/web/trading_terminal.py` |
| Docker Config | ✅ | `Dockerfile.production`, `docker-compose.yml` |

### 🔧 Commands

```bash
# Trading Terminal
python3 src/ui/web/trading_terminal.py

# Paper Trading
python3 -c "
from src.paper_trading.paper_trader import create_paper_trader
trader = create_paper_trader()
trader.place_order('EURUSD', 'BUY', 1.0)
print(trader.get_status())
"

# MTF Analysis
python3 -c "
from src.analysis.mtf_analyzer import create_mtf_analyzer
a = create_mtf_analyzer()
print(a.get_market_summary('EURUSD'))
"

# Docker Deployment
docker-compose up -d

# Run Tests
python3 -m pytest test_v2_components.py -v  # 25 tests
python3 -m pytest test_core_modules.py -v   # 18 tests
```

---

## [2.0.0] - 2026-01-16

### 🎯 Major Features (Initial v2.0 Release)

#### Backtesting System
- Per-Asset Testing
- Per-Strategy Testing  
- Per-Timeframe Testing
- Strategy Comparison
- Detailed Metrics (Sharpe, Sortino, Calmar, SQN, Profit Factor)

#### In-Memory Statistics System
- BacktestMemory
- InteractionLogger
- StatisticsManager
- Session Management

#### Multi-Agent Framework (8 Agents)
1. DataAgent - Market data collection
2. AnalystAgent - Technical/fundamental analysis
3. StrategistAgent - Signal generation
4. RiskAgent - Risk assessment
5. TraderAgent - Order execution
6. SentimentAgent - News/social sentiment
7. MLAgent - Machine learning predictions
8. PortfolioAgent - Portfolio optimization

#### 18 New SMC/ICT Concepts
- OTE (Optimal Trade Entry)
- Kill Zones (London, NY, Asian)
- Market Profile / TPO Analysis
- Volume Delta / Order Flow
- Absorption Detection
- Displacement Analysis
- Mitigation Counter
- Liquidity Void Detection
- Opening Range Analysis
- Divergence Detection
- Cumulative Volume Delta (CVD)
- Trend Line Break Detection

---

## [1.2.0] - 2026-01-15

### Fixed

- Test files with proper pytest assertions
- Fixed API signatures in quantitative_strategies, portfolio_optimizer, risk_management
- Removed invalid CoinGecko API parameters
- Fixed return statements in test files

### Data Sources Verified

- Yahoo Finance - US/IDX Stocks
- CoinGecko - Cryptocurrency
- exchangerate-api - Forex
- MetaTrader5 - Ready for integration

---

## [1.1.0] - 2026-01-14

### Added

- 18 SMC/ICT Strategies to unified_retail_strategy.py
- OTEAnalyzer, KillZoneAnalyzer, MarketProfileAnalyzer
- VolumeDeltaAnalyzer, AbsorptionAnalyzer, DisplacementAnalyzer
- MitigationAnalyzer, LiquidityVoidAnalyzer, OpeningRangeAnalyzer
- DivergenceAnalyzer, CVDAnalyzer, TrendLineBreakAnalyzer

---

## [1.0.0] - 2026-01-14

### Added

- Multi-Asset AI Trading System
- Indonesian Stock Support (IDX)
- Forex Support (150+ currencies)
- Cryptocurrency Support (400+ coins)
- Commodity Support (Gold, Oil)
- OpenCode AI Integration (FREE!)
- Interactive Launcher
- Multi-Asset Analysis Script

---

*Last Updated: 2026-01-16*
*Version: 2.1.0*
