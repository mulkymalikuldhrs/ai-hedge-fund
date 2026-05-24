# AI Hedge Fund Blueprint

## 📋 Project Overview

**Name**: AI Hedge Fund - Multi-Asset Trading System  
**Version**: 1.0.0  
**Status**: MVP Complete  
**Last Updated**: 2026-01-14

## 🎯 Vision

Build a comprehensive, free AI-powered trading system that supports multiple asset classes without requiring paid API subscriptions.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI HEDGE FUND SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 1: User Interface                                        │
│  ├── launcher.py (Interactive CLI)                              │
│  ├── run_multi_asset.py (Multi-asset script)                   │
│  └── src/main.py (Original AI Hedge Fund CLI)                  │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 2: Orchestration                                         │
│  ├── Agent Management (Warren Buffett, Burry, Wood, etc.)      │
│  ├── LLM Integration (OpenCode, Groq, Google, etc.)            │
│  └── Workflow Engine (LangGraph)                                │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 3: Data Layer                                            │
│  ├── Multi-Asset API (Yahoo Finance, CoinGecko, Binance)       │
│  ├── Financial Datasets API                                     │
│  └── Cache System                                               │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 4: Infrastructure                                        │
│  ├── Poetry (Dependency Management)                             │
│  ├── Python 3.11+                                               │
│  └── Environment Configuration (.env)                           │
└─────────────────────────────────────────────────────────────────┘
```

## 📦 Current Features (v1.0.0)

### ✅ Completed

- [x] Multi-asset data support
  - [x] US Stocks (Yahoo Finance)
  - [x] Indonesian Stocks IDX (Yahoo Finance + IDX API)
  - [x] Forex (exchangerate-api.com)
  - [x] Cryptocurrencies (CoinGecko + Binance)
  - [x] Commodities (Yahoo Finance)
  - [x] Market Indices (Yahoo Finance)

- [x] AI Integration
  - [x] OpenCode CLI integration (FREE!)
  - [x] OpenCode/grok-code model
  - [x] OpenCode/big-pickle model
  - [x] OpenCode/gpt-5-nano model
  - [x] Structured output support

- [x] AI Agents
  - [x] Warren Buffett (Value Investing)
  - [x] Michael Burry (Contrarian/Deep Value)
  - [x] Cathie Wood (Growth/Innovation)
  - [x] Additional agents from original system

- [x] User Interface
  - [x] Interactive launcher (launcher.py)
  - [x] Multi-asset analysis script
  - [x] Color-coded output
  - [x] Portfolio summary

- [x] Documentation
  - [x] README.md
  - [x] This Blueprint
  - [x] Inline code comments

## 🚀 Planned Features (v1.1.0)

### High Priority

- [ ] **Enhanced AI Analysis**
  - [ ] Better JSON parsing for structured output
  - [ ] Fallback to non-structured output
  - [ ] Confidence scoring improvements

- [ ] **Data Sources**
  - [ ] Indonesian stock fundamentals (StockBit API)
  - [ ] Real-time crypto prices (Binance WebSocket)
  - [ ] Economic calendar data

- [ ] **User Experience**
  - [ ] Save/load portfolios
  - [ ] Export to CSV/JSON
  - [ ] Telegram bot integration
  - [ ] Web dashboard (Streamlit)

### Medium Priority

- [ ] **Advanced Analytics**
  - [ ] Technical indicators (RSI, MACD, Bollinger Bands)
  - [ ] Portfolio optimization
  - [ ] Backtesting module

- [ ] **More AI Models**
  - [ ] Groq integration (if API key works)
  - [ ] Local models (Ollama)
  - [ ] Claude via Anthropic API

### Lower Priority

- [ ] **Social Features**
  - [ ] Share portfolios
  - [ ] Community signals
  - [ ] Copy trading

- [ ] **Mobile**
  - [ ] iOS/Android app
  - [ ] Push notifications

## 📊 Asset Classes

### Stocks

| Market | Source | Ticker Format | Status |
|--------|--------|---------------|--------|
| US | Yahoo Finance | AAPL, MSFT | ✅ Done |
| Indonesia | Yahoo Finance | BBCA.JK | ✅ Done |
| Others | Yahoo Finance | 6789.T (JP) | 🔲 Future |

### Forex

| Pair | Source | Status |
|------|--------|--------|
| USD/IDR | exchangerate-api.com | ✅ Done |
| Major pairs | exchangerate-api.com | ✅ Done |
| Exotic pairs | ForexRateAPI | 🔲 Future |

### Crypto

| Source | Status |
|--------|--------|
| CoinGecko (Historical) | ✅ Done |
| Binance (Spot) | ✅ Done |
| Binance WebSocket | 🔲 Future |
| DEX APIs | 🔲 Future |

### Commodities

| Commodity | Source | Status |
|-----------|--------|--------|
| Gold | Yahoo Finance | ✅ Done |
| Oil | Yahoo Finance | ✅ Done |
| Others | Yahoo Finance | ✅ Done |

## 🤖 AI Models

| Provider | Model | Cost | Status |
|----------|-------|------|--------|
| OpenCode | grok-code | FREE | ✅ Done |
| OpenCode | big-pickle | FREE | ✅ Done |
| OpenCode | gpt-5-nano | FREE | ✅ Done |
| Groq | llama-3.3-70b | Free tier | 🔲 Needs key |
| Google | gemini-2.5-pro | Free tier | 🔲 Needs key |

## 📁 File Structure

```
ai-hedge-fund/
├── src/
│   ├── main.py              # Entry point (original)
│   ├── agents/              # AI agent implementations
│   │   ├── warren_buffett.py
│   │   ├── michael_burry.py
│   │   ├── cathie_wood.py
│   │   └── ... (10+ agents)
│   ├── tools/
│   │   ├── api.py           # Financial APIs
│   │   └── multi_asset_api.py # Multi-asset data
│   ├── llm/
│   │   ├── models.py        # LLM providers
│   │   └── opencode_client.py # OpenCode wrapper
│   ├── cli/                 # CLI utilities
│   ├── graph/               # LangGraph workflows
│   └── utils/               # Helpers
├── run_multi_asset.py       # Multi-asset analysis
├── launcher.py              # Interactive launcher
├── pyproject.toml           # Dependencies
├── .env                     # Environment
├── README.md                # Main docs
├── BLUEPRINT.md             # This file
└── docs/
    ├── CHANGELOG.md
    └── ... (additional docs)
```

## 🔧 Technology Stack

| Category | Technology | Version |
|----------|------------|---------|
| Language | Python | 3.11+ |
| Package Manager | Poetry | Latest |
| AI Framework | LangGraph | 0.2.x |
| AI Models | OpenCode CLI | 1.1.x |
| Data (Stocks) | yFinance | 1.0.x |
| Data (Crypto) | CoinGecko API | - |
| Data (Forex) | exchangerate-api | - |
| CLI | Questionary | 2.x |
| Output | Rich + Colorama | - |

## 📈 Performance Goals

| Metric | Target | Current |
|--------|--------|---------|
| Analysis Time | < 30s per asset | ~10-20s |
| Memory Usage | < 500MB | ~200MB |
| API Success Rate | > 95% | ~90% |
| AI Response Accuracy | > 80% | TBD |

## 🧪 Testing Strategy

### Unit Tests
- [ ] Data fetching tests
- [ ] LLM integration tests
- [ ] Agent logic tests

### Integration Tests
- [ ] Full workflow test
- [ ] Multi-asset test
- [ ] Error handling test

### Manual Tests
- [ ] CLI interface test
- [ ] Output formatting test
- [ ] User experience test

## 📝 Changelog

See `docs/CHANGELOG.md` for detailed history.

## 🔒 Security Considerations

- API keys stored in `.env` (not committed)
- No sensitive data in logs
- Rate limiting to prevent API bans
- Input validation on all user inputs

## 🎓 Learning Outcomes

1. **Multi-source data integration**: Combining Yahoo Finance, CoinGecko, Binance, IDX
2. **AI agent design**: Multiple investment strategies
3. **LLM integration**: OpenCode CLI as free alternative
4. **CLI design**: Interactive user experience
5. **Project structure**: Clean architecture with Poetry

## 📚 References

- [OpenCode Docs](https://opencode.ai/docs/cli/)
- [yFinance](https://pypi.org/project/yfinance/)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [LangChain](https://python.langchain.com/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - See LICENSE file

---

**Blueprint Version**: 1.0  
**Last Modified**: 2026-01-14  
**Next Review**: 2026-02-14

---

> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
>
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
