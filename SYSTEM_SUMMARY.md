# AI HEDGE FUND - SYSTEM SUMMARY

## 📦 Complete System Overview

### Core Components

```
ai-hedge-fund/
├── 📄 ENTRY POINTS
│   ├── terminal.py          # Interactive terminal (RECOMMENDED)
│   ├── launcher.py          # Command line launcher
│   ├── enhanced_analyzer.py # Multi-strategy analyzer
│   └── run_multi_asset.py   # Simple multi-asset analysis
│
├── 📂 src/
│   ├── 📂 strategies/        # 6 Quantitative Strategies
│   │   ├── quantitative_strategies.py
│   │   ├── jim_simmons.py
│   │   ├── momentum.py
│   │   └── ...
│   │
│   ├── 📂 agents/           # 6 AI Agents + Original Agents
│   │   ├── enhanced_agents.py  # NEW: Jim Simons, Quant Analyst, etc.
│   │   ├── warren_buffett.py   # Original agent
│   │   ├── michael_burry.py    # Original agent
│   │   └── ...
│   │
│   └── 📂 tools/
│       ├── advanced_data_provider.py  # Multi-source data
│       └── multi_asset_api.py         # Basic data
│
├── 📂 docs/                 # Documentation
│   ├── README.md
│   ├── QUICK_START.md
│   ├── BLUEPRINT.md
│   ├── MEMORY.md
│   ├── TODO.md
│   ├── ROADMAP.md          # Future plans
│   ├── CHANGELOG.md
│   └── DEPENDENCIES.md
│
├── 📂 backups/              # Automatic backups
│   └── 20260114_*/
│
└── 📄 pyproject.toml        # Dependencies
```

---

## 🎯 Quick Reference

### How to Run

```bash
# 1. Interactive Terminal (RECOMMENDED)
cd /home/mulky/ai-hedge-fund
python terminal.py

# 2. Quick Command Line
python launcher.py AAPL,MSFT,BTC
python launcher.py BBCA,BBRI --type stock_idx
python launcher.py BTC,ETH,SOL --type crypto

# 3. Enhanced Analysis
python enhanced_analyzer.py --tickers AAPL,MSFT,NVDA
```

### Supported Assets

| Type | Examples | Data Source |
|------|----------|-------------|
| 🇺🇸 US Stocks | AAPL, MSFT, NVDA, GOOGL | Yahoo Finance |
| 🇮🇩 IDX Stocks | BBCA, BBRI, BMRI, TLKM | Yahoo Finance (.JK) |
| 💱 Forex | USD/IDR, EUR/USD, GBP/JPY | exchangerate-api.com |
| 🪙 Crypto | BTC, ETH, SOL, XRP | CoinGecko + Binance |
| 🥇 Commodities | GOLD, SILVER, OIL | Yahoo Finance |

### Strategies & Agents

#### Strategies (Quantitative)
1. **Jim Simons** - Statistical pattern recognition (weight: 1.5)
2. **Quantitative Momentum** - Multi-timeframe momentum (weight: 1.2)
3. **Mean Reversion** - Oversold/overbought detection (weight: 1.0)
4. **Factor Investing** - Value, Momentum, Quality, Volatility (weight: 1.3)
5. **Earnings Momentum** - Earnings acceleration (weight: 1.1)
6. **Technical Analysis** - RSI, MACD, Bollinger Bands (weight: 0.9)

#### Agents (AI)
1. **Jim Simons Agent** - Quant analysis
2. **Quantitative Analyst** - Momentum analysis
3. **Technical Analyst** - Technical indicators
4. **Factor Investor** - Multi-factor analysis
5. **Earnings Momentum** - Earnings trends
6. **Mean Reversion** - Oversold/overbought

---

## ✅ Dependencies (All Installed)

```bash
# Core
python >= 3.11
langchain >= 0.3.7
langgraph >= 0.2.56

# Data
yfinance >= 1.0
pandas >= 2.1.0
numpy >= 1.24.0
httpx >= 0.27.0

# UI
colorama >= 0.4.6
rich >= 13.9.4
questionary >= 2.1.0

# Web
fastapi >= 0.104.0
pydantic >= 2.4.2

# Install
poetry install
```

---

## 🔧 Commands Reference

### Terminal Commands

```bash
# Main Menu
1 - New Analysis (custom tickers)
2 - US Stocks
3 - Indonesia Stocks
4 - Cryptocurrency
5 - Forex
6 - Commodities
7 - All Strategies (6 strategies + 6 agents)
8 - Exit
```

### Launcher Commands

```bash
# Syntax
python launcher.py TICKERS [OPTIONS]

# Examples
python launcher.py AAPL                    # Single ticker, auto-detect
python launcher.py AAPL,MSFT,NVDA          # Multiple tickers
python launcher.py BBCA,BBRI --type stock_idx  # Specify type
python launcher.py BTC --type crypto       # Crypto
python launcher.py USD/IDR --type forex    # Forex
python launcher.py GOLD --type commodity   # Commodity

# Options
--type, -t     Asset type (stock_us, stock_idx, forex, crypto, commodity, auto)
--model, -m    AI model (opencode/grok-code, opencode/big-pickle, opencode/gpt-5-nano)
--help         Show help
```

### Enhanced Analyzer Commands

```bash
# Syntax
python enhanced_analyzer.py --tickers TICKERS [OPTIONS]

# Examples
python enhanced_analyzer.py --tickers AAPL
python enhanced_analyzer.py --tickers AAPL,MSFT,NVDA --type stock_us
python enhanced_analyzer.py --tickers BTC,ETH,SOL --type crypto --model opencode/big-pickle
```

---

## 📊 Sample Outputs

### Terminal Output
```
╔══════════════════════════════════════════════════════════════════════╗
║                  🤖 AI HEDGE FUND TERMINAL                          ║
╚══════════════════════════════════════════════════════════════════════╝

  1 📊 New Analysis
  2 🇺🇸 US Stocks
  3 🇮🇩 Indonesia Stocks
  4 🪙 Cryptocurrency
  5 💱 Forex
  6 🥇 Commodities
  7 🧠 All Strategies
  8 🚪 Exit

  ➜ 
```

### Analysis Result
```
╔═══════════════════════════════════════════════════════════════════╗
║  PORTFOLIO SUMMARY                                               ║
╠═══════════════════════════════════════════════════════════════════╣
║  TICKER     SIGNAL    CONFIDENCE    STRATEGIES    AGENTS         │
╠═══════════════════════════════════════════════════════════════════╣
║  AAPL      ✅ BUY    75%           6             6              │
║  BBCA      ✅ BUY    72%           6             6              │
║  BTC       ✅ BUY    70%           6             6              │
╠═══════════════════════════════════════════════════════════════════╣
║  BUY: 3    SELL: 0    HOLD: 0                                       ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## 📁 File Inventory

### Core Files
| File | Size | Purpose |
|------|------|---------|
| `terminal.py` | ~12KB | Interactive terminal |
| `launcher.py` | ~8KB | CLI launcher |
| `enhanced_analyzer.py` | ~12KB | Multi-strategy analyzer |
| `run_multi_asset.py` | ~10KB | Simple analyzer |

### Source Files
| Path | Files | Purpose |
|------|-------|---------|
| `src/strategies/` | 1 file | Quantitative strategies |
| `src/agents/` | 2 files | AI agents |
| `src/tools/` | 2 files | Data providers |

### Documentation
| File | Size | Purpose |
|------|------|---------|
| `README.md` | ~9KB | Main docs |
| `QUICK_START.md` | ~3KB | Quick start |
| `BLUEPRINT.md` | ~9KB | Architecture |
| `MEMORY.md` | ~8KB | Context |
| `TODO.md` | ~3KB | Tasks |
| `ROADMAP.md` | ~12KB | Future plans |
| `docs/CHANGELOG.md` | ~3KB | History |
| `docs/DEPENDENCIES.md` | ~5KB | Dependencies |

---

## 🔒 Safety Features

1. **No API Keys Required** - All data sources are FREE!
2. **Error Handling** - Graceful fallbacks for failed API calls
3. **Rate Limiting** - Built-in rate limiters for external APIs
4. **Caching** - 1-hour cache to reduce API calls
5. **Backup** - Automatic backups before major changes

---

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Module not found | Run `poetry install` |
| API errors | Check internet connection |
| Rate limiting | Wait and retry |
| Empty data | Ticker may be delisted |

### Check System
```bash
# Test Python
python --version

# Test dependencies
poetry run python -c "import yfinance, langchain, colorama; print('OK')"

# Test data providers
poetry run python -c "from src.tools.advanced_data_provider import data_provider; print('OK')"
```

---

## 📞 Support

- **Documentation**: See `docs/` folder
- **Issues**: Check `TODO.md` for known issues
- **Roadmap**: See `docs/ROADMAP.md` for future plans

---

**System Version**: 1.1.0  
**Last Updated**: 2026-01-14  
**Status**: ✅ Production Ready
