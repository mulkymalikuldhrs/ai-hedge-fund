"""
Free Data Sources Integration for AI Hedge Fund v2.2
=====================================================

Provides FREE data sources without API keys:
- Yahoo Finance: Stocks, ETFs, Indices
- CoinGecko: Cryptocurrency data
- exchangerate-api: Forex rates
- yfinance: Market data (no API key required)

Usage:
    from src.data.free_data_provider import get_free_data_provider
    data = get_free_data_provider()
    df = data.get_historical_data("AAPL", days=365)
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from abc import ABC, abstractmethod
import time
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssetType(Enum):
    STOCK = "stock"
    FOREX = "forex"
    CRYPTO = "crypto"
    COMMODITY = "commodity"
    INDEX = "index"
    ETF = "etf"
    BOND = "bond"


class DataSource(Enum):
    YAHOO = "yahoo"
    COINGECKO = "coingecko"
    EXCHANGERATE = "exchangerate"
    MANUAL = "manual"


@dataclass
class OHLCV:
    """OHLCV data structure"""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "OHLCV":
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            open=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            close=float(data["close"]),
            volume=float(data["volume"]),
        )


@dataclass
class MarketData:
    """Market data container"""

    symbol: str
    asset_type: str
    current_price: float
    daily_change: float
    daily_change_pct: float
    high_24h: float
    low_24h: float
    volume_24h: float
    market_cap: float = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "asset_type": self.asset_type,
            "current_price": self.current_price,
            "daily_change": self.daily_change,
            "daily_change_pct": self.daily_change_pct,
            "high_24h": self.high_24h,
            "low_24h": self.low_24h,
            "volume_24h": self.volume_24h,
            "market_cap": self.market_cap,
            "last_updated": self.last_updated.isoformat(),
        }


class BaseDataProvider(ABC):
    """Abstract base class for data providers"""

    @abstractmethod
    def get_historical_data(
        self, symbol: str, days: int = 365, interval: str = "1d"
    ) -> List[OHLCV]:
        pass

    @abstractmethod
    def get_current_price(self, symbol: str) -> MarketData:
        pass

    @abstractmethod
    def get_supported_symbols(self) -> List[str]:
        pass


class YahooFinanceProvider(BaseDataProvider):
    """Yahoo Finance data provider (FREE - no API key)"""

    def __init__(self):
        try:
            import yfinance as yf

            self.yf = yf
            logger.info("Yahoo Finance provider initialized")
        except ImportError:
            logger.error("yfinance not installed. Install with: pip install yfinance")
            raise ImportError("yfinance required for Yahoo Finance provider")

    def get_historical_data(
        self, symbol: str, days: int = 365, interval: str = "1d"
    ) -> List[OHLCV]:
        """Get historical OHLCV data from Yahoo Finance"""
        try:
            ticker = self.yf.Ticker(symbol)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            df = ticker.history(start=start_date, end=end_date, interval=interval)

            if df.empty:
                logger.warning(f"No data for {symbol}")
                return []

            ohlcv_list = []
            for idx, row in df.iterrows():
                ohlcv = OHLCV(
                    timestamp=idx.to_pydatetime(),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=float(row["Volume"]) if pd.notna(row["Volume"]) else 0.0,
                )
                ohlcv_list.append(ohlcv)

            logger.info(f"Retrieved {len(ohlcv_list)} data points for {symbol}")
            return ohlcv_list

        except Exception as e:
            logger.error(f"Error fetching Yahoo data for {symbol}: {e}")
            return []

    def get_current_price(self, symbol: str) -> MarketData:
        """Get current market data from Yahoo Finance"""
        try:
            ticker = self.yf.Ticker(symbol)
            info = ticker.info

            current_price = (
                info.get("currentPrice") or info.get("regularMarketPrice") or 0
            )
            prev_close = (
                info.get("previousClose")
                or info.get("regularMarketPreviousClose")
                or current_price
            )
            daily_change = current_price - prev_close
            daily_change_pct = (daily_change / prev_close * 100) if prev_close else 0

            market_data = MarketData(
                symbol=symbol,
                asset_type=AssetType.STOCK.value,
                current_price=current_price,
                daily_change=daily_change,
                daily_change_pct=daily_change_pct,
                high_24h=info.get("dayHigh") or current_price,
                low_24h=info.get("dayLow") or current_price,
                volume_24h=info.get("volume") or 0,
                market_cap=info.get("marketCap") or 0,
            )

            return market_data

        except Exception as e:
            logger.error(f"Error fetching current price for {symbol}: {e}")
            return MarketData(
                symbol=symbol,
                asset_type=AssetType.STOCK.value,
                current_price=0,
                daily_change=0,
                daily_change_pct=0,
                high_24h=0,
                low_24h=0,
                volume_24h=0,
            )
            prev_close = (
                info.get("previousClose")
                or info.get("regularMarketPreviousClose")
                or current_price
            )
            daily_change = current_price - prev_close
            daily_change_pct = (daily_change / prev_close * 100) if prev_close else 0

            market_data = MarketData(
                symbol=symbol,
                asset_type=AssetType.STOCK.value,
                current_price=current_price,
                daily_change=daily_change,
                daily_change_pct=daily_change_pct,
                high_24h=info.get("dayHigh") or current_price,
                low_24h=info.get("dayLow") or current_price,
                volume_24h=info.get("volume") or 0,
                market_cap=info.get("marketCap") or 0,
            )

            return market_data

        except Exception as e:
            logger.error(f"Error fetching current price for {symbol}: {e}")
            return MarketData(
                symbol=symbol,
                asset_type=AssetType.STOCK.value,
                current_price=0,
                daily_change=0,
                daily_change_pct=0,
                high_24h=0,
                low_24h=0,
                volume_24h=0,
            )

    def get_supported_symbols(self) -> List[str]:
        """Get list of supported stock symbols"""
        return [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "NVDA",
            "TSLA",
            "JPM",
            "V",
            "JNJ",
            "WMT",
            "PG",
            "MA",
            "UNH",
            "HD",
            "DIS",
            "BAC",
            "ADBE",
            "CRM",
            "NFLX",
            "PFE",
            "TMO",
            "COST",
            "ABBV",
            "ACN",
            "MCD",
            "DHR",
            "AVGO",
            "NKE",
            "MRK",
            "PEP",
            "KO",
            "AMD",
            "INTC",
            "CSCO",
            "QCOM",
            "TXN",
            "AMAT",
            "MU",
            "LRCX",
            "EURUSD=X",
            "GBPUSD=X",
            "USDJPY=X",
            "AUDUSD=X",
            "USDCAD=X",
            "USDCHF=X",
            "^GSPC",
            "^DJI",
            "^IXIC",
            "^RUT",
            "^VIX",
        ]


class CoinGeckoProvider(BaseDataProvider):
    """CoinGecko cryptocurrency data provider (FREE tier)"""

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        logger.info("CoinGecko provider initialized")

    def get_historical_data(
        self, symbol: str, days: int = 365, interval: str = "1d"
    ) -> List[OHLCV]:
        """Get historical OHLCV data from CoinGecko"""
        coin_id = self._symbol_to_coin_id(symbol)
        if not coin_id:
            return []

        try:
            import requests

            url = f"{self.BASE_URL}/coins/{coin_id}/market_chart"
            params = {"vs_currency": "usd", "days": days, "interval": "daily"}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "prices" not in data:
                return []

            ohlcv_list = []
            for i, (timestamp, price) in enumerate(data["prices"]):
                market_caps = data.get("market_caps", [])
                volumes = data.get("total_volumes", [])

                open_price = (
                    data["prices"][0][1]
                    if i == 0
                    else data["prices"][i - 1][1]
                    if i > 0
                    else price
                )
                high = price
                low = price
                volume = volumes[i][1] if i < len(volumes) else 0

                for j in range(max(0, i - 23), min(i + 1, len(data["prices"]))):
                    p = data["prices"][j][1]
                    high = max(high, p)
                    low = min(low, p)

                ohlcv = OHLCV(
                    timestamp=datetime.fromtimestamp(timestamp / 1000),
                    open=open_price,
                    high=high,
                    low=low,
                    close=price,
                    volume=volume,
                )
                ohlcv_list.append(ohlcv)

            return ohlcv_list

        except Exception as e:
            logger.error(f"Error fetching CoinGecko data for {symbol}: {e}")
            return []

    def get_current_price(self, symbol: str) -> MarketData:
        """Get current cryptocurrency data from CoinGecko"""
        coin_id = self._symbol_to_coin_id(symbol)
        if not coin_id:
            return MarketData(
                symbol=symbol,
                asset_type=AssetType.CRYPTO.value,
                current_price=0,
                daily_change=0,
                daily_change_pct=0,
                high_24h=0,
                low_24h=0,
                volume_24h=0,
            )

        try:
            import requests

            url = f"{self.BASE_URL}/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_24hr_high": "true",
                "include_24hr_low": "true",
                "include_24hr_vol": "true",
                "include_market_cap": "true",
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if coin_id not in data:
                return MarketData(
                    symbol=symbol,
                    asset_type=AssetType.CRYPTO.value,
                    current_price=0,
                    daily_change=0,
                    daily_change_pct=0,
                    high_24h=0,
                    low_24h=0,
                    volume_24h=0,
                )

            coin_data = data[coin_id]
            current_price = coin_data.get("usd", 0)
            change_24h = coin_data.get("usd_24h_change", 0)
            daily_change = current_price * (change_24h / 100)

            return MarketData(
                symbol=symbol,
                asset_type=AssetType.CRYPTO.value,
                current_price=current_price,
                daily_change=daily_change,
                daily_change_pct=change_24h,
                high_24h=coin_data.get("usd_24h_high", current_price),
                low_24h=coin_data.get("usd_24h_low", current_price),
                volume_24h=coin_data.get("usd_24h_vol", 0),
                market_cap=coin_data.get("usd_market_cap", 0),
            )

        except Exception as e:
            logger.error(f"Error fetching CoinGecko price for {symbol}: {e}")
            return MarketData(
                symbol=symbol,
                asset_type=AssetType.CRYPTO.value,
                current_price=0,
                daily_change=0,
                daily_change_pct=0,
                high_24h=0,
                low_24h=0,
                volume_24h=0,
            )

    def _symbol_to_coin_id(self, symbol: str) -> Optional[str]:
        """Convert symbol to CoinGecko coin ID"""
        symbol_lower = symbol.lower().replace("/", "").replace("-", "")

        coin_mapping = {
            "btc": "bitcoin",
            "btcusd": "bitcoin",
            "btc/usd": "bitcoin",
            "eth": "ethereum",
            "ethusd": "ethereum",
            "eth/usd": "ethereum",
            "sol": "solana",
            "solusd": "solana",
            "sol/usd": "solana",
            "xrp": "ripple",
            "xrpusd": "ripple",
            "xrp/usd": "ripple",
            "ada": "cardano",
            "adausd": "cardano",
            "ada/usd": "cardano",
            "dot": "polkadot",
            "dotusd": "polkadot",
            "dot/usd": "polkadot",
            "doge": "dogecoin",
            "dogeusd": "dogecoin",
            "doge/usd": "dogecoin",
            "link": "chainlink",
            "linkusd": "chainlink",
            "link/usd": "chainlink",
            "avax": "avalanche-2",
            "avaxusd": "avalanche-2",
            "avax/usd": "avalanche-2",
            "matic": "matic-network",
            "maticusd": "matic-network",
            "matic/usd": "matic-network",
            "uni": "uniswap",
            "uniusd": "uniswap",
            "uni/usd": "uniswap",
            "atom": "cosmos",
            "atomusd": "cosmos",
            "atom/usd": "cosmos",
        }

        return coin_mapping.get(symbol_lower)

    def get_supported_symbols(self) -> List[str]:
        """Get list of supported cryptocurrency symbols"""
        return [
            "BTC",
            "BTC/USD",
            "BTCUSDT",
            "ETH",
            "ETH/USD",
            "ETHUSDT",
            "SOL",
            "SOL/USD",
            "SOLUSDT",
            "XRP",
            "XRP/USD",
            "XRPUSDT",
            "ADA",
            "ADA/USD",
            "ADAUSDT",
            "DOT",
            "DOT/USD",
            "DOTUSDT",
            "DOGE",
            "DOGE/USD",
            "DOGEUSDT",
            "LINK",
            "LINK/USD",
            "LINKUSDT",
            "AVAX",
            "AVAX/USD",
            "AVAXUSDT",
            "MATIC",
            "MATIC/USD",
            "MATICUSDT",
            "UNI",
            "UNI/USD",
            "UNIUSDT",
            "ATOM",
            "ATOM/USD",
            "ATOMUSDT",
        ]


class ExchangeRateProvider(BaseDataProvider):
    """Exchange rate data provider (FREE tier)"""

    BASE_URL = "https://api.exchangerate-api.com/v4"

    def __init__(self):
        logger.info("ExchangeRate provider initialized")

    def get_historical_data(
        self, symbol: str, days: int = 365, interval: str = "1d"
    ) -> List[OHLCV]:
        """Get historical exchange rate data"""
        try:
            import requests

            base, quote = self._parse_forex_pair(symbol)
            if not base or not quote:
                return []

            ohlcv_list = []
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")

                try:
                    url = f"{self.BASE_URL}/{date_str}"
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    data = response.json()

                    if base in data["rates"] and quote in data["rates"]:
                        base_rate = data["rates"][base]
                        quote_rate = data["rates"][quote]
                        price = quote_rate / base_rate

                        ohlcv = OHLCV(
                            timestamp=current_date,
                            open=price,
                            high=price,
                            low=price,
                            close=price,
                            volume=0,
                        )
                        ohlcv_list.append(ohlcv)

                except Exception:
                    pass

                current_date += timedelta(days=1)
                time.sleep(0.2)

            return ohlcv_list

        except Exception as e:
            logger.error(f"Error fetching exchange rate data for {symbol}: {e}")
            return []

    def get_current_price(self, symbol: str) -> MarketData:
        """Get current exchange rate"""
        try:
            import requests

            base, quote = self._parse_forex_pair(symbol)
            if not base or not quote:
                return MarketData(
                    symbol=symbol,
                    asset_type=AssetType.FOREX.value,
                    current_price=0,
                    daily_change=0,
                    daily_change_pct=0,
                    high_24h=0,
                    low_24h=0,
                    volume_24h=0,
                )

            url = f"{self.BASE_URL}/latest/{base}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            rate = data["rates"].get(quote, 0)

            return MarketData(
                symbol=symbol,
                asset_type=AssetType.FOREX.value,
                current_price=rate,
                daily_change=0,
                daily_change_pct=0,
                high_24h=rate,
                low_24h=rate,
                volume_24h=0,
            )

        except Exception as e:
            logger.error(f"Error fetching exchange rate for {symbol}: {e}")
            return MarketData(
                symbol=symbol,
                asset_type=AssetType.FOREX.value,
                current_price=0,
                daily_change=0,
                daily_change_pct=0,
                high_24h=0,
                low_24h=0,
                volume_24h=0,
            )

    def _parse_forex_pair(self, symbol: str) -> Tuple[str, str]:
        """Parse forex pair symbol"""
        symbol_upper = symbol.upper()

        if "=" in symbol_upper:
            parts = symbol_upper.split("=")
            return parts[0], parts[1]

        if "/" in symbol_upper:
            parts = symbol_upper.split("/")
            return parts[0], parts[1]

        common_pairs = {
            "EURUSD": ("EUR", "USD"),
            "GBPUSD": ("GBP", "USD"),
            "USDJPY": ("USD", "JPY"),
            "AUDUSD": ("AUD", "USD"),
            "USDCAD": ("USD", "CAD"),
            "USDCHF": ("USD", "CHF"),
            "NZDUSD": ("NZD", "USD"),
            "EURGBP": ("EUR", "GBP"),
            "EURJPY": ("EUR", "JPY"),
            "GBPJPY": ("GBP", "JPY"),
        }

        return common_pairs.get(symbol_upper, (None, None))

    def get_supported_symbols(self) -> List[str]:
        """Get list of supported forex symbols"""
        return [
            "EURUSD",
            "GBPUSD",
            "USDJPY",
            "AUDUSD",
            "USDCAD",
            "USDCHF",
            "NZDUSD",
            "EURGBP",
            "EURJPY",
            "GBPJPY",
            "EURUSD=X",
            "GBPUSD=X",
        ]


class FreeDataProvider:
    """Unified FREE data provider"""

    _instance = None
    _providers = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_providers()
        return cls._instance

    def _initialize_providers(self):
        """Initialize all data providers"""
        try:
            self._providers[DataSource.YAHOO] = YahooFinanceProvider()
        except ImportError:
            logger.warning("Yahoo Finance provider not available")

        try:
            self._providers[DataSource.COINGECKO] = CoinGeckoProvider()
        except Exception as e:
            logger.warning(f"CoinGecko provider not available: {e}")

        try:
            self._providers[DataSource.EXCHANGERATE] = ExchangeRateProvider()
        except Exception as e:
            logger.warning(f"ExchangeRate provider not available: {e}")

    def get_historical_data(
        self, symbol: str, days: int = 365, interval: str = "1d"
    ) -> List[OHLCV]:
        """Get historical data using best available provider"""
        symbol_upper = symbol.upper()

        if (
            symbol_upper.endswith("=X")
            or "/" in symbol_upper
            or symbol_upper in ["EURUSD", "GBPUSD", "USDJPY"]
        ):
            provider = self._providers.get(DataSource.EXCHANGERATE)
            if provider:
                return provider.get_historical_data(symbol, days, interval)

        crypto_symbols = [
            "BTC",
            "ETH",
            "SOL",
            "XRP",
            "ADA",
            "DOT",
            "DOGE",
            "LINK",
            "AVAX",
            "MATIC",
            "UNI",
            "ATOM",
        ]
        if any(sym in symbol_upper for sym in crypto_symbols):
            provider = self._providers.get(DataSource.COINGECKO)
            if provider:
                return provider.get_historical_data(symbol, days, interval)

        provider = self._providers.get(DataSource.YAHOO)
        if provider:
            return provider.get_historical_data(symbol, days, interval)

        logger.error("No data provider available")
        return []

    def get_current_price(self, symbol: str) -> MarketData:
        """Get current price using best available provider"""
        symbol_upper = symbol.upper()

        if (
            symbol_upper.endswith("=X")
            or "/" in symbol_upper
            or symbol_upper in ["EURUSD", "GBPUSD", "USDJPY"]
        ):
            provider = self._providers.get(DataSource.EXCHANGERATE)
            if provider:
                return provider.get_current_price(symbol)

        crypto_symbols = [
            "BTC",
            "ETH",
            "SOL",
            "XRP",
            "ADA",
            "DOT",
            "DOGE",
            "LINK",
            "AVAX",
            "MATIC",
            "UNI",
            "ATOM",
        ]
        if any(sym in symbol_upper for sym in crypto_symbols):
            provider = self._providers.get(DataSource.COINGECKO)
            if provider:
                return provider.get_current_price(symbol)

        provider = self._providers.get(DataSource.YAHOO)
        if provider:
            return provider.get_current_price(symbol)

        return MarketData(
            symbol=symbol,
            asset_type="unknown",
            current_price=0,
            daily_change=0,
            daily_change_pct=0,
            high_24h=0,
            low_24h=0,
            volume_24h=0,
        )

    def get_all_prices(self, symbols: List[str]) -> Dict[str, MarketData]:
        """Get current prices for multiple symbols"""
        prices = {}
        for symbol in symbols:
            try:
                price = self.get_current_price(symbol)
                prices[symbol] = price
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error fetching price for {symbol}: {e}")
        return prices

    def get_supported_symbols(self) -> List[str]:
        """Get all supported symbols"""
        symbols = set()
        for provider in self._providers.values():
            symbols.update(provider.get_supported_symbols())
        return sorted(list(symbols))

    def detect_asset_type(self, symbol: str) -> AssetType:
        """Detect asset type from symbol"""
        symbol_upper = symbol.upper()

        crypto_symbols = [
            "BTC",
            "ETH",
            "SOL",
            "XRP",
            "ADA",
            "DOT",
            "DOGE",
            "LINK",
            "AVAX",
            "MATIC",
            "UNI",
            "ATOM",
        ]
        if any(sym in symbol_upper for sym in crypto_symbols):
            return AssetType.CRYPTO

        if symbol_upper.endswith("=X") or "/" in symbol_upper:
            if symbol_upper.startswith("XAU") or symbol_upper.startswith("XAG"):
                return AssetType.COMMODITY
            return AssetType.FOREX

        if symbol_upper.startswith("^"):
            return AssetType.INDEX

        return AssetType.STOCK


def get_free_data_provider() -> FreeDataProvider:
    """Get free data provider singleton"""
    return FreeDataProvider()


if __name__ == "__main__":
    provider = get_free_data_provider()

    print("Testing Free Data Provider...")
    print(f"Supported symbols: {len(provider.get_supported_symbols())}")

    test_symbols = ["AAPL", "BTC", "EURUSD"]

    for symbol in test_symbols:
        print(f"\nTesting {symbol}...")
        price = provider.get_current_price(symbol)
        print(f"  Current Price: {price.current_price}")
        print(f"  Daily Change: {price.daily_change_pct:.2f}%")
        print(f"  Asset Type: {price.asset_type}")

        data = provider.get_historical_data(symbol, days=7)
        print(f"  Historical Data Points: {len(data)}")
