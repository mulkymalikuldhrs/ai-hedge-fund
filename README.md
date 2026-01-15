# AI Hedge Fund - Professional Quantitative Trading System

🤖 **Enterprise-grade AI-powered hedge fund trading system** with comprehensive portfolio optimization, risk management, and machine learning capabilities.

---

## 👨‍💻 Lead Developer

**Mulky Malikul Dhaher**
- **Email**: [mulkymalikuldhr@mail.com](mailto:mulkymalikuldhr@mail.com)
- **GitHub**: [mulkymalikuldhrs](https://github.com/mulkymalikuldhrs)
- **Instagram**: [mulkymalikuldhr](https://instagram.com/mulkymalikuldhr)

---

## 🏆 Version 2.0 - AI QUANT HEDGE FUND (FULL AI-DRIVEN)

### Current Status (v2.0.0 - Working)
- ✅ **34 Trading Strategies** (18 Retail/SMC + 6 Quantitative + 10 Legendary Investors)
- ✅ **Unified Trading System** (all strategies combined)
- ✅ **Multi-Asset Data** (Stocks, Forex, Crypto, Commodities, Indices)
- ✅ **MT5 Broker Integration** (Live trading ready)
- ✅ **Professional Trading Terminal** (Bloomberg-style web UI)
- ✅ **Mode Manager** (MANUAL, SEMI_AUTO, FULL_AUTO)
- ✅ **43 Tests Passing**

### Key Features v2.0
- 🎯 **Comprehensive Backtesting Engine** (per-asset, per-strategy, per-timeframe)
- 🎯 **Real-time Portfolio Monitor** with WebSocket
- 🎯 **Multi-Agent Framework** (8 specialized agents)
- 🎯 **Professional Trading Terminal** (Web UI - Bloomberg style)
- 🎯 **MT5 Integration** for live trading
- 🎯 **Paper Trading Mode**

---

## 🌟 Core Features

### Multi-Asset Data & Analysis
| Asset Type | Sources | Symbols |
|------------|---------|---------|
| **Stocks** | Yahoo Finance, Alpha Vantage | US, IDX, Global |
| **Forex** | exchangerate-api, MT5 | Major & Minor pairs |
| **Crypto** | CoinGecko, Binance | Bitcoin, Ethereum, Alts |
| **Commodities** | Yahoo Finance, MT5 | Gold, Oil, Gas |
| **Indices** | Yahoo Finance | S&P 500, NASDAQ, IHSG |

### Data Sources Attribution
- **Yahoo Finance** - Stock data (yfinance) - BSD 3-Clause
- **CoinGecko** - Crypto data - CC BY 4.0
- **Alpha Vantage** - Technical indicators - CC BY 4.0
- **MetaTrader 5** - Forex/CFD data - Proprietary
- **Binance** - Crypto exchange data - Proprietary

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /home/mulky/ai-hedge-fund

# Install Python dependencies
pip install dash plotly pandas numpy --break-system-packages
```

### 2. Run Trading Terminal (Web UI)
```bash
# Start Bloomberg-style trading terminal
python3 src/ui/web/trading_terminal.py

# Open browser: http://localhost:8050
```

### 3. Run from Command Line
```bash
# Single stock analysis
python3 unified_trading_system.py AAPL --days 200

# Crypto analysis
python3 unified_trading_system.py BTC --asset crypto --days 200

# Portfolio analysis
python3 unified_trading_system.py --portfolio
```

---

## 📊 Trading Terminal Features

```
┌─────────────────────────────────────────────────────────────────┐
│  🤖 AI QUANT HEDGE FUND v2.0          CONNECTED                 │
├─────────────────────────────────────────────────────────────────┤
│  Portfolio    Daily PnL    Win Rate    Profit Factor  Positions │
│  $126,789    +$1,234     68%          2.34          3           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐  ┌──────────────────────────────────┐  │
│  │ CHARTS              │  │ POSITIONS           WATCHLIST    │  │
│  │  [Interactive       │  │                                    │  │
│  │   Candlestick with  │  │  SYMBOL SIDE VOL  ENTRY  PNL      │  │
│  │   SMA20/SMA50]      │  │  EURUSD BUY  1.0  1.0850  +$250   │  │
│  │                     │  │  GBPUSD BUY  0.5  1.2700  +$125   │  │
│  │  - Zoom/Pan         │  │  USDJPY SELL 0.75 149.50   -$94   │  │
│  │  - Auto-refresh     │  └──────────────────────────────────┘  │
│  │  - Dark Theme       │                                         │
│  └─────────────────────┘                                         │
│                                                                  │
│  ┌─────────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │ STRATEGY SIGNALS    │  │ PERFORMANCE     │  │ ALLOCATION  │  │
│  │                     │  │                 │  │             │  │
│  │ ICT SMC        BUY 72%│  │ [Equity Curve] │  │ [Pie Chart] │  │
│  │ Price Action   BUY 68%│  │                 │  │             │  │
│  │ RSI Divergence BUY 65%│  └─────────────────┘  └─────────────┘  │
│  │ MA Crossover   HOLD 55%│                                       │
│  └─────────────────────┘                                         │
├─────────────────────────────────────────────────────────────────┤
│  MODE: [SEMI-AUTO ▼]  SYMBOL: [EURUSD ▼]  TIMEFRAME: [1m ▼]    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ai-hedge-fund/
├── src/
│   ├── execution/                   # Broker Integration
│   │   └── mt5_broker.py            # MetaTrader 5
│   ├── monitoring/                  # Portfolio Management
│   │   ├── portfolio_models.py      # Position/Trade/Portfolio
│   │   └── portfolio_monitor.py     # Real-time monitor
│   ├── modes/                       # Trading Modes
│   │   ├── mode_manager.py          # MANUAL/SEMI/FULL_AUTO
│   │   └── execution_controller.py  # Order execution
│   ├── ui/                          # User Interfaces
│   │   └── web/
│   │       └── trading_terminal.py  # Bloomberg-style UI
│   ├── strategies/                  # 34 Strategies
│   │   ├── unified_retail_strategy.py
│   │   ├── quantitative_strategies.py
│   │   └── legendary_investors.py
│   ├── tools/                       # Data Providers
│   │   ├── unified_data_provider.py
│   │   └── multi_asset_api.py
│   └── agents/                      # Multi-Agent System
│       └── (8 specialized agents)
├── unified_trading_system.py        # Main system
├── test_v2_components.py            # Tests
└── CREDITS.md                       # Credits & Attribution
```

---

## 📈 Trading Strategies (34 Total)

### Retail & SMC (18 Strategies)
| Strategy | Description |
|----------|-------------|
| ICT SMC | Inner Circle Trader concepts |
| Price Action | Al Brooks methodology |
| Order Block | Smart money concepts |
| Liquidity Sweep | Liquidity grabs |
| Fair Value Gap | Imbalance detection |
| Premium/Discount | Market structure |
| Break of Structure | Momentum detection |
| Change of Character | Trend change |
| And 10 more... |

### Quantitative (6 Strategies)
| Strategy | Description |
|----------|-------------|
| Jim Simons | Statistical patterns |
| Momentum | Multi-timeframe |
| Mean Reversion | Reversals |
| Factor Investing | Multi-factor |
| Earnings Momentum | Earnings surprises |
| Technical Analysis | RSI/MACD/BB |

### Legendary Investors (10 Strategies)
| Investor | Style |
|----------|-------|
| Warren Buffett | Value investing |
| Benjamin Graham | Margin of safety |
| Peter Lynch | Growth investing |
| Michael Burry | Value, behavioral |
| Charlie Munger | Mental models |
| Bill Ackman | Activist |
| Cathie Wood | Innovation |
| Stanley Druckenmiller | Macro |
| Mohnish Pabrai | Clone investing |
| Philip Fisher | Growth |

---

## 🛠️ Dependencies

### Core
- `pandas`, `numpy` - Data processing
- `requests` - HTTP requests
- `python-dotenv` - Environment variables

### Trading
- `MetaTrader5` - MT5 integration
- `ccxt` - Crypto exchanges

### Web UI
- `dash` - Web framework
- `plotly` - Interactive charts
- `gunicorn` - WSGI server

### Testing
- `pytest` - Testing framework

---

## 📊 Performance Metrics

The system calculates:
- **Return Metrics**: Total return, CAGR, monthly returns
- **Risk Metrics**: Volatility, Sharpe ratio, Sortino ratio
- **Drawdown Metrics**: Max drawdown, recovery time
- **Trade Metrics**: Win rate, profit factor, avg win/loss
- **Portfolio Metrics**: Beta, alpha, VaR, CVaR

---

## ⚠️ Disclaimer

This is for **educational purposes only**. Not financial advice. 

Trading financial markets involves substantial risk of loss. Past performance does not guarantee future results.

**The developer (Mulky Malikul Dhaher) is not responsible for any financial losses incurred while using this software.**

---

## 📝 License & Credits

### License
MIT License - See LICENSE file for details.

### Credits
See [CREDITS.md](CREDITS.md) for complete attribution including:
- Developer: **Mulky Malikul Dhaher**
- Data Sources: Yahoo Finance, CoinGecko, Alpha Vantage, MT5, Binance
- Open Source: Freqtrade, Backtrader, QuantConnect Lean, FinRL
- Strategy References: ICT, Warren Buffett, Benjamin Graham, Peter Lynch, Michael Burry, and more

---

**Built with ❤️ by Mulky Malikul Dhaher**

*AI Quant Hedge Fund v2.0 - Professional Trading System*
