# AI Hedge Fund v2.3.0 - Professional Quantitative Trading System

Enterprise-grade AI-powered hedge fund trading system with comprehensive portfolio optimization, risk management, and machine learning capabilities.

---

## Lead Developer

**Mulky Malikul Dhaher**
- **Email**: [mulkymalikuldhr@mail.com](mailto:mulkymalikuldhr@mail.com)
- **GitHub**: [mulkymalikuldhrs](https://github.com/mulkymalikuldhrs)
- **Instagram**: [mulkymalikuldhr](https://instagram.com/mulkymalikuldhr)

---

## Version 2.3.0 - Agent Constitution Integration

### System Overview

| Component | Status | Lines |
|-----------|--------|-------|
| **Multi-Agent Orchestrator** | ✅ Working | 500+ |
| **Graham Value Strategy** | ✅ Working | 400+ |
| **Turtle Trading Strategy** | ✅ Working | 450+ |
| **Kelly Criterion** | ✅ Working | 500+ |
| **Risk Parity Optimizer** | ✅ Working | 600+ |
| **VaR Module** | ✅ Working | 400+ |
| **LLM7 Client** | ✅ Working | 500+ |
| **Interactive Menu (main.py)** | ✅ Working | 1,741 |
| **Enhanced Data Providers** | ✅ Working | 1,000+ |
| **Streamlit Dashboard** | ✅ Working | 700+ |
| **CLI Terminal** | ✅ Working | 600+ |
| **Telegram Bot** | ✅ Working | 400+ |
| **ML Signal Generator** | ✅ Working | 700+ |
| **Backtesting Engine** | ✅ Working | 300+ |
| **Paper Trading** | ✅ Working | 500+ |
| **Auto-Heal System** | ✅ Working | 3,200+ |
| **Exness Integration** | ✅ Working | 500+ |
| **Live Trading System** | ✅ Working | 800+ |

### Key Features v2.3.0

**Agent Constitution Integration:**
- **Meta-Prinsip Agent** - 6 highest principles for autonomous behavior
- **Agent Lifecycle** - Bootstrap → Analyze → Plan → Execute → Validate → Document
- **Mode Operations** - Normal, Audit, Lock, Recovery
- **Session Management** - JSON/Markdown export for Opencode
- **Logging & Audit** - Complete activity tracking

**RISET Fullstack Implementation:**
- **Multi-Agent System (MAS)** - 4 specialist agents with message passing
- **Graham Value Investing** - Graham Number, margin of safety, intrinsic value
- **Turtle Trading** - Original Turtle rules with ATR-based position sizing
- **Kelly Criterion** - Optimal position sizing (Full/Half/Quarter/Adaptive)
- **Risk Parity** - Equal risk contribution portfolio optimization
- **Value at Risk (VaR)** - Parametric, Historical, Monte Carlo methods
- **LLM7 Integration** - gpt-5-nano with fallback to backup LLMs

**Previous Features:**
- **Interactive Single Entry Point** - Menu-driven system (main.py)
- **Multi-Source Free Data** - Indonesian stocks, global markets, crypto, forex, commodities, indices
- **53+ Trading Strategies** (18 Retail/SMC + 6 Quantitative + 10 Legendary Investors + 13 Enhanced)
- **Exness Demo Trading** - $100,000 demo account with auto-trading
- **3 ML Models** (Random Forest, XGBoost, LSTM)
- **Multi-Account Support** via account switching
- **3 Trading Modes** (Manual, Semi-Auto, Full-Auto)
- **Streamlit Web Dashboard** with auto-browser open
- **Enhanced CLI Terminal** with menu system
- **Telegram Notifications** (@dhaherautobot)
- **Auto-Heal System** - Health, backup, strategy evaluation
- **Risk Management** - 2% per trade, 6% daily max

---

## Quick Start

### Installation

```bash
cd /home/mulky/ai-hedge-fund
pip install -r requirements.txt
```

### Interactive Launcher (Recommended)

```bash
# Start menu-driven interface
python3 launcher.py

# Options:
# 1. Web Dashboard - Opens browser UI
# 2. CLI Terminal - Interactive command line
# 3. Quick Analysis - Single symbol analysis
# 4. Backtest - Run strategy backtest
# 5. Paper Trading - Simulation mode
# 6. System Status - Check all modules
# 7. Configuration - View settings
# 8. Exit
```

### Web Dashboard

```bash
# Auto-opens browser at http://localhost:8501
python3 launcher.py --dashboard
# or
python3 main.py --dashboard
```

### CLI Terminal

```bash
# Interactive command line interface
python3 launcher.py --cli
# or
python3 main.py --cli
```

### Quick Analysis

```bash
# Single symbol
python3 launcher.py --analyze AAPL
python3 main.py AAPL

# Multiple symbols
python3 main.py AAPL,BTC,USD/IDR

# With asset type
python3 main.py BTC --asset crypto
python3 main.py EURUSD --asset forex
```

### Backtesting

```bash
# Interactive backtest
python3 launcher.py --backtest

# Command line backtest
python3 main.py --backtest EURUSD --days 180
python3 main.py --backtest AAPL --days 365

# Portfolio backtest
python3 main.py --backtest --portfolio AAPL,MSFT,GOOGL
```

### System Status

```bash
# Check all modules
python3 launcher.py --status
# or
python3 main.py --status
```

---

## Auto-Heal System v2.2.1

The Auto-Heal System provides self-healing, monitoring, and optimization capabilities for your trading system.

### Components

| Module | Description | Lines |
|--------|-------------|-------|
| **Health Monitor** | System health checks, auto-restart, error tracking | 650+ |
| **Backup Manager** | Automatic daily backups, rotation, restore | 550+ |
| **Strategy Evaluator** | Performance ranking, recommendations | 700+ |
| **Monitoring Dashboard** | Real-time CLI/Streamlit dashboard | 500+ |
| **Orchestrator** | Unified control of all auto-systems | 450+ |

### Features

#### Health Monitor
- System resource monitoring (CPU, Memory, Disk)
- Module availability checks (9 core modules)
- Auto-restart on critical conditions (CPU/Memory >95%)
- Metrics export to JSON (`health_metrics.json`)

#### Auto-Backup
- Automatic daily backups (scheduled at 3 AM)
- Backup rotation (7 daily, 4 weekly retention)
- Compressed archives (.tar.gz with SHA256 checksum)
- Backup verification and restore capability

#### Strategy Evaluator
- Evaluates all 34+ trading strategies
- Performance ranking by win rate, profit factor, Sharpe ratio
- Risk-adjusted scoring (return, risk, consistency)
- Market condition recommendations
- JSON export (`strategy_rankings.json`)

#### Monitoring Dashboard
- Real-time CLI dashboard with visual progress bars
- Streamlit web dashboard option
- Historical trends (last 60 data points)
- Module status display

### Usage

```bash
# Interactive menu (recommended)
python3 launcher.py
# Select option [8] Auto-Heal System

# Auto-Heal entry point
python3 auto_heal_system.py              # Show status
python3 auto_heal_system.py --daemon     # Run as daemon
python3 auto_heal_system.py --health     # Health check
python3 auto_heal_system.py --backup     # Create backup
python3 auto_heal_system.py --evaluate   # Evaluate strategies
python3 auto_heal_system.py --monitor    # Run dashboard
python3 auto_heal_system.py --all        # Run all checks

# Via main.py
python3 main.py --autoheal               # Launch Auto-Heal System
```

### Configuration

#### Health Monitor
```python
config = HealthConfig(
    check_interval=30,                    # Check every 30 seconds
    cpu_warning_threshold=80.0,           # Yellow at 80%
    cpu_critical_threshold=95.0,          # Red at 95%
    memory_warning_threshold=80.0,
    memory_critical_threshold=95.0,
    restart_on_critical=True,             # Auto-restart on critical
    max_restarts_per_hour=3               # Prevent restart loops
)
```

#### Backup Configuration
```python
config = BackupConfig(
    retention_days=7,                     # Keep 7 daily backups
    retention_weeks=4,                    # Keep 4 weekly backups
    schedule_daily_hour=3,                # Backup at 3 AM
    compression=True                      # .tar.gz compression
)
```

#### Strategy Scoring Weights
```python
weights = {
    "win_rate": 0.25,
    "profit_factor": 0.20,
    "sharpe_ratio": 0.20,
    "max_drawdown": 0.15,                 # Lower is better
    "expectancy": 0.10,
    "consistency": 0.10
}
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AI HEDGE FUND v2.2                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐    ┌──────────────────┐    ┌────────────────────────┐│
│  │ DATA LAYER   │───▶│ INDICATORS LAYER │───▶│ STRATEGY LAYER         ││
│  │              │    │                  │    │                        ││
│  │ • Yahoo      │    │ • RSI (7/14/21)  │    │ • 18 Retail/SMC       ││
│  │ • CoinGecko  │    │ • MACD           │    │ • 6 Quantitative      ││
│  │ • ExchangeRate│   │ • Bollinger      │    │ • 10 Legendary        ││
│  │              │    │ • ATR, ADX       │    │ • ML Ensemble (3)     ││
│  │              │    │ • Ichimoku       │    │                        ││
│  │              │    │ • SuperTrend     │    │ Total: 34+ Strategies ││
│  │              │    │ • OBV, VWAP      │    │                        ││
│  └──────────────┘    └──────────────────┘    └───────────┬────────────┘│
│                                                           │              │
│  ┌────────────────────────────────────────────────────────────────────┐│
│  │                    PRESENTATION LAYER                              ││
│  │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    ││
│  │   │ Streamlit Web   │  │ CLI Terminal    │  │ Telegram Bot    │    ││
│  │   │ Dashboard       │  │ (Interactive)   │  │ (Notifications) │    ││
│  │   │ Port: 8501      │  │ Menu System     │  │ Commands        │    ││
│  │   └─────────────────┘  └─────────────────┘  └─────────────────┘    ││
│  └────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐│
│  │                    TRADING LAYER                                   ││
│  │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    ││
│  │   │ Paper Trading   │  │ Backtesting     │  │ MetaTrader      │    ││
│  │   │ Simulation      │  │ Walk-forward    │  │ Browser Bridge  │    ││
│  │   └─────────────────┘  └─────────────────┘  └─────────────────┘    ││
│  └────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐│
│  │                    ML LAYER                                        ││
│  │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    ││
│  │   │ Random Forest   │  │ XGBoost         │  │ LSTM Neural     │    ││
│  │   │ Classifier      │  │ Classifier      │  │ Network         │    ││
│  │   └─────────────────┘  └─────────────────┘  └─────────────────┘    ││
│  │                              │                                      ││
│  │                    ┌─────────▼─────────┐                           ││
│  │                    │ Ensemble Voting    │                           ││
│  │                    │ (Majority/Weighted)│                           ││
│  │                    └───────────────────┘                           ││
│  └────────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Multi-Asset Data & Analysis

| Asset Type | Sources | Symbols |
|------------|---------|---------|
| **Indonesian Stocks** | Yahoo Finance (IDX) | BBCA, BBRI, TLKM, UNVR, GOTO, etc. |
| **Global Stocks** | Financial Datasets / Yahoo | AAPL, MSFT, GOOGL, TSLA, NVDA, etc. |
| **Forex** | ExchangeRate-API / Yahoo | EURUSD, GBPUSD, USDJPY, USDIDR, etc. |
| **Crypto** | CoinGecko / Yahoo | BTC, ETH, SOL, XRP, ADA, etc. |
| **Commodities** | Yahoo Finance | XAUUSD (Gold), XAGUSD (Silver), Oil, Gas |
| **Indices** | Yahoo Finance | JCI, S&P 500, NASDAQ, DAX, Nikkei, etc. |

### Enhanced Data Providers

```python
from src.data.enhanced_data_provider import get_unified_data_provider

# Get provider with multiple free sources
provider = get_unified_data_provider()

# Automatic routing to appropriate source
price = provider.get_current_price("AAPL")      # Global stock
price = provider.get_current_price("BBCA")      # Indonesian stock
price = provider.get_current_price("BTC")       # Crypto
price = provider.get_current_price("EURUSD")    # Forex
price = provider.get_current_price("XAUUSD")   # Gold commodity
price = provider.get_current_price("JCI")      # Indonesian index
```

**Data Sources:**
- **Financial Datasets API** - Primary: Global markets (Premium)
- **Yahoo Finance** - Fallback: Stocks, crypto, forex, indices, commodities
- **CoinGecko** - Fallback: Cryptocurrency data
- **ExchangeRate-API** - Fallback: Forex rates

### Indonesian Stocks (IDX)

| Symbol | Name | Category |
|--------|------|----------|
| BBCA | Bank Central Asia Tbk | Banking |
| BBRI | Bank Rakyat Indonesia Tbk | Banking |
| BBNI | Bank Negara Indonesia Tbk | Banking |
| BMRI | Bank Mandiri Tbk | Banking |
| TLKM | Telkom Indonesia Tbk | Telecom |
| UNVR | Unilever Indonesia Tbk | Consumer |
| GOTO | GoTo Gojek Tokopedia Tbk | Tech/Startup |
| ASII | Astra International Tbk | Automotive |

### Data Sources Attribution

- **Financial Datasets API** - Premium market data - API provided
- **Yahoo Finance** - Stock data (yfinance) - BSD 3-Clause
- **CoinGecko** - Crypto data - CC BY 4.0
- **ExchangeRate-API** - Forex data - Free tier

---

## LLM7 Integration

### Primary LLM Configuration

| Setting | Value |
|---------|--------|
| **Primary LLM** | LLM7 |
| **Base URL** | https://api.llm7.io/v1 |
| **Main Model** | gpt-5-nano-2025-08-07 |
| **Fallback Model** | gpt-4.1-nano-2025-04-14 |
| **Temperature** | 0.1 (Low variance) |
| **Max Tokens** | 2000 |

### Backup LLM Providers

| Provider | Model | Purpose |
|----------|--------|---------|
| **OpenRouter** | gpt-4o-mini | Flexible LLM access |
| **Groq** | llama3-70b-8192 | Fast inference |
| **Google Gemini** | gemini-1.5-flash | Quick responses |
| **DeepSeek** | deepseek-chat | Alternative |

### Usage Example

```python
from src.llm.llm7_client import LLM7Client

# Initialize LLM7 client
llm = LLM7Client()

# Generate trading signal
response = llm.generate(
    prompt="Analyze AAPL for buy signal",
    model="gpt-5-nano-2025-08-07",
    temperature=0.1
)

print(response.text)
```

---

## Trading Strategies (34 Total)

### Retail & SMC (18 Strategies)

| Strategy | Description |
|----------|-------------|
| ICT SMC | Inner Circle Trader concepts |
| Price Action | Al Brooks methodology |
| Order Block | Smart money concepts |
| Liquidity Sweep | Liquidity grabs detection |
| Fair Value Gap | Imbalance detection |
| Premium/Discount | Market structure |
| Break of Structure | Momentum detection |
| Change of Character | Trend change detection |
| OTE | Optimal Trade Entry |
| Kill Zones | Session timing (London/NY/Asian) |
| Market Profile | TPO, POC, VAH, VAL |
| Volume Delta | Order flow analysis |
| Absorption | Rejection detection |
| Displacement | Momentum break detection |
| Mitigation | Order block tracking |
| Liquidity Void | FVG detection |
| Opening Range | First hour analysis |
| Divergence | RSI/MACD divergence |

### Quantitative (6 Strategies)

| Strategy | Description |
|----------|-------------|
| Jim Simons | Statistical patterns |
| Momentum | Multi-timeframe momentum |
| Mean Reversion | Price reversals |
| Factor Investing | Multi-factor model |
| Earnings Momentum | Earnings surprises |
| Technical Analysis | RSI/MACD/BB combination |

### Legendary Investors (10 Strategies)

| Investor | Style |
|----------|-------|
| Warren Buffett | Value investing |
| Benjamin Graham | Margin of safety |
| Peter Lynch | Growth investing |
| Michael Burry | Value, behavioral |
| Charlie Munger | Mental models |
| Bill Ackman | Activist investing |
| Cathie Wood | Innovation/growth |
| Stanley Druckenmiller | Macro trading |
| Mohnish Pabrai | Clone investing |
| Philip Fisher | Growth stocks |

---

## ML Signal Generator

### Models

1. **Random Forest Classifier** - Ensemble tree-based classification
2. **XGBoost Classifier** - Gradient boosting
3. **LSTM Neural Network** - Sequential pattern recognition

### Ensemble Voting

- **Majority Voting** - 2+ models agree
- **Weighted Voting** - Based on model confidence

### Signal Thresholds

| Signal | Threshold |
|--------|-----------|
| STRONG_BUY | >= 75% |
| BUY | 60-74% |
| HOLD | 45-59% |
| SELL | 30-44% |
| STRONG_SELL | < 30% |

---

## Risk Management

### Risk Parameters

```python
{
    "max_risk_per_trade": 0.02,      # 2% per trade
    "max_daily_loss": 0.06,          # 6% daily limit
    "max_drawdown_limit": 0.15,      # 15% maximum drawdown
    "min_risk_reward_ratio": 2.0,    # 1:2 minimum R:R
    "kelly_fraction": 0.25           # 25% Kelly criterion
}
```

### Multi-Timeframe Weights

| Timeframe | Weight | Purpose |
|-----------|--------|---------|
| H1 | 40% | Trend bias |
| M15 | 35% | Entry confirmation |
| M5 | 25% | Precise timing |

---

## Trading Modes

| Mode | Description |
|------|-------------|
| **MANUAL** | You confirm all trades |
| **SEMI_AUTO** | Auto position sizing, you confirm |
| **FULL_AUTO** | Autonomous trading |

---

## MetaTrader Integration

### Browser Automation (FREE)

The system uses Playwright to automate MetaTrader Web:

```bash
# MetaTrader Web Terminal
python3 src/execution/metatrader_bridge.py
```

**Features:**
- No paid API required
- Works with any broker's web terminal
- Multi-account support via account switching
- Order execution via browser automation

---

## Project Structure

```
ai-hedge-fund/
├── main.py                      # Unified entry point (v2.2.1)
├── launcher.py                  # Interactive menu system (868 lines)
├── auto_heal_system.py          # Auto-Heal entry point (300+ lines)
├── start_live_trading.py         # Live trading entry point (27KB)
├── test_integration.py          # Integration tests
│
├── src/
│   ├── agents/                  # Multi-Agent System (v2.2.2)
│   │   └── mas_orchestrator.py  # 4 specialist agents (500+ lines)
│   │
│   ├── auto_heal/               # Auto-Heal System (3,200+ lines)
│   │   ├── __init__.py
│   │   ├── health_monitor.py    # Health checking, auto-restart
│   │   ├── backup_manager.py    # Backup/restore system
│   │   ├── strategy_evaluator.py # Strategy ranking
│   │   ├── monitoring_dashboard.py # Real-time dashboard
│   │   └── orchestrator.py      # Unified control
│   │
│   ├── dashboard/
│   │   ├── streamlit_app.py     # Web Dashboard UI
│   │   ├── cli_terminal.py      # CLI Terminal
│   │   └── telegram_bot.py      # Telegram notifications
│   │
│   ├── data/
│   │   ├── enhanced_data_provider.py  # Multi-source free data (1,000+ lines)
│   │   └── free_data_provider.py # Yahoo/CoinGecko/ExchangeRate
│   │
│   ├── llm/                     # LLM Integration (v2.2.2)
│   │   └── llm7_client.py      # LLM7 API client (500+ lines)
│   │
│   ├── ml/
│   │   └── ml_signal_generator.py # RF/XGBoost/LSTM models
│   │
│   ├── backtesting/
│   │   ├── vectorbt_engine.py  # Fast vectorized backtesting (400+ lines)
│   │   └── backtest_engine.py   # Walk-forward analysis
│   │
│   ├── paper_trading/
│   │   └── paper_trader.py      # Simulation engine
│   │
│   ├── risk/                    # Risk Management (v2.2.2)
│   │   ├── kelly.py            # Kelly Criterion (500+ lines)
│   │   ├── risk_parity.py      # Risk Parity optimizer (600+ lines)
│   │   └── var.py              # Value at Risk (400+ lines)
│   │
│   ├── strategies/              # Trading Strategies
│   │   ├── graham_value.py     # Graham investing (400+ lines)
│   │   ├── turtle_trading.py   # Turtle Trading (450+ lines)
│   │   ├── sepa.py            # CANSLIM + VCP (450+ lines)
│   │   ├── unified_retail_strategy.py  # 18 SMC strategies
│   │   ├── quantitative_strategies.py  # 6 quantitative
│   │   └── legendary_investors.py      # 10 investor styles
│   │
│   ├── indicators/
│   │   └── technical_indicators.py     # 34+ indicators
│   │
│   └── tools/
│       └── unified_data_provider.py     # Data aggregation
│
├── docs/                        # Documentation
├── AGENTS.md                    # Agent framework docs
├── CHANGELOG.md                 # Version history
└── README.md                    # This file
```

---

## Dependencies

### Core
- `pandas`, `numpy` - Data processing
- `requests` - HTTP requests
- `python-dotenv` - Environment variables

### ML
- `scikit-learn` - Random Forest
- `xgboost` - Gradient boosting
- `tensorflow` - LSTM neural network

### Dashboard
- `streamlit` - Web UI
- `plotly` - Interactive charts

### Trading
- `playwright` - Browser automation
- `yfinance` - Yahoo Finance data
- `ccxt` - Crypto exchange integration

### Telegram
- `python-telegram-bot` - Telegram Bot API

### Testing
- `pytest` - Testing framework

---

## Commands Reference

### Launcher Commands

```bash
python3 launcher.py              # Interactive menu
python3 launcher.py --dashboard  # Web UI (auto-opens browser)
python3 launcher.py --cli        # CLI Terminal
python3 launcher.py --analyze    # Quick analysis
python3 launcher.py --backtest   # Backtest mode
python3 launcher.py --trade      # Paper trading
python3 launcher.py --status     # System status
python3 launcher.py --config     # Show configuration
python3 launcher.py --autoheal   # Auto-Heal System
```

### Main Entry Point

```bash
python3 main.py                  # Interactive mode
python3 main.py AAPL             # Quick analysis
python3 main.py BTC --asset crypto  # Crypto analysis
python3 main.py --dashboard      # Web UI
python3 main.py --cli            # CLI
python3 main.py --backtest EURUSD --days 180  # Backtest
python3 main.py --status         # System status
python3 main.py --portfolio AAPL,MSFT  # Portfolio
python3 main.py --autoheal       # Auto-Heal System
```

### Auto-Heal System

```bash
python3 auto_heal_system.py              # Show status
python3 auto_heal_system.py --daemon     # Run as daemon
python3 auto_heal_system.py --health     # Health check
python3 auto_heal_system.py --backup     # Create backup
python3 auto_heal_system.py --evaluate   # Evaluate strategies
python3 auto_heal_system.py --monitor    # Run dashboard
python3 auto_heal_system.py --all        # Run all checks
```

---

## Telegram Bot Commands

```
/start - Initialize bot
/status - Get current positions
/positions - List open trades
/analyze AAPL - Quick analysis
/backtest EURUSD --days 90 - Run backtest
/help - Show all commands
```

---

## Performance Metrics

The system calculates:

- **Return Metrics**: Total return, CAGR, monthly returns
- **Risk Metrics**: Volatility, Sharpe ratio, Sortino ratio
- **Drawdown Metrics**: Max drawdown, recovery time
- **Trade Metrics**: Win rate, profit factor, avg win/loss
- **ML Metrics**: Model accuracy, precision, recall, F1

---

## File Manifest

### Core Modules (9 modules verified working)

| File | Purpose |
|------|---------|
| `src/memory/enhanced_memory_system.py` | SQLite + JSON storage |
| `src/trading_plan/trading_plan.py` | Risk parameters |
| `src/data/free_data_provider.py` | Free data sources |
| `src/execution/metatrader_bridge.py` | Browser automation |
| `src/dashboard/telegram_bot.py` | Telegram notifications |
| `src/ml/ml_signal_generator.py` | ML models |
| `src/backtesting/backtest_engine.py` | Walk-forward analysis |
| `src/paper_trading/paper_trader.py` | Simulation |
| `src/dashboard/streamlit_app.py` | Web UI |

### Launchers

| File | Purpose |
|------|---------|
| `main.py` | Unified entry point |
| `launcher.py` | Interactive menu system |

---

## Git History

```
d76363b - Complete interactive launcher
d84ee7b - Auto-open browser with xdg-open
25c1303 - Unified entry point (main.py)
7716322 - Backtesting modules
ec16e9c - Phase 1 & 2 complete
```

---

## Testing

### Run Integration Tests

```bash
cd /home/mulky/ai-hedge-fund
python3 test_integration.py
```

### Expected Output

```
✓ Memory System
✓ Trading Plan
✓ Data Provider
✓ MT Bridge
✓ Telegram Bot
✓ ML Generator
✓ Backtesting
✓ Paper Trading
✓ Dashboard

Loaded: 9/9 modules
```

---

## Data Fetching Examples

```python
from src.data.free_data_provider import FreeDataProvider

provider = FreeDataProvider()

# Stocks
stocks = provider.get_stock_data("AAPL", period="180d")

# Crypto
crypto = provider.get_crypto_data("BTC", days=180)

# Forex
forex = provider.get_forex_data("EURUSD")
```

---

## Disclaimer

This is for **educational purposes only**. Not financial advice.

Trading financial markets involves substantial risk of loss. Past performance does not guarantee future results.

**The developer (Mulky Malikul Dhaher) is not responsible for any financial losses incurred while using this software.**

---

## License & Credits

### License

MIT License - See LICENSE file for details.

### Credits

- **Developer**: Mulky Malikul Dhaher
- **Data Sources**: Yahoo Finance, CoinGecko, ExchangeRate-API
- **Open Source References**: Freqtrade, Backtrader, QuantConnect Lean, FinRL
- **Strategy References**: ICT, Warren Buffett, Benjamin Graham, Peter Lynch, Michael Burry, and more

---

**Built with ❤️ by Mulky Malikul Dhaher**

*AI Quant Hedge Fund v2.2.2 - RISET Fullstack Implementation*
