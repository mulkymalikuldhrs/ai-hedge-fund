# AI Quant Hedge Fund - Credits & Attribution

## Project Information
- **Project Name**: AI Quant Hedge Fund v2.0
- **Version**: 2.0.0
- **License**: MIT License
- **Repository**: https://github.com/mulkymalikuldhrs/ai-hedge-fund

---

## Lead Developer

### Mulky Malikul Dhaher
- **Role**: Lead Developer & Founder
- **Email**: mulkymalikuldhr@mail.com
- **GitHub**: [mulkymalikuldhrs](https://github.com/mulkymalikuldhrs)
- **Instagram**: [mulkymalikuldhr](https://instagram.com/mulkymalikuldhr)

---

## Data Sources

The AI Quant Hedge Fund uses the following data providers and APIs:

### 1. Yahoo Finance (yfinance)
- **Purpose**: Stock price data, historical OHLCV data
- **Website**: https://finance.yahoo.com
- **Python Package**: `yfinance`
- **License**: Apache 2.0
- **Attribution**: Data provided by Yahoo Finance

### 2. CoinGecko API
- **Purpose**: Cryptocurrency price data, market data
- **Website**: https://www.coingecko.com
- **API Documentation**: https://www.coingecko.com/en/api
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Attribution**: "Data provided by CoinGecko"
- **Rate Limits**: Free tier - 10-50 calls/minute

### 3. MetaTrader 5 (MT5)
- **Purpose**: Forex, CFD, and commodities trading data
- **Website**: https://www.metatrader5.com
- **Python Package**: `MetaTrader5`
- **License**: Proprietary (MetaQuotes Software)
- **Attribution**: "Data provided by MetaTrader 5"

### 4. Alpha Vantage
- **Purpose**: Stock API, technical indicators
- **Website**: https://www.alphavantage.co
- **API Documentation**: https://www.alphavantage.co/documentation
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Attribution**: "Data provided by Alpha Vantage"
- **API Key Required**: Free tier available

### 5. Binance API
- **Purpose**: Cryptocurrency exchange data
- **Website**: https://www.binance.com
- **API Documentation**: https://developers.binance.com
- **License**: Proprietary
- **Attribution**: "Data provided by Binance"

### 6. Forex Factory
- **Purpose**: Economic calendar, forex news
- **Website**: https://www.forexfactory.com
- **License**: Proprietary
- **Attribution**: "News and calendar from Forex Factory"

### 7. Investing.com
- **Purpose**: Market news, economic data
- **Website**: https://www.investing.com
- **License**: Proprietary
- **Attribution**: "Data provided by Investing.com"

---

## Third-Party Libraries & Dependencies

### Core Python Libraries
- **Python 3.9+** - Programming Language
- **pandas** - Data manipulation - BSD 3-Clause
- **numpy** - Numerical computing - BSD 3-Clause
- **requests** - HTTP requests - Apache 2.0

### Technical Analysis
- **TA-Lib** - Technical Analysis Library - BSD 3-Clause
- **pandas-ta** - Technical Analysis indicators - MIT License

### Machine Learning & AI
- **scikit-learn** - Machine Learning - BSD 3-Clause
- **xgboost** - Gradient Boosting - Apache 2.0
- **lightgbm** - Gradient Boosting - MIT License

### LLM & NLP
- **langchain** - LLM Framework - MIT License
- **openai** - OpenAI API client - MIT License
- **ollama** - Local LLM serving - MIT License

### Web Framework & UI
- **Dash** - Web application framework - MIT License
- **Plotly** - Interactive charts - MIT License
- **Streamlit** - Web dashboard - Apache 2.0
- **Textual** - Terminal UI framework - MIT License
- **Rich** - Terminal rich text - MIT License

### Trading
- **MetaTrader5** - MT5 Python binding - Proprietary
- **ccxt** - Cryptocurrency exchange library - MIT License

### Testing
- **pytest** - Testing framework - MIT License
- **pytest-asyncio** - Async testing - Apache 2.0

---

## Strategy References

The AI Quant Hedge Fund includes strategies inspired by:

### Retail & SMC (Smart Money Concepts) Strategies
- **ICT (Inner Circle Trader)** - Concepts from Michael Huddleston
- **Price Action Trading** - Concepts from Al Brooks
- **Order Block Theory** - SMC methodology
- **Liquidity Sweep Strategy** - SMC methodology
- **Fair Value Gap (FVG)** - SMC methodology

### Quantitative Strategies
- **Mean Reversion** - Academic research based
- **Momentum Trading** - Academic research based
- **Pairs Trading** - Statistical arbitrage
- **Grid Trading** - Systematic approach
- **Dollar Cost Averaging** - Investment methodology

### Legendary Investors Strategies
- **Warren Buffett** - Value investing philosophy
- **Benjamin Graham** - Security analysis
- **Peter Lynch** - Growth investing
- **Benjamin Graham** - Margin of safety
- **Michael Burry** - Value investing, behavioral finance
- **Charlie Munger** - Mental models
- **Bill Ackman** - Activist investing
- **Cathie Wood** - Innovation investing
- **Stanley Druckenmiller** - Macroeconomic trading
- **Mohnish Pabrai** - Clone investing

---

## Academic References

The system incorporates concepts from:

1. **Efficient Market Hypothesis** - Fama (1970)
2. **Modern Portfolio Theory** - Markowitz (1952)
3. **Capital Asset Pricing Model** - Sharpe (1964)
4. **Behavioral Finance** - Kahneman & Tversky
5. **Machine Learning in Finance** - Various research papers

---

## Open Source Projects Referenced

- **Freqtrade** - https://github.com/freqtrade/freqtrade
- **Backtrader** - https://github.com/mementum/backtrader
- **Zipline** - https://github.com/quantopian/zipline
- **QuantConnect Lean** - https://github.com/quantconnect/lean
- **FinRL** - https://github.com/AI4Finance-Foundation/FinRL
- **AutoTrader** - https://github.com/kieran-mackle/AutoTrader

---

## Documentation & Resources

### Books & Publications
- "Security Analysis" - Benjamin Graham & David Dodd
- "The Intelligent Investor" - Benjamin Graham
- "One Up On Wall Street" - Peter Lynch
- "Common Stocks and Uncommon Profits" - Philip Fisher
- "The Most Important Thing" - Howard Marks

### Online Resources
- Investopedia (https://www.investopedia.com)
- Khan Academy Finance (https://www.khanacademy.org/economics-finance-domain)
- MIT OpenCourseWare - Finance Theory

---

## API Keys Configuration

To use certain data providers, configure API keys:

```bash
# Create .env file
cp .env.example .env

# Add your API keys
ALPHA_VANTAGE_API_KEY=your_key
COINGECKO_API_KEY=your_key
```

### Obtaining API Keys
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key
- **CoinGecko**: Free API - no key required for basic usage
- **MT5**: Open account with supported broker

---

## Disclaimer

This software is for educational and research purposes only. Trading financial markets involves substantial risk of loss. The developers are not responsible for any financial losses incurred while using this software.

Past performance does not guarantee future results. Always test strategies thoroughly before live trading with real money.

---

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

### How to Contribute
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Contact

### Mulky Malikul Dhaher
- **Email**: mulkymalikuldhr@mail.com
- **GitHub**: https://github.com/mulkymalikuldhrs
- **Instagram**: https://instagram.com/mulkymalikuldhr

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01-16 | Added live trading terminal, MT5 integration, portfolio models |
| 1.2.0 | 2026-01-10 | Added 34 strategies, multi-agent system |
| 1.0.0 | 2026-01-01 | Initial release |

---

*Last Updated: 2026-01-16*
*Document Version: 2.0.0*
