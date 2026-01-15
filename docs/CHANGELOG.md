# Changelog

All notable changes to AI Hedge Fund project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-16 (PLANNED)

### 🎯 Major Features Coming

#### Backtesting System
- **Per-Asset Testing** - Test each asset independently
- **Per-Strategy Testing** - Individual strategy analysis
- **Per-Timeframe Testing** - Multi-timeframe analysis (1m, 5m, 15m, 1h, 4h, 1d, 1w)
- **Strategy Comparison** - Side-by-side strategy comparison
- **Detailed Metrics** (Sharpe, Sortino, Calmar, SQN, Profit Factor)

#### In-Memory Statistics System
- **BacktestMemory** - All backtest results stored in memory
- **InteractionLogger** - All system interactions tracked
- **StatisticsManager** - Central metrics aggregation
- **Session Management** - Track backtest sessions

#### Multi-Agent Framework (8 Agents)
1. **DataAgent** - Market data collection
2. **AnalystAgent** - Technical/fundamental analysis
3. **StrategistAgent** - Signal generation
4. **RiskAgent** - Risk assessment (VaR, CVaR)
5. **TraderAgent** - Order execution
6. **SentimentAgent** - News/social sentiment
7. **MLAgent** - Machine learning predictions
8. **PortfolioAgent** - Portfolio optimization

#### Live Trading & Web Integration (NEW - See ADDENDUM)
- **MT4/MT5 Web Integration** - Autonomous trading execution
  - MetaTrader5 Python package integration
  - ZeroMQ connector alternative
  - Web API support
  - Docker headless terminal

- **Real-time Portfolio & PnL Tracking**
  - Position management (open/close/SL/TP)
  - Live PnL calculation
  - WebSocket broadcasting
  - Portfolio statistics

- **Multi-Timeframe Analysis**
  - HTF (Higher Timeframe) bias detection
  - Cross-timeframe signal combination
  - Live data streaming via WebSocket

- **UI/UX Architecture Decision**
  - **RECOMMENDED**: Hybrid approach
  - Primary: Textual TUI (lightweight, fast, no browser)
  - Optional: Streamlit Dashboard (for charts/analytics)
  - REST API + WebSocket for external access

- **Live Terminal Dashboard**
  - Real-time portfolio display
  - ASCII/Unicode candlestick charts
  - Strategy signal monitoring
  - Position management

- **System Interaction Modes**
  1. **MANUAL** - View only, manual execution
  2. **SEMI-AUTO** - Auto analysis, manual confirmation (RECOMMENDED)
  3. **FULL AUTO** - Full autonomous trading (HIGH RISK)

#### New Components (v2.0)
```
src/execution/
├── mt5_broker.py           # MetaTrader5 integration
├── execution_controller.py # Mode-based execution
├── order_manager.py        # Order handling
└── risk_validator.py       # Pre-execution risk check

src/monitoring/
├── portfolio_monitor.py    # Real-time PnL
├── position_tracker.py     # Position management
└── websocket_server.py     # Live updates

src/ui/
├── textual_dashboard.py    # Terminal UI
└── streamlit_dashboard.py  # Web dashboard (optional)

src/modes/
├── mode_manager.py         # Mode configuration
└── semi_auto_workflow.py   # Confirmation flow
```

#### Agent Coordination
- **AgentCoordinator** - Central orchestration
- **Message Passing** - Inter-agent communication
- **Task Queue** - Asynchronous task processing
- **State Management** - Agent state tracking

#### New Commands (v2.0)

```bash
# Backtesting
python3 backtest_runner.py --symbol AAPL --start 2020-01-01 --end 2024-01-01
python3 backtest_runner.py --symbols AAPL,MSFT,GOOGL --strategy all
python3 backtest_runner.py --symbol AAPL --timeframes 1h,4h,1d

# Live Trading (NEW)
python3 live_trader.py --mode semi_auto --symbol EURUSD
python3 live_trader.py --mode full_auto --symbols ALL
python3 live_trader.py --mode manual  # View only

# Terminal Dashboard (NEW)
python3 terminal_dashboard.py

# Web Dashboard (optional)
streamlit run dashboard.py

# Agent CLI (NEW)
python3 agents_cli.py --symbol AAPL --pipeline full
python3 agents_cli.py --status
```

#### Reference Projects Integrated
| Project | Features Borrowed |
|---------|-------------------|
| Freqtrade | Strategy framework, backtesting, dry-run |
| FinceptTerminal | Data connectors, AI personas |
| Quanta AI | Multi-agent, memory system |
| Quant-Nanggoe-AI | Market regime, pressure normalization |
| Zenbot | Genetic algorithm, visual backtesting |
| MetaTrader5 | Python integration, order execution |
| AutoTrader | Broker abstraction, portfolio management |

#### Research & Web References
- [Building a Multi-Agent AI Trading System](https://medium.com/@ishveen/building-a-multi-agent-ai-trading-system-technical-deep-dive-into-architecture-b5ba216e70f3)
- [Freqtrade Backtesting](https://github.com/freqtrade/freqtrade)
- [PyBroker ML Trading](https://github.com/edtechre/pybroker)
- [VectorBT](https://github.com/polakowo/vectorbt)
- [Neural Network Trading (arXiv)](https://arxiv.org/html/2508.02356v1)
- [FinAgent Orchestration (arXiv)](https://arxiv.org/pdf/2512.02227)

### Documentation
- `docs/DEVELOPMENT_PLAN_v2.md` - Core development plan
- `docs/DEVELOPMENT_PLAN_v2_ADDENDUM.md` - **NEW** Live trading & UI architecture
- `docs/architecture.md` - System architecture (NEW)
- `docs/api.md` - API documentation (NEW)
- `docs/backtesting.md` - Backtesting guide (NEW)
- `docs/agents.md` - Agent documentation (NEW)
- `docs/live_trading.md` - Live trading guide (NEW)
- `docs/ui_guide.md` - UI/Dashboard guide (NEW)

### New Commands (v2.0)

```bash
# Backtesting
python3 backtest_runner.py --symbol AAPL --start 2020-01-01 --end 2024-01-01
python3 backtest_runner.py --symbols AAPL,MSFT,GOOGL --strategy all
python3 backtest_runner.py --symbol AAPL --timeframes 1h,4h,1d

# Multi-Agent Analysis
python3 agents_cli.py --symbol AAPL --pipeline full
python3 agents_cli.py --status

# Dashboard
streamlit run dashboard.py
```

### Documentation
- `docs/DEVELOPMENT_PLAN_v2.md` - Complete development plan
- `docs/architecture.md` - System architecture (NEW)
- `docs/api.md` - API documentation (NEW)
- `docs/backtesting.md` - Backtesting guide (NEW)
- `docs/agents.md` - Agent documentation (NEW)

### Added

- 🆕 **12 New SMC/ICT Concepts Implemented** (`unified_retail_strategy.py`)
  
  #### High Priority
  - **OTE (Optimal Trade Entry)** - ICT concept untuk entry di zona premium/discount optimal
    - Deteksi discount zone (<50% range) = BUY opportunity
    - Deteksi premium zone (>50% range) = SELL opportunity
    - `OTEAnalyzer` class dengan scoring system
  
  - **Kill Zones** - Session-based trading windows dengan probabilitas tinggi
    - London Kill Zone (08:00-11:00 UTC)
    - NY Kill Zone (13:00-16:00 UTC)
    - Asian Session (00:00-08:00 UTC)
    - London/NY Overlap (13:00-14:00 UTC)
    - `KillZoneAnalyzer` class dengan liquidity window detection

  #### Medium Priority
  - **Market Profile / TPO Analysis**
    - Point of Control (POC) calculation
    - Value Area High/Low (VAH/VAL) - 70% volume
    - Profile shape detection (b-shape, p-shape, normal)
    - Auction type classification (balanced, unfinished, tail)
    - Initial Balance (IB) analysis
    - `MarketProfileAnalyzer` class

  - **Volume Delta / Order Flow**
    - Per-candle delta calculation
    - Buying/Selling pressure ratio
    - Cumulative delta tracking
    - Order flow quality assessment (strong/weak/neutral)
    - `VolumeDeltaAnalyzer` class

  - **Absorption Detection**
    - Rejection candle detection (long wicks)
    - Failed break attempt counter
    - Time-at-level analysis
    - `AbsorptionAnalyzer` class

  - **Displacement Analysis**
    - Strong momentum candle detection
    - Pullback zone calculation
    - Target after displacement
    - `DisplacementAnalyzer` class

  - **Mitigation Counter**
    - Order block mitigation tracking
    - Active/Partial/Fully mitigated classification
    - Best BUY/SELL OB identification
    - `MitigationAnalyzer` class

  - **Liquidity Void Detection**
    - Unfilled FVG tracking
    - Gap quality assessment (strong/weak)
    - Void depth analysis
    - `LiquidityVoidAnalyzer` class

  - **Opening Range Analysis**
    - First hour high/low calculation
    - OR break detection
    - Failed breakout counter
    - Session-specific OR (London/NY/Asian)
    - `OpeningRangeAnalyzer` class

  #### Low Priority
  - **Divergence Detection**
    - RSI divergence (regular & hidden)
    - MACD divergence (regular & hidden)
    - Bullish/Bearish classification
    - Strength scoring
    - `DivergenceAnalyzer` class

  - **Cumulative Volume Delta (CVD)**
    - Per-candle delta calculation
    - CVD trend analysis (rising/falling/flat)
    - Zero line cross detection
    - Extremes tracking
    - `CVDAnalyzer` class

  - **Trend Line Break Detection**
    - Automatic trend line drawing
    - Swing high/low identification
    - Break quality assessment (strong/weak)
    - Retest zone calculation
    - `TrendLineBreakAnalyzer` class

- 📊 **Updated RetailStrategyAnalyzer**
  - Increased dari 6 menjadi 18 strategies
  - New weighted scoring system
  - All new signals included in metadata
  - Cross-strategy confluence detection

### Changed

- Renamed `SNRAnalyzer` ke `SupportResistanceAnalyzer` untuk clarity
- Updated `RetailStrategyAnalyzer.weights` dengan 18 strategies
- Improved `_aggregate_signals()` untuk handle semua new signals
- Added new dataclasses: `OTESignal`, `KillZoneSignal`, `MarketProfileSignal`, `VolumeDeltaSignal`, `AbsorptionSignal`, `DisplacementSignal`, `MitigationSignal`, `LiquidityVoidSignal`, `OpeningRangeSignal`, `DivergenceSignal`, `CVDSignal`, `TrendLineBreakSignal`

### Fixed

- Test files `test_core_modules.py`, `test_minimal.py`, `test_isolated.py`, `test_langchain_free.py` - removed return statements, proper pytest assertions
- Fixed `test_data_providers` import untuk menggunakan `POPULAR_TICKERS` bukan `MultiAssetAPI`
- Fixed API signatures: `quantitative_strategies` (final_signal), `portfolio_optimizer` (min_variance_portfolio), `risk_management` (portfolio_value argument), `technical_indicators` (bollinger_bands signature)

### Data Sources ✅

- Created `src/tools/unified_data_provider.py` - All-in-one data access
- All 6 data sources connected to REAL APIs:
  | Asset Type | Source | Endpoint |
  |------------|--------|----------|
  | US Stocks | Yahoo Finance | `yfinance.Ticker()` |
  | IDX Stocks | Yahoo Finance | `yfinance.Ticker(ticker.JK)` |
  | Forex | exchangerate-api.com | `open.er-api.com/v6/latest/USD` |
  | Crypto | CoinGecko | `api.coingecko.com/api/v3` |
  | Commodities | Yahoo Finance | `yfinance.Ticker(GC=F)` |
  | Indices | Yahoo Finance | `yfinance.Ticker(^GSPC)` |
- Fixed CoinGecko API (removed invalid 'interval' parameter)
- All APIs verified working with real-time data

### Documentation

- Created `audit.md` - Comprehensive codebase audit report
- Updated `AGENTS.md` dengan coding guidelines
- All new classes have Google-style docstrings

## [1.0.0] - 2026-01-14

### Added

- 🚀 **Initial Release** - Multi-Asset AI Trading System
- 🌍 **Indonesian Stock Support (IDX)**
  - Added `multi_asset_api.py` with Yahoo Finance integration
  - Support for BBCA.JK, BBRI.JK, BMRI.JK, etc.
  - IHSG market index tracking

- 💱 **Forex Support**
  - exchangerate-api.com integration (FREE, no API key)
  - USD/IDR, EUR/USD, GBP/JPY, and 150+ currencies
  - Cross-rate calculation

- 🪙 **Cryptocurrency Support**
  - CoinGecko API for historical data (FREE)
  - Binance API for spot prices
  - BTC, ETH, SOL, XRP, ADA, DOGE, and 400+ coins

- 🥇 **Commodity Support**
  - Yahoo Finance integration for GOLD, SILVER, OIL
  - Real-time price tracking

- 🤖 **OpenCode AI Integration** (FREE!)
  - `opencode/grok-code` - Fastest model
  - `opencode/big-pickle` - Larger context
  - `opencode/gpt-5-nano` - GPT-5 variant
  - `opencode/glm-4.7-free` - Zhipu AI model
  - CLI-based wrapper (no API key needed!)

- 📊 **Interactive Launcher**
  - `launcher.py` - Full interactive CLI
  - Menu-driven interface
  - Asset type selection
  - AI model selection
  - Color-coded output

- 📈 **Multi-Asset Analysis Script**
  - `run_multi_asset.py` - Quick analysis
  - Portfolio summary
  - Signal confidence scoring

- 📚 **Documentation**
  - `README.md` - Complete user guide
  - `BLUEPRINT.md` - Architecture and roadmap
  - Inline code comments

### Changed

- Refactored data fetching to support multiple asset types
- Added structured output handling for OpenCode responses
- Improved error handling for AI analysis

### Fixed

- JSON parsing for AI responses (fallback mechanism)
- Indonesian stock ticker formatting (.JK suffix)
- Currency formatting for IDR, crypto

### Removed

- Puter SDK integration (requires API key)
- Legacy single-asset workflow

### Dependencies

- Added: `yfinance==1.0`
- Updated: `httpx==0.27.0` (already present)

### Known Issues

- AI models may not always return valid JSON (handled with fallback)
- Some crypto historical data may be rate-limited
- Indonesian stock data may have slight delays

## [0.0.0] - 2026-01-13

### Added

- Project skeleton created
- Original AI Hedge Fund code structure
- Base agent implementations (Warren Buffett, Michael Burry, etc.)
- LangGraph workflow setup

---

## 📌 Version Guide

| Version | Status | Description |
|---------|--------|-------------|
| 1.2.0 | Current | Unified Trading System Fixed |
| 1.1.0 | Previous | SMC/ICT Concepts + Test Fixes |
| 1.0.0 | Previous | Initial multi-asset release |
| 0.0.0 | Pre-release | Project skeleton |

## 🔜 Future Releases

### v1.2.0 (Target: 2026-02-01)
- [x] Unified Trading System integration
- [ ] Better JSON parsing
- [ ] Save/load portfolios
- [ ] Telegram bot integration

### v1.2.0 (Target: 2026-03-01)
- Web dashboard (Streamlit)
- Backtesting module
- Technical indicators

### v2.0.0 (Target: TBD)
- Full backtesting system
- Paper trading
- Multi-user support
