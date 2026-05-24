# AI Hedge Fund - Project Memory

## 📚 Context

This document captures the key decisions, lessons learned, and important context for the AI Hedge Fund project. It serves as a "memory" for future development.

---

## 🎯 Project Vision

Create a **FREE**, AI-powered trading system that supports:
- Multiple asset classes (Stocks, Forex, Crypto, Commodities)
- Multiple investment strategies (Buffett, Burry, Wood, etc.)
- No paid API subscriptions required

---

## 💡 Key Decisions

### 1. OpenCode as Primary LLM (2026-01-14)

**Decision**: Use OpenCode CLI instead of paid APIs

**Reasoning**:
- OpenCode CLI (`opencode run --model opencode/grok-code`) is FREE
- No API key needed
- Works offline (once installed)
- Multiple free models available

**Alternatives Considered**:
- Groq API: Requires API key, keys from credential.txt didn't work
- Puter SDK: Requires API key
- Anthropic/OpenAI: Paid APIs

**Trade-offs**:
- ✅ No cost
- ✅ No authentication issues
- ❌ Slower than API-based solutions
- ❌ Limited control over parameters

**Implementation**: Created `src/llm/models.py::OpenCodeChatModel` wrapper

---

### 2. Yahoo Finance for Stock Data (2026-01-14)

**Decision**: Use `yfinance` library for all stock data

**Reasoning**:
- Completely free
- No API key required
- Works for US and international stocks
- Historical data available

**Indonesian Stock Format**:
- Ticker: `BBCA` → Yahoo: `BBCA.JK`
- Automatically appends `.JK` suffix for IDX stocks

**Trade-offs**:
- ✅ Free, reliable
- ❌ Slight data delays
- ❌ Rate limiting on high-volume requests

---

### 3. Multi-Asset Architecture (2026-01-14)

**Decision**: Unified `multi_asset_api.py` instead of separate modules

**Reasoning**:
- Consistent API across asset types
- Easier to maintain
- Auto-detection of asset type

**Asset Type Detection**:
```python
if ticker.endswith('.JK') → stock_idx
if '/' in ticker → forex  
if ticker in ['BTC', 'ETH', ...] → crypto
else → stock_us
```

---

## 🔧 Technical Implementation

### OpenCodeChatModel Wrapper

**File**: `src/llm/models.py`

```python
class OpenCodeChatModel:
    def __init__(self, model: str = "opencode/grok-code"):
        self.model = model
    
    def with_structured_output(self, pydantic_model):
        # Returns wrapper with JSON handling
    
    def invoke(self, input_data):
        # Calls: opencode run --model <model>
        # Parses response
        # Returns structured output
```

**Key Features**:
- Fallback to default values on JSON parse failure
- Regex-based JSON extraction from text
- Automatic retry on failure

### Multi-Asset Data Flow

```
User Input (tickers)
    ↓
Auto-detect asset type
    ↓
Fetch prices (Yahoo/CoinGecko/Binance)
    ↓
Generate AI prompt with price data
    ↓
OpenCode LLM analysis
    ↓
Parse JSON response
    ↓
Display results
```

---

## 📊 Supported Assets

### Indonesian Stocks (IDX)

| Ticker | Name | Yahoo Format |
|--------|------|--------------|
| BBCA | Bank Central Asia | BBCA.JK |
| BBRI | Bank Rakyat Indonesia | BBRI.JK |
| BMRI | Bank Mandiri | BMRI.JK |
| TLKM | Telkom Indonesia | TLKM.JK |
| UNVR | Unilever Indonesia | UNVR.JK |

**Data Source**: Yahoo Finance

### US Stocks

| Ticker | Name |
|--------|------|
| AAPL | Apple Inc. |
| MSFT | Microsoft Corp. |
| NVDA | NVIDIA Corp. |
| GOOGL | Alphabet Inc. |

**Data Source**: Yahoo Finance

### Forex

| Pair | Rate Source | Status |
|------|-------------|--------|
| USD/IDR | exchangerate-api.com | ✅ |
| EUR/USD | exchangerate-api.com | ✅ |
| Major pairs | exchangerate-api.com | ✅ |

**API**: https://open.er-api.com/v6/latest/USD (NO KEY REQUIRED)

### Cryptocurrencies

| Coin | Data Source |
|------|-------------|
| BTC | CoinGecko Historical |
| ETH | CoinGecko Historical |
| SOL | CoinGecko Historical |
| Altcoins | CoinGecko API |

**APIs**:
- Historical: https://api.coingecko.com/api/v3
- Spot: https://api.binance.com/api/v3

### Commodities

| Commodity | Yahoo Ticker |
|-----------|--------------|
| Gold | GC=F |
| Silver | SI=F |
| Oil | CL=F |

**Data Source**: Yahoo Finance Futures

---

## 🤖 AI Agents

### Available Agents

1. **Warren Buffett** - Value investing, long-term fundamentals
2. **Michael Burry** - Deep value, contrarian, spotting bubbles
3. **Cathie Wood** - Growth, innovation, disruption
4. **Ben Graham** - Defensive value, margin of safety
5. **Peter Lynch** - GARP (Growth at Reasonable Price)
6. **Howard Marks** - Risk management, market cycles
7. **Ray Dalio** - Macroeconomic analysis

### Agent Selection

```bash
# Single analyst
--analysts warren_buffett

# Multiple analysts  
--analysts warren_buffett,cathie_wood

# All analysts
--analysts-all
```

---

## 🐛 Known Issues

### 1. AI JSON Parsing

**Issue**: OpenCode models don't always return valid JSON

**Workaround**: Fallback to default values
```python
try:
    parsed = json.loads(response)
    return pydantic_model(**parsed)
except:
    return self._get_default_response()
```

**Status**: Mitigated, but not fully resolved

### 2. Portfolio Manager Validation Error

**Issue**: `PortfolioManagerOutput.decisions` field required but not returned

**Workaround**: Default to empty decisions
```python
return create_default_response(pydantic_model)
```

**Status**: Needs fix in `src/agents/portfolio_manager.py`

### 3. Crypto Historical Data

**Issue**: CoinGecko rate limiting on historical data

**Workaround**: Catch exception, return empty list

**Status**: Monitor, may need caching

---

## 📝 Lessons Learned

### 1. Free APIs Have Limitations

**Lesson**: "Free" doesn't mean unlimited or reliable

**Action**:
- Implement caching
- Add rate limiting
- Have fallback sources

### 2. LLM Output is Unpredictable

**Lesson**: Don't assume AI will return JSON

**Action**:
- Always have fallbacks
- Validate outputs
- Use structured output wrappers

### 3. Indonesian Market is Unique

**Lesson**: IDX has different ticker format (.JK suffix)

**Action**:
- Auto-detect and append suffix
- Support IDR currency formatting
- Track IHSG as market benchmark

---

## 🔐 Credentials

**Note**: All credentials stored in `credential.txt` on Desktop

### Working Credentials
- None required for core functionality (OpenCode, Yahoo Finance, CoinGecko)

### Previously Tested (Failed)
- Groq API key (invalid/expired)
- DeepSeek API key (invalid)
- OpenRouter API keys (authentication failed)

---

## 🚀 Future Enhancements (Ideas)

1. **Telegram Bot** - Get signals via messaging app
2. **Web Dashboard** - Streamlit-based UI
3. **Backtesting** - Test strategies on historical data
4. **Paper Trading** - Simulate with fake money
5. **Portfolio Optimization** - Modern Portfolio Theory
6. **Technical Analysis** - RSI, MACD, Bollinger Bands
7. **Social Features** - Share portfolios with friends

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `launcher.py` | Interactive CLI entry point |
| `run_multi_asset.py` | Multi-asset analysis script |
| `src/llm/models.py` | LLM provider integration |
| `src/tools/multi_asset_api.py` | Data fetching |
| `src/agents/*.py` | AI analyst implementations |
| `pyproject.toml` | Dependencies |
| `.env` | Environment configuration |

---

## 🏃 Running the Project

### Quick Start
```bash
cd /home/mulky/ai-hedge-fund
python launcher.py
```

### Single Stock Analysis
```bash
python run_multi_asset.py --tickers BBCA --type stock_idx
```

### Full AI Analysis
```bash
poetry run python src/main.py --tickers AAPL --analysts-all --model opencode/grok-code
```

---

## 📞 Support & Resources

- **OpenCode CLI**: https://opencode.ai/
- **yFinance**: https://pypi.org/project/yfinance/
- **CoinGecko API**: https://www.coingecko.com/
- **exchangerate-api**: https://open.er-api.com/

---

**Memory Last Updated**: 2026-01-14  
**Memory Version**: 1.0

---

> **Contact:** Mulky Malikul Dhaher — [mulkymalikuldhaher@email.com](mailto:mulkymalikuldhaher@email.com)
>
> **Disclaimer:** This project is for Education Purpose only. Risiko apapun tidak kita tanggung. (We are not responsible for any risks or damages.)
