# 🚀 AI HEDGE FUND ENTERPRISE - QUICK START GUIDE

## 🎯 ENTERPRISE-GRADE AI TRADING SYSTEM NOW AVAILABLE!

### Professional Terminal (NEW!)
```bash
cd /home/mulky/ai-hedge-fund
python3 -c "
from src.integrations.web_terminal import web_terminal
web_terminal.run_terminal_loop()
"
```

### Legacy Interactive Mode
```bash
cd /home/mulky/ai-hedge-fund
python launcher.py
```

---

### Analisis Cepat

```bash
# Indonesian Stocks
poetry run python run_multi_asset.py --tickers BBCA,BBRI,BMRI --type stock_idx

# US Stocks  
poetry run python run_multi_asset.py --tickers AAPL,MSFT,NVDA --type stock_us

# Crypto
poetry run python run_multi_asset.py --tickers BTC,ETH,SOL --type crypto

# Forex
poetry run python run_multi_asset.py --tickers USD/IDR,EUR/USD --type forex

# Commodities
poetry run python run_multi_asset.py --tickers GOLD,OIL --type commodity

# Mixed Portfolio
poetry run python run_multi_asset.py --tickers BBCA,USD/IDR,BTC,GOLD --auto
```

---

## 🏗️ Enterprise System Architecture

```
ai-hedge-fund/
├── 🚀 launcher.py                    # Legacy launcher
├── 🎯 TERMINAL_RUN_COMMAND.md        # Professional terminal guide
├── 📊 FINAL_SYSTEM_DOCUMENTATION.md  # Complete system docs
├── 📋 QUICK_START.md                 # This guide
├── 📂 src/
│   ├── 🤖 agents/
│   │   ├── enhanced_agents.py        # Multi-agent system
│   │   └── portfolio_manager.py      # Fixed decision engine
│   ├── 📊 strategies/
│   │   └── quantitative_strategies.py # 6 quant strategies
│   ├── 📈 indicators/
│   │   └── technical_indicators.py   # 34 technical indicators
│   ├── 🔗 integrations/              # ENTERPRISE COMPONENTS
│   │   ├── integration_manager.py    # Component orchestration
│   │   ├── entry_analysis.py         # Intelligent strategy selection
│   │   ├── web_terminal.py           # Professional terminal
│   │   ├── metatrader_bridge.py      # MT4/MT5 integration
│   │   ├── quant_strategies_analysis.py # Advanced quant analysis
│   │   ├── retail_strategies.py      # 10 retail strategies
│   │   ├── analysis_display.py       # Comprehensive visualization
│   │   ├── enhanced_sentiment_agent.py # Sentiment integration
│   │   └── enhanced_autonomous_trader.py # Autonomous trading
│   ├── 🛡️ risk/                      # Risk management
│   └── 🛢️ tools/                     # Data providers
├── 📂 tests/                         # Comprehensive test suite
├── 📋 WUW.md                         # Coordination log
├── 📊 TESTING_PLAN.md                # Testing roadmap
└── 📚 AGENT*_TASKS.md               # Task specifications
```

---

## 🔑 Fitur Enterprise (NEW!)

| Fitur | Status | Deskripsi |
|-------|--------|-----------|
| 🤖 Multi-Agent Analysis | ✅ Complete | 6 AI agents + sentiment analysis |
| 📊 16 Trading Strategies | ✅ Complete | 6 Quant + 10 Retail strategies |
| 🎯 Intelligent Entry Selection | ✅ Complete | Confidence-based strategy choice |
| 🛡️ Advanced Risk Management | ✅ Complete | Kill-switches, VaR, position sizing |
| 🔌 MetaTrader Integration | ✅ Complete | MT4/MT5 bridge for auto-trading |
| 💻 Professional Terminal | ✅ Complete | MetaTrader-style interface |
| 📈 Real-Time Analysis | ✅ Complete | Live market data processing |
| 🚀 External Integrations | ✅ Complete | 4 major AI projects integrated |

## 📊 Legacy Features

| Fitur | Status | Sumber Data |
|-------|--------|-------------|
| 🇺🇸 US Stocks | ✅ Done | Yahoo Finance |
| 🇮🇩 IDX Stocks | ✅ Done | Yahoo Finance (.JK) |
| 💱 Forex | ✅ Done | exchangerate-api.com (FREE) |
| 🪙 Crypto | ✅ Done | CoinGecko + Binance |
| 🥇 Commodities | ✅ Done | Yahoo Finance |
| 📈 Indices | ✅ Done | Yahoo Finance |

---

## 🎯 Professional Terminal Commands

### Analysis Commands
```bash
Terminal> analyze AAPL          # Full enterprise analysis
Terminal> analyze AAPL quant    # Quantitative strategies only
Terminal> analyze AAPL retail   # Retail strategies only
Terminal> results              # Show last analysis results
```

### Trading Commands
```bash
Terminal> order buy AAPL 100   # Place market buy order
Terminal> order sell AAPL 50   # Place market sell order
Terminal> connect 5            # Connect to MetaTrader 5
Terminal> connect 4            # Connect to MetaTrader 4
```

### Strategy Commands
```bash
Terminal> strategies           # Show all 10 retail strategies
Terminal> add TSLA            # Add to watchlist
Terminal> dashboard           # Show professional dashboard
```

## 🤖 AI Models (Enhanced)

```bash
# Enterprise AI Analysis
- Multi-Agent Decision Making
- Sentiment Analysis Integration
- Quantitative Strategy Optimization
- Risk-Adjusted Position Sizing
- Autonomous Trading Logic

# Legacy Models (Still Available)
--model opencode/grok-code    # Fast analysis
--model opencode/big-pickle   # Deep analysis
--model opencode/gpt-5-nano   # Advanced reasoning
```

---

## 📊 Enterprise Analysis Output

```
🤖 AI HEDGE FUND ENTERPRISE ANALYSIS - AAPL
═══════════════════════════════════════════════════════════════

🎯 ENTRY ANALYSIS: mean_reversion strategy selected (59.5%)
   Risk Level: medium | Time Horizon: medium | Priority: medium

📊 MULTI-AGENT ANALYSIS - AAPL
   Sentiment Agent: NEUTRAL (50.0%) - News + Social Media
   Quantitative Strategies: 6 strategies analyzed
   Retail Strategies: 10 strategies available

🛡️ RISK ASSESSMENT
   Kill-switch: ACTIVE | VaR: 2.1% | Max Drawdown: 15%
   Position Size: 1,247 shares | Stop Loss: $148.25

🔌 METATRADER READY
   MT4 Bridge: Connected | MT5 Bridge: Ready
   Auto-execution: Available | Order monitoring: Active

📈 PORTFOLIO SUMMARY
╔═══════════════════════════════════════════════════════════════╗
║  Ticker      │  Strategy │  Confidence │  Action            ║
╠═══════════════════════════════════════════════════════════════╣
║  AAPL       │  Mean Rev │    59.5%    │  BUY 1,247 shares   ║
╠═══════════════════════════════════════════════════════════════╣
║  Total Signals: BUY: 3  SELL: 1  HOLD: 2                     ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## ⚠️ Enterprise System Notes

1. **Professional Terminal** - Use `python3 -c "from src.integrations.web_terminal import web_terminal; web_terminal.run_terminal_loop()"`
2. **MetaTrader Integration** - Requires MT4/MT5 installation for live trading
3. **External Dependencies** - LangChain removed, system works standalone
4. **Rate Limiting** - Built-in rate limiting for all data providers
5. **Backup System** - All analyses saved with timestamps

---

## 📚 Enterprise Documentation

### Core Documentation
- `FINAL_SYSTEM_DOCUMENTATION.md` - Complete enterprise system overview
- `TERMINAL_RUN_COMMAND.md` - Professional terminal usage guide
- `TESTING_PLAN.md` - Comprehensive testing roadmap
- `WUW.md` - Real-time coordination and progress log

### Component Documentation
- `AGENT1_TASKS.md` - Portfolio Manager & Core Systems
- `AGENT2_TASKS.md` - Technical Systems & Testing
- `COORDINATION_STATUS.md` - System integration status

### Legacy Documentation
- `README.md` - Basic usage guide
- `docs/CHANGELOG.md` - Version history
- `BLUEPRINT.md` - System architecture
- `MEMORY.md` - Project context and decisions

---

## 🎯 System Capabilities Summary

### 🤖 AI-Powered Analysis
- Multi-Agent Decision Making (6 specialized agents)
- Sentiment-Driven Trading Signals
- Autonomous Strategy Selection
- Real-time Market Analysis
- Confidence-Based Recommendations

### 📊 Strategy Coverage
- 6 Quantitative Strategies (Jim Simons, Momentum, Mean Reversion, etc.)
- 10 Retail Strategies (Scalping, Swing, Position Trading, etc.)
- Risk-Adjusted Position Sizing
- Intelligent Entry Selection
- Backtest Performance Tracking

### 🛡️ Enterprise Risk Management
- Kill-Switch Protection
- Dynamic Stop Loss/Take Profit
- Portfolio Risk Analysis (VaR, Drawdown)
- Multi-Layer Risk Controls
- Real-time Risk Monitoring

### 🔌 Professional Integration
- MetaTrader 4/5 Bridge
- Automated Order Execution
- Real-time Position Monitoring
- Professional Terminal Interface
- External Project Integrations

---

## 🚀 Ready for Production Trading!

**The AI Hedge Fund Enterprise System is now complete and ready for live trading operations.**

**Start with the Professional Terminal command and begin your advanced algorithmic trading journey!**

🎯 **ENTERPRISE-GRADE AI TRADING SYSTEM ACTIVE** 🎯

**Happy Advanced Trading! 🚀✨**

---

> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
>
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
