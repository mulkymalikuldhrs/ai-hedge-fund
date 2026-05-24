# TODO List - AI Hedge Fund

## 🎯 Current Sprint (v1.2.0) - Immediate Tasks

### High Priority

- [ ] **Technical Indicators Library**
  - [ ] Create `src/indicators/` package
  - [ ] Implement 30+ indicators (RSI, MACD, Bollinger, Stochastic, CCI, ADX, etc.)
  - [ ] Add tests for each indicator

- [ ] **Backtesting Engine**
  - [ ] Create `src/backtesting/backtest_engine.py`
  - [ ] Implement historical simulation
  - [ ] Add performance metrics (Sharpe, Sortino, Max Drawdown)

- [ ] **Fix AI JSON Parsing**
  - [ ] Improve structured output handling in `src/llm/models.py`
  - [ ] Add regex-based JSON extraction
  - [ ] Test with all OpenCode models

### Medium Priority

- [ ] **Strategy Templates**
  - [ ] Create MACD strategy template
  - [ ] Create RSI strategy template
  - [ ] Create Bollinger Bands strategy
  - [ ] Create Ichimoku strategy

- [ ] **Trade Executor**
  - [ ] Implement stop loss / take profit
  - [ ] Add trailing stop functionality
  - [ ] Support multiple order types

- [ ] **Test Coverage**
  - [ ] Test multi_asset_api.py with all asset types
  - [ ] Test launcher.py interactive mode
  - [ ] Test error scenarios

### Low Priority

- [ ] **Configuration System**
  - [ ] Create `src/config/manager.py`
  - [ ] Add YAML/JSON config support
  - [ ] Environment variable handling

- [ ] **Hyperparameter Optimization**
  - [ ] Create `src/optimization/hyperopt.py`
  - [ ] Implement random/bayesian search
  - [ ] Add parameter space definition

## 📋 Backlog

### Features

- [ ] **Save/Load Portfolios**
  - [ ] Add portfolio persistence (JSON/SQLite)
  - [ ] `python launcher.py --load portfolio.json`
  - [ ] Export to CSV functionality

- [ ] **Telegram Bot Integration**
  - [ ] Create `telegram_bot.py`
  - [ ] Add /analyze command
  - [ ] Add /portfolio command
  - [ ] Setup webhook

- [ ] **Web Dashboard**
  - [ ] Create Streamlit app
  - [ ] Real-time portfolio tracking
  - [ ] Charts and analytics

- [ ] **Enhanced Analytics**
  - [ ] Technical indicators (RSI, MACD, Bollinger)
  - [ ] Portfolio optimization (Sharpe ratio)
  - [ ] Risk metrics (VaR, drawdown)

- [ ] **Backtesting**
  - [ ] Historical strategy testing
  - [ ] Performance comparison
  - [ ] Paper trading mode

### Data Sources

- [ ] **Indonesian Fundamentals**
  - [ ] Integrate StockBit API
  - [ ] PER, PBV, Dividend Yield data
  - [ ] Financial statements

- [ ] **Real-time Crypto**
  - [ ] Binance WebSocket connection
  - [ ] Live price updates
  - [ ] Order book data

- [ ] **Economic Calendar**
  - [ ] FRED API integration
  - [ ] Interest rate announcements
  - [ ] GDP/CPI data

### AI Improvements

- [ ] **Better Prompt Engineering**
  - [ ] System prompts for each analyst
  - [ ] Few-shot examples
  - [ ] Output format templates

- [ ] **Multi-Model Ensemble**
  - [ ] Combine signals from multiple models
  - [ ] Weighted voting system
  - [ ] Confidence aggregation

- [ ] **Local Models**
  - [ ] Ollama integration
  - [ ] Llama 3.1 70B (if hardware allows)
  - [ ] Smaller quantized models

### User Experience

- [ ] **Configuration**
  - [ ] `~/.ai-hedge-fund/config.yaml`
  - [ ] Default tickers
  - [ ] Preferred analysts
  - [ ] Output format settings

- [ ] **Notifications**
  - [ ] Email alerts (buy/sell signals)
  - [ ] Price alerts
  - [ ] Portfolio rebalancing reminders

- [ ] **Documentation**
  - [ ] API documentation
  - [ ] Agent prompt templates
  - [ ] Data source documentation

## ✅ Completed (v1.0.0)

- [x] Multi-asset support (Stocks, Forex, Crypto, Commodities)
- [x] OpenCode AI integration (grok-code, big-pickle, gpt-5-nano)
- [x] Interactive launcher
- [x] Multi-asset analysis script
- [x] Indonesian stock support (IDX)
- [x] Yahoo Finance integration
- [x] CoinGecko integration
- [x] exchangerate-api integration
- [x] README.md
- [x] BLUEPRINT.md
- [x] CHANGELOG.md

## 📝 Notes

### Symbols Used
- [ ] Todo
- [x] Completed
- 🔲 Future/Lower priority

### Priority Levels
1. 🔴 High - Blockers, must fix
2. 🟡 Medium - Important, should do
3. 🟢 Low - Nice to have

### Effort Estimation
- XS: < 1 hour
- S: 1-4 hours
- M: 1-2 days
- L: 1 week
- XL: 2+ weeks

---

**Last Updated**: 2026-01-14  
**Sprint Goal**: v1.1.0 - User Experience & Persistence

---

> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
>
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
