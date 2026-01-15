# AI Quant Hedge Fund API Documentation

## Overview

AI Quant Hedge Fund v2.0 provides a comprehensive API for:
- Trading operations (paper & live)
- Portfolio management
- Market data access
- Strategy execution
- Multi-timeframe analysis

---

## Quick Start

```bash
# Install dependencies
pip install -e .

# Start trading terminal
python3 src/ui/web/trading_terminal.py

# API available at http://localhost:8050
```

---

## Core Components

### 1. Paper Trader API

```python
from src.paper_trading.paper_trader import create_paper_trader

# Initialize
trader = create_paper_trader(
    initial_capital=100000.0,
    max_positions=10,
    max_position_size=0.20
)

# Update prices
trader.update_price("EURUSD", 1.0850, 1.0855)

# Place order
result = trader.place_order(
    symbol="EURUSD",
    action="BUY",
    volume=1.0,
    sl=1.0800,
    tp=1.1000,
    strategy="ICT SMC",
    confidence=0.75
)

# Get status
status = trader.get_status()
# {
#     "cash": 99891.50,
#     "equity": 100141.50,
#     "daily_pnl": 141.50,
#     "open_positions": 1,
#     "win_rate": 0.0,
#     "profit_factor": 0
# }

# Get statistics
stats = trader.get_statistics()
```

#### Paper Trader Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `place_order()` | Place a trading order | Dict with order details |
| `close_position()` | Close specific position | Dict with PnL |
| `close_all_positions()` | Close all positions | List of close results |
| `update_price()` | Update market price | None |
| `get_status()` | Get current status | Dict |
| `get_statistics()` | Get trading stats | Dict |
| `reset()` | Reset to initial state | None |
| `export_trades()` | Export trades to JSON | None |

---

### 2. Multi-Timeframe Analyzer API

```python
from src.analysis.mtf_analyzer import create_mtf_analyzer

# Initialize
analyzer = create_mtf_analyzer()

# Get market summary
summary = analyzer.get_market_summary("EURUSD")
# {
#     "symbol": "EURUSD",
#     "overall_bias": "BULLISH",
#     "alignment_score": 0.75,
#     "recommendation": "BUY",
#     "timeframes_analyzed": {
#         "4H": {"trend": "BULLISH", "strength": 0.72, "structure": "UPTREND"},
#         "1D": {"trend": "BULLISH", "strength": 0.68, "structure": "UPTREND"},
#         "1W": {"trend": "NEUTRAL", "strength": 0.45, "structure": "CONSOLIDATING"}
#     }
# }

# Full analysis
signal = analyzer.analyze("EURUSD", htf="4H", ltf="15m", lookback_days=30)
# {
#     "symbol": "EURUSD",
#     "direction": "BUY",
#     "combined_confidence": 0.72,
#     "entry_price": 1.0875,
#     "stop_loss": 1.0800,
#     "take_profit": 1.1000,
#     "risk_reward_ratio": 3.0,
#     "reasoning": [...]
# }
```

#### MTF Analyzer Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `analyze()` | Perform MTF analysis | MultiTimeframeSignal |
| `get_market_summary()` | Get overall bias | Dict |

---

### 3. Trading Terminal API

```python
from src.ui.web.trading_terminal import app

# Run terminal
app.run(debug=False, port=8050, host="0.0.0.0")
```

#### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Trading terminal UI |
| `/api/status` | GET | Get trading status |
| `/api/positions` | GET | Get open positions |
| `/api/orders` | GET | Get pending orders |
| `/api/trades` | GET | Get trade history |
| `/api/analyze` | POST | Analyze symbol |

---

### 4. Portfolio Monitor API

```python
from src.monitoring.portfolio_monitor import PortfolioMonitor

# Initialize
monitor = PortfolioMonitor(broker=broker)

# Start monitoring
await monitor.start()

# Get snapshot
snapshot = monitor.get_portfolio_snapshot()

# Subscribe to updates
monitor.subscribe(callback_function)
```

---

### 5. Mode Manager API

```python
from src.modes.mode_manager import create_mode_manager

# Initialize
mode_manager = create_mode_manager("semi_auto")

# Check mode
mode_manager.current_mode  # TradingMode.SEMI_AUTO

# Switch mode
mode_manager.set_mode("full_auto", "Market conditions favorable")

# Check execution allowed
allowed, reason = mode_manager.is_execution_allowed(
    confidence=0.7,
    position_size=1.0,
    current_daily_loss=0.01
)
```

#### Trading Modes

| Mode | Auto Analyze | Auto Execute | Confirmation |
|------|--------------|--------------|--------------|
| `manual` | ❌ | ❌ | N/A |
| `semi_auto` | ✅ | ❌ | Required |
| `full_auto` | ✅ | ✅ | Not Required |

---

### 6. Execution Controller API

```python
from src.modes.execution_controller import create_execution_controller

# Initialize
controller = create_execution_controller(mode="semi_auto")

# Process signal
proposal = TradeProposal(
    symbol="EURUSD",
    side="BUY",
    volume=1.0,
    entry_price=1.0850,
    sl=1.0800,
    tp=1.1000,
    confidence=0.75,
    strategy="ICT SMC",
    reasoning=[...]
)

result = await controller.process_signal(proposal)

# Confirm order
if result.status == ExecutionStatus.PENDING:
    confirmed = await controller.confirm_proposal(
        order_id=proposal.order_id,
        confirmed=True
    )
```

---

### 7. Telegram Notifier API

```python
from src.integrations.telegram_notifier import create_telegram_notifier

# Initialize
notifier = create_telegram_notifier(
    bot_token="YOUR_BOT_TOKEN",
    chat_id="YOUR_CHAT_ID",
    enabled=True
)

# Start
await notifier.start()

# Send signal
signal = TradeSignal(
    symbol="EURUSD",
    side="BUY",
    entry_price=1.0850,
    stop_loss=1.0800,
    take_profit=1.1000,
    confidence=0.75,
    strategy="ICT SMC",
    reasoning=[...],
    risk_reward_ratio=3.0
)

await notifier.send_signal(signal, mode="semi_auto")

# Stop
await notifier.stop()
```

---

## Data Models

### TradeSignal

```python
@dataclass
class TradeSignal:
    symbol: str
    side: str  # BUY, SELL
    entry_price: float
    stop_loss: float
    take_profit: float
    confidence: float  # 0.0 - 1.0
    strategy: str
    reasoning: List[str]
    risk_reward_ratio: float
```

### HTFBias

```python
@dataclass
class HTFBias:
    timeframe: str
    trend: str  # BULLISH, BEARISH, NEUTRAL
    strength: float  # 0.0 - 1.0
    key_levels: Dict[str, float]
    structure: str  # UPTREND, DOWNTREND, etc.
    liquidity_levels: Dict[str, float]
```

### PaperPosition

```python
@dataclass
class PaperPosition:
    position_id: str
    symbol: str
    side: str  # LONG, SHORT
    volume: float
    entry_price: float
    entry_time: datetime
    sl: Optional[float]
    tp: Optional[float]
    current_price: float
    pnl: float
    pnl_pct: float
```

---

## Configuration

### Environment Variables

```bash
# Trading
INITIAL_CAPITAL=100000.0
MAX_POSITIONS=10
MAX_POSITION_SIZE=0.20

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# API Keys
ALPHA_VANTAGE_API_KEY=your_key
COINGECKO_API_KEY=your_key

# Database
REDIS_URL=redis://localhost:6379
```

### Risk Limits

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_positions` | 10 | Maximum open positions |
| `max_position_size` | 20% | Max position as % of equity |
| `max_daily_loss` | 5% | Daily loss limit |
| `max_correlation` | 0.7 | Max position correlation |

---

## Error Handling

```python
try:
    result = trader.place_order(...)
except InsufficientFundsError:
    print("Not enough capital")
except MaxPositionsError:
    print("Too many open positions")
except InvalidOrderError:
    print("Invalid order parameters")
```

---

## Examples

### Complete Trading Workflow

```python
from src.paper_trading.paper_trader import create_paper_trader
from src.analysis.mtf_analyzer import create_mtf_analyzer
from src.integrations.telegram_notifier import create_telegram_notifier

async def run_trading_workflow():
    # Initialize components
    trader = create_paper_trader(initial_capital=100000)
    analyzer = create_mtf_analyzer()
    notifier = create_telegram_notifier(
        bot_token="YOUR_TOKEN",
        chat_id="YOUR_CHAT_ID"
    )
    
    await notifier.start()
    
    # Get analysis
    signal = analyzer.analyze("EURUSD", htf="4H", ltf="15m")
    
    if signal.direction == "BUY" and signal.combined_confidence >= 0.6:
        # Place trade
        result = trader.place_order(
            symbol=signal.symbol,
            action="BUY",
            volume=1.0,
            sl=signal.stop_loss,
            tp=signal.take_profit,
            strategy=f"MTF_{signal.htf_bias.timeframe}",
            confidence=signal.combined_confidence,
            reason=signal.reasoning[0] if signal.reasoning else "MTF alignment"
        )
        
        # Send notification
        await notifier.send_signal(signal, mode="semi_auto")
    
    # Check status
    status = trader.get_status()
    print(f"Equity: ${status['equity']:,.2f}")
    
    await notifier.stop()

# Run
import asyncio
asyncio.run(run_trading_workflow())
```

---

## WebSocket API

Real-time updates via WebSocket:

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8765');

// Subscribe to updates
ws.onopen = () => {
    ws.send(JSON.stringify({ type: 'subscribe' }));
};

// Receive updates
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Update:', data);
};
```

### WebSocket Message Types

| Type | Description |
|------|-------------|
| `snapshot` | Full portfolio snapshot |
| `portfolio_update` | Real-time portfolio update |
| `position_update` | Position change |
| `signal_new` | New trading signal |

---

## Testing

```bash
# Run all tests
python3 -m pytest test_v2_components.py -v

# Run specific test
python3 -m pytest test_v2_components.py::TestPaperTrader -v

# Run with coverage
python3 -m pytest --cov=src test_v2_components.py
```

---

## Deployment

### Docker

```bash
# Build
docker build -f Dockerfile.production -t ai-hedge-fund .

# Run
docker run -p 8050:8050 -p 8765:8765 ai-hedge-fund

# With docker-compose
docker-compose up -d
```

---

*Last Updated: 2026-01-16*
*Version: 2.0.0*
