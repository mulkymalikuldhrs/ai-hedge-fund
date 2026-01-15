# AI Quant Hedge Fund v2.0 - ADDENDUM
## Fitur Tambahan: Live Trading, WebUI, dan Multi-Mode Operation

**Tanggal**: 2026-01-16
**Versi**: 2.0-ADDENDUM
**Status**: Perencanaan

---

## Daftar Isi

1. [Executive Summary](#1-executive-summary)
2. [MT4/MT5 Web Terminal Integration](#2-mt4mt5-web-terminal-integration)
3. [Real-time Portfolio & PNL Tracking](#3-real-time-portfolio--pnl-tracking)
4. [Multi-Timeframe Analysis](#4-multi-timeframe-analysis)
5. [UI/UX Architecture Decision](#5-uiux-architecture-decision)
6. [Live Terminal Dashboard](#6-live-terminal-dashboard)
7. [Live Candlestick Charts](#7-live-candlestick-charts)
8. [System Interaction Modes](#8-system-interaction-modes)
9. [Architecture Overview](#9-architecture-overview)
10. [Implementation Plan](#10-implementation-plan)
11. [Research References](#11-research-references)

---

## 1. Executive Summary

Dokumen ini adalah **addendum** untuk `docs/DEVELOPMENT_PLAN_v2.md` yang menambahkan fitur-fitur untuk **live trading** dan **user interface** yang belum tercatat sebelumnya.

### Fitur Baru yang Ditambahkan

| Fitur | Prioritas | Kompleksitas | Status |
|-------|-----------|--------------|--------|
| MT4/MT5 Web Integration | HIGH | HIGH | 🔲 Planning |
| Real-time Portfolio/PnL | HIGH | MEDIUM | 🔲 Planning |
| Multi-Timeframe Live | HIGH | MEDIUM | 🔲 Planning |
| WebUI vs TerminalUI | HIGH | MEDIUM | 🔲 Decision Needed |
| Live Dashboard | MEDIUM | HIGH | 🔲 Planning |
| Live Candlestick Charts | MEDIUM | HIGH | 🔲 Planning |
| Auto/Semi/M Manual Modes | HIGH | MEDIUM | 🔲 Planning |

### Arsitektur Target

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AI QUANT HEDGE FUND v2.0                         │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 1: USER INTERFACE                                            │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │
│  │   WEBUI (Light) │    │  TERMINAL UI    │    │  DASHBOARD      │ │
│  │  (Rich/Plotly)  │    │   (CLI/TUI)     │    │  (Streamlit)    │ │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘ │
├───────────┼─────────────────────┼───────────────────────┼──────────┤
│           │                     │                       │          │
│  ┌────────▼─────────────────────▼───────────────────────▼────────┐ │
│  │                    UNIFIED API GATEWAY                         │ │
│  │            REST API + WebSocket + gRPC (optional)              │ │
│  └─────────────────────────┬─────────────────────────────────────┘ │
│                            │                                         │
│  ┌─────────────────────────▼─────────────────────────────────────┐ │
│  │                    CORE TRADING ENGINE                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │ │
│  │  │  ANALYSIS   │  │  DECISION   │  │      EXECUTION          │ │ │
│  │  │   ENGINE    │  │    ENGINE   │  │      ENGINE             │ │ │
│  │  │ (34+ strats)│  │ (Signal agg)│  │ (MT5/Broker APIs)       │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘ │ │
│  └─────────────────────────┬─────────────────────────────────────┘ │
│                            │                                         │
│  ┌─────────────────────────▼─────────────────────────────────────┐ │
│  │                    BROKER CONNECTIONS                          │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │ │
│  │  │  MetaTrader5  │  │  Alpaca │  │ Binance │  │  CCXT (Multi)  │  │ │
│  │  │   (MT5)       │  │   API   │  │   API   │  │    Broker      │  │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. MT4/MT5 Web Terminal Integration

### 2.1 Overview

MetaTrader 4/5 adalah platform trading paling populer untuk Forex dan CFD. Integrasi web memungkinkan eksekusi trading dari browser tanpa install aplikasi desktop.

### 2.2 Reference Implementations

#### A. MetaTrader5 Python Package (Official)

```python
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

class MT5Broker:
    """MetaTrader 5 broker integration untuk autonomous trading"""
    
    def __init__(self, login: int, password: str, server: str):
        self.login = login
        self.password = password
        self.server = server
        self.connected = False
    
    def connect(self) -> bool:
        """Connect ke MT5 terminal"""
        if not mt5.initialize(
            login=self.login,
            server=self.server,
            password=self.password
        ):
            print(f"MT5 init failed: {mt5.last_error()}")
            return False
        
        self.connected = True
        print(f"Connected to MT5: {self.server}")
        return True
    
    def get_rates(self, symbol: str, timeframe: str, count: int = 1000):
        """Ambil data OHLC"""
        tf_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
        }
        
        rates = mt5.copy_rates_from_pos(symbol, tf_map[timeframe], 0, count)
        if rates is None:
            return None
        
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
    
    def place_order(
        self,
        symbol: str,
        action: str,  # "BUY" or "SELL"
        volume: float,
        stop_loss: float = None,
        take_profit: float = None,
        magic: int = 9001
    ) -> dict:
        """Place market order"""
        tick = mt5.symbol_info_tick(symbol)
        price = tick.ask if action == "BUY" else tick.bid
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY if action == "BUY" else mt5.ORDER_TYPE_SELL,
            "price": price,
            "deviation": 10,
            "magic": magic,
            "comment": "AI_HedgeFund",
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        if stop_loss:
            request["sl"] = stop_loss
        if take_profit:
            request["tp"] = take_profit
        
        result = mt5.order_send(request)
        return {
            "retcode": result.retcode,
            "order": result.order,
            "volume": result.volume,
            "price": result.price,
            "pnl": result.profit
        }
    
    def get_positions(self, symbol: str = None) -> list:
        """Get open positions"""
        positions = mt5.positions_get(symbol=symbol if symbol else "*")
        return [
            {
                "ticket": p.ticket,
                "symbol": p.symbol,
                "type": "BUY" if p.type == mt5.POSITION_TYPE_BUY else "SELL",
                "volume": p.volume,
                "open_price": p.price_open,
                "current_price": p.price_current,
                "pnl": p.profit,
                "sl": p.sl,
                "tp": p.tp
            }
            for p in positions
        ]
    
    def get_account_info(self) -> dict:
        """Get account balance, equity, margin"""
        info = mt5.account_info()
        return {
            "balance": info.balance,
            "equity": info.equity,
            "margin": info.margin,
            "free_margin": info.margin_free,
            "leverage": info.leverage,
            "currency": info.currency
        }
    
    def close_position(self, ticket: int, volume: float = None):
        """Close position by ticket"""
        position = mt5.positions_get(ticket=ticket)[0]
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": volume or position.volume,
            "type": mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "position": ticket,
            "price": mt5.symbol_info_tick(position.symbol).bid if position.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(position.symbol).ask,
            "deviation": 10,
            "magic": 9001,
            "comment": "AI_HedgeFund_Close"
        }
        
        return mt5.order_send(request)
    
    def shutdown(self):
        """Disconnect from MT5"""
        mt5.shutdown()
        self.connected = False
```

#### B. ZeroMQ Connector (Darwinex DWX)

```python
import zmq
import json

class DWX_MT5_Connector:
    """ZeroMQ-based connector untuk MT5 (alternative to official API)"""
    
    def __init__(self, host: str = "localhost", push_port: int = 32769):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect(f"tcp://{host}:{push_port}")
    
    def send_command(self, command: dict):
        """Send command ke MT5"""
        self.socket.send_json(command)
    
    def new_trade(self, symbol: str, action: str, volume: float, sl: int, tp: int):
        """Open new trade"""
        self.send_command({
            "_action": "OPEN",
            "_symbol": symbol,
            "_type": action,  # "buy" or "sell"
            "_volume": volume,
            "_sl": sl,  # pips
            "_tp": tp,  # pips
            "_magic": 123456
        })
    
    def close_all(self):
        """Close all positions"""
        self.send_command({"_action": "CLOSE_ALL"})
    
    def get_open_positions(self) -> list:
        """Request open positions (response via separate SUB socket)"""
        self.send_command({"_action": "GET_OPEN_POSITIONS"})
```

### 2.3 Web Integration Options

#### Option A: MetaTrader Web API (Cloud-based)

```python
# Using metatraderapi.cloud atau similar service
class MT5WebAPI:
    """Web-based MT5 API integration"""
    
    def __init__(self, api_key: str, base_url: str = "https://metatraderapi.cloud"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def create_session(self, login: str, password: str, server: str):
        """Create trading session"""
        response = self.session.post(
            f"{self.base_url}/api/sessions/start/",
            json={"login": login, "password": password, "server": server}
        )
        return response.json()
    
    def place_order(self, session_id: str, order: dict):
        """Place order via web API"""
        response = self.session.post(
            f"{self.base_url}/api/sessions/{session_id}/trade/open/",
            json=order
        )
        return response.json()
    
    def get_positions(self, session_id: str):
        """Get open positions"""
        response = self.session.get(
            f"{self.base_url}/api/sessions/{session_id}/positions/"
        )
        return response.json()
```

#### Option B: Headless MT5 with Docker

```dockerfile
# Dockerfile untuk headless MT5
FROM nevmerzhitsky/headless-metatrader4:latest

# Copy EA (Expert Advisor) for automated trading
COPY ./expert/AIHedgeFund.ex5 /home/winer/.wine/drive_c/mt4/experts/

# Configure auto-trading
ENV AUTO_TRADING=true
ENV EXPERT=AIHedgeFund

# Expose ports for Python API
EXPOSE 32768 32769 32770
```

### 2.4 Execution Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     EXECUTION LAYER                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐                                                 │
│  │  TRADING ENGINE │                                                 │
│  │   (our system)  │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐    ┌─────────────────────────────────────────┐  │
│  │ ORDER MANAGER   │───▶│ MT5 BRIDGE (Python → MT5 Terminal)      │  │
│  │  - Validation   │    │  ┌─────────────────────────────────────┐ │  │
│  │  - Risk Check   │    │  │ Option A: MetaTrader5 Package       │ │  │
│  │  - Size Calc    │    │  │   Direct local terminal connection  │ │  │
│  └─────────────────┘    │  │ Option B: ZeroMQ Connector          │ │  │
│                         │  │   Network-based message passing     │ │  │
│                         │  │ Option C: Web API (cloud)           │ │  │
│                         │  │   Remote terminal access            │ │  │
│                         │  └─────────────────────────────────────┘ │  │
│                         └─────────────────────────────────────────┘  │
│           │                                                          │
│           ▼                                                          │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    METATRADER 5 TERMINAL                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │  │
│  │  │ Chart    │  │ Strategy │  │  EA      │  │  Order       │   │  │
│  │  │ (visual) │  │ (manual) │  │(auto)    │  │  Management  │   │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │  │
│  │                                                               │  │
│  │  Connected to Broker via MQL5.community                       │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.5 Implementation Tasks

| Task | Description | Priority |
|------|-------------|----------|
| MT5-001 | Implement `MT5Broker` class dengan official API | HIGH |
| MT5-002 | Add ZeroMQ alternative connector | MEDIUM |
| MT5-003 | Create order validation & risk check | HIGH |
| MT5-004 | Implement position management (SL/TP/partial close) | HIGH |
| MT5-005 | Add connection monitoring & auto-reconnect | MEDIUM |
| MT5-006 | Create Docker setup untuk headless MT5 | LOW |
| MT5-007 | Add web API integration option | MEDIUM |

---

## 3. Real-time Portfolio & PNL Tracking

### 3.1 Portfolio Data Model

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum
import pandas as pd
import numpy as np

class PositionStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PENDING = "PENDING"

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"

@dataclass
class Position:
    """Trading position"""
    ticket: int
    symbol: str
    side: OrderSide
    volume: float
    open_price: float
    open_time: datetime
    sl: Optional[float] = None
    tp: Optional[float] = None
    current_price: Optional[float] = None
    commission: float = 0.0
    swap: float = 0.0
    magic: int = 9001
    comment: str = ""
    
    @property
    def current_value(self) -> float:
        if self.current_price is None:
            return self.volume * self.open_price
        return self.volume * self.current_price
    
    @property
    def pnl(self) -> float:
        if self.side == OrderSide.BUY:
            return (self.current_price - self.open_price) * self.volume * 100000  # for Forex
        else:
            return (self.open_price - self.current_price) * self.volume * 100000
    
    @property
    def pnl_pct(self) -> float:
        return self.pnl / (self.open_price * self.volume * 100000) * 100

@dataclass
class Trade:
    """Completed trade record"""
    ticket: int
    symbol: str
    side: OrderSide
    volume: float
    entry_price: float
    exit_price: float
    entry_time: datetime
    exit_time: datetime
    commission: float = 0.0
    swap: float = 0.0
    pnl: float = 0.0
    pnl_pct: float = 0.0
    duration_hours: float = 0.0
    
    @classmethod
    def from_position(cls, position: Position, exit_price: float, exit_time: datetime):
        if position.side == OrderSide.BUY:
            pnl = (exit_price - position.open_price) * position.volume * 100000
        else:
            pnl = (position.open_price - exit_price) * position.volume * 100000
        
        duration = (exit_time - position.open_time).total_seconds() / 3600
        
        return cls(
            ticket=position.ticket,
            symbol=position.symbol,
            side=position.side,
            volume=position.volume,
            entry_price=position.open_price,
            exit_price=exit_price,
            entry_time=position.open_time,
            exit_time=exit_time,
            commission=position.commission,
            swap=position.swap,
            pnl=pnl,
            pnl_pct=pnl / (position.open_price * position.volume * 100000) * 100,
            duration_hours=duration
        )

@dataclass
class Portfolio:
    """Portfolio state"""
    account_balance: float
    account_equity: float
    account_currency: str = "USD"
    positions: Dict[int, Position] = field(default_factory=dict)
    trades: List[Trade] = field(default_factory=list)
    daily_pnl: float = 0.0
    total_pnl: float = 0.0
    margin_used: float = 0.0
    margin_free: float = 0.0
    margin_level: float = 0.0
    last_update: datetime = field(default_factory=datetime.now)
    
    @property
    def open_positions_count(self) -> int:
        return len(self.positions)
    
    @property
    def long_exposure(self) -> float:
        return sum(
            p.current_value 
            for p in self.positions.values() 
            if p.side == OrderSide.BUY
        )
    
    @property
    def short_exposure(self) -> float:
        return sum(
            p.current_value 
            for p in self.positions.values() 
            if p.side == OrderSide.SELL
        )
    
    @property
    def net_exposure(self) -> float:
        return self.long_exposure - self.short_exposure
    
    def calculate_statistics(self) -> dict:
        """Calculate portfolio statistics"""
        if not self.trades:
            return {}
        
        closed_pnls = [t.pnl for t in self.trades]
        wins = [p for p in closed_pnls if p > 0]
        losses = [p for p in closed_pnls if p <= 0]
        
        return {
            "total_trades": len(self.trades),
            "win_rate": len(wins) / len(closed_pnls) if closed_pnls else 0,
            "profit_factor": abs(sum(wins) / sum(losses)) if losses and sum(losses) != 0 else float('inf'),
            "avg_win": np.mean(wins) if wins else 0,
            "avg_loss": np.mean(losses) if losses else 0,
            "max_win": max(wins) if wins else 0,
            "max_loss": min(losses) if losses else 0,
            "avg_trade_duration_hours": np.mean([t.duration_hours for t in self.trades]) if self.trades else 0,
            "longest_win_streak": self._calculate_streak(wins),
            "longest_loss_streak": self._calculate_streak(losses),
        }
    
    def _calculate_streak(self, trades: List[float]) -> int:
        """Calculate longest winning/losing streak"""
        if not trades:
            return 0
        max_streak = current_streak = 0
        for trade in trades:
            if trade > 0 or (len(trades) > 0 and trades[0] == 0):
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        return max_streak
```

### 3.2 Real-time PnL Calculator

```python
import asyncio
from typing import Callable
from datetime import datetime

class RealTimePortfolioMonitor:
    """Real-time portfolio and PnL tracking"""
    
    def __init__(self, broker, update_interval: float = 1.0):
        self.broker = broker
        self.update_interval = update_interval
        self.portfolio = Portfolio(account_balance=100000.0, account_equity=100000.0)
        self.subscribers: List[Callable] = []
        self.running = False
        self._price_cache: Dict[str, float] = {}
    
    def subscribe(self, callback: Callable):
        """Subscribe to portfolio updates"""
        self.subscribers.append(callback)
    
    def _notify_subscribers(self):
        """Notify all subscribers of update"""
        for callback in self.subscribers:
            try:
                callback(self.portfolio)
            except Exception as e:
                print(f"Subscriber callback failed: {e}")
    
    async def start(self):
        """Start real-time monitoring"""
        self.running = True
        while self.running:
            try:
                await self._update_portfolio()
                self._notify_subscribers()
                await asyncio.sleep(self.update_interval)
            except Exception as e:
                print(f"Portfolio update failed: {e}")
                await asyncio.sleep(5)  # Retry delay
    
    async def _update_portfolio(self):
        """Update portfolio from broker"""
        # Get account info
        account = self.broker.get_account_info()
        self.portfolio.account_balance = account["balance"]
        self.portfolio.account_equity = account["equity"]
        self.portfolio.margin_used = account["margin"]
        self.portfolio.margin_free = account["free_margin"]
        self.portfolio.margin_level = account["equity"] / account["margin"] * 100 if account["margin"] > 0 else 0
        self.portfolio.last_update = datetime.now()
        
        # Update position prices
        positions = self.broker.get_positions()
        for pos_data in positions:
            ticket = pos_data["ticket"]
            if ticket in self.portfolio.positions:
                position = self.portfolio.positions[ticket]
                position.current_price = pos_data.get("current_price", pos_data["open_price"])
                position.pnl = pos_data.get("pnl", 0)
    
    def get_portfolio_snapshot(self) -> dict:
        """Get current portfolio snapshot"""
        stats = self.portfolio.calculate_statistics()
        return {
            "timestamp": self.portfolio.last_update.isoformat(),
            "account": {
                "balance": self.portfolio.account_balance,
                "equity": self.portfolio.account_equity,
                "margin_used": self.portfolio.margin_used,
                "margin_free": self.portfolio.margin_free,
                "margin_level": self.portfolio.margin_level,
            },
            "positions": {
                str(ticket): {
                    "symbol": p.symbol,
                    "side": p.side.value,
                    "volume": p.volume,
                    "open_price": p.open_price,
                    "current_price": p.current_price,
                    "pnl": p.pnl,
                    "pnl_pct": p.pnl_pct,
                    "sl": p.sl,
                    "tp": p.tp
                }
                for ticket, p in self.portfolio.positions.items()
            },
            "statistics": stats,
            "exposure": {
                "long": self.portfolio.long_exposure,
                "short": self.portfolio.short_exposure,
                "net": self.portfolio.net_exposure
            }
        }
    
    async def stop(self):
        """Stop monitoring"""
        self.running = False
```

### 3.3 WebSocket untuk Real-time Updates

```python
import asyncio
import websockets
import json
from typing import Set

class PortfolioWebSocketServer:
    """WebSocket server untuk real-time portfolio updates"""
    
    def __init__(self, port: int = 8765):
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.portfolio_monitor = None
    
    async def register(self, websocket: websockets.WebSocketServerProtocol):
        """Register new client"""
        self.clients.add(websocket)
        print(f"Client connected. Total: {len(self.clients)}")
    
    async def unregister(self, websocket: websockets.WebSocketServerProtocol):
        """Unregister client"""
        self.clients.remove(websocket)
        print(f"Client disconnected. Total: {len(self.clients)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all clients"""
        if not self.clients:
            return
        
        message_str = json.dumps(message)
        await asyncio.gather(
            *[client.send(message_str) for client in self.clients],
            return_exceptions=True
        )
    
    async def handler(self, websocket: websockets.WebSocketServerProtocol):
        """Handle client connections"""
        await self.register(websocket)
        try:
            async for message in websocket:
                # Handle client requests
                data = json.loads(message)
                if data.get("type") == "subscribe":
                    # Client wants updates - already registered
                    pass
                elif data.get("type") == "get_snapshot":
                    snapshot = self.portfolio_monitor.get_portfolio_snapshot()
                    await websocket.send(json.dumps({
                        "type": "snapshot",
                        "data": snapshot
                    }))
        finally:
            await self.unregister(websocket)
    
    async def start(self, portfolio_monitor: RealTimePortfolioMonitor):
        """Start WebSocket server"""
        self.portfolio_monitor = portfolio_monitor
        
        # Subscribe to portfolio updates
        portfolio_monitor.subscribe(lambda p: asyncio.create_task(
            self.broadcast({
                "type": "portfolio_update",
                "data": p.get_portfolio_snapshot()
            })
        ))
        
        async with websockets.serve(self.handler, "0.0.0.0", self.port):
            print(f"WebSocket server started on port {self.port}")
            await asyncio.Future()  # Run forever
```

---

## 4. Multi-Timeframe Analysis

### 4.1 Multi-Timeframe Architecture

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import pandas as pd
import numpy as np

class Timeframe(Enum):
    """Supported timeframes"""
    TICK = "tick"
    SECOND_1 = "1s"
    SECOND_5 = "5s"
    SECOND_15 = "15s"
    SECOND_30 = "30s"
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    DAY_1 = "1d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"

@dataclass
class TimeframeData:
    """Data for a single timeframe"""
    timeframe: Timeframe
    df: pd.DataFrame
    last_update: datetime
    
    @property
    def ohlcv(self) -> pd.DataFrame:
        return self.df
    
    @property
    def latest(self) -> dict:
        if self.df.empty:
            return {}
        last = self.df.iloc[-1]
        return {
            "open": last.get("open", last.get("close")),
            "high": last.get("high", last.get("close")),
            "low": last.get("low", last.get("close")),
            "close": last.get("close"),
            "volume": last.get("volume", 0),
            "time": last.name
        }

class MultiTimeframeAnalyzer:
    """Analyze market across multiple timeframes"""
    
    def __init__(self):
        self.data: Dict[str, Dict[Timeframe, TimeframeData]] = {}
        self.timeframe_hierarchy = [
            Timeframe.TICK,
            Timeframe.SECOND_1,
            Timeframe.SECOND_5,
            Timeframe.MINUTE_1,
            Timeframe.MINUTE_5,
            Timeframe.MINUTE_15,
            Timeframe.HOUR_1,
            Timeframe.HOUR_4,
            Timeframe.DAY_1,
            Timeframe.WEEK_1,
        ]
    
    def add_symbol_data(
        self,
        symbol: str,
        timeframe: Timeframe,
        df: pd.DataFrame
    ):
        """Add data for a symbol at specific timeframe"""
        if symbol not in self.data:
            self.data[symbol] = {}
        
        self.data[symbol][timeframe] = TimeframeData(
            timeframe=timeframe,
            df=df,
            last_update=datetime.now()
        )
    
    def get_higher_timeframe_trend(self, symbol: str) -> dict:
        """Get trend from higher timeframes (HTF)"""
        if symbol not in self.data:
            return {"trend": "UNKNOWN", "confidence": 0}
        
        trends = []
        confidences = []
        
        # Check from higher to lower timeframe
        tf_order = [
            Timeframe.WEEK_1,
            Timeframe.DAY_1,
            Timeframe.HOUR_4,
            Timeframe.HOUR_1,
        ]
        
        for tf in tf_order:
            if tf in self.data[symbol]:
                df = self.data[symbol][tf].df
                if len(df) < 20:
                    continue
                
                # Calculate trend based on price position vs moving averages
                sma20 = df['close'].rolling(20).mean().iloc[-1]
                sma50 = df['close'].rolling(50).mean().iloc[-1]
                current = df['close'].iloc[-1]
                
                if current > sma20 > sma50:
                    trends.append("BULLISH")
                    confidences.append(0.8)
                elif current < sma20 < sma50:
                    trends.append("BEARISH")
                    confidences.append(0.8)
                else:
                    trends.append("NEUTRAL")
                    confidences.append(0.5)
        
        if not trends:
            return {"trend": "UNKNOWN", "confidence": 0}
        
        # Majority vote
        from collections import Counter
        trend_counts = Counter(trends)
        dominant_trend = trend_counts.most_common(1)[0][0]
        avg_confidence = np.mean(confidences)
        
        return {
            "trend": dominant_trend,
            "confidence": avg_confidence,
            "timeframes_analyzed": len(trends),
            "details": {
                tf.value: trend 
                for tf, trend in zip(tf_order[:len(trends)], trends)
            }
        }
    
    def get_htf_bias(self, symbol: str) -> float:
        """
        Get HTF bias: -1 (bearish) to +1 (bullish)
        Used to filter LTF signals
        """
        htf = self.get_higher_timeframe_trend(symbol)
        trend = htf.get("trend", "NEUTRAL")
        confidence = htf.get("confidence", 0)
        
        bias_map = {
            "BULLISH": confidence,
            "BEARISH": -confidence,
            "NEUTRAL": 0,
            "UNKNOWN": 0
        }
        
        return bias_map.get(trend, 0)
    
    def get_multi_tf_signal(self, symbol: str, ltf_signal: str, ltf_confidence: float) -> dict:
        """
        Combine LTF signal dengan HTF bias
        
        Args:
            symbol: Trading symbol
            ltf_signal: Signal dari lower timeframe (BUY/SELL/HOLD)
            ltf_confidence: Confidence dari LTF signal
        
        Returns:
            Combined signal dengan HTF adjustment
        """
        htf_bias = self.get_htf_bias(symbol)
        
        # Adjust confidence based on HTF bias
        # If HTF is bullish and LTF says BUY, boost confidence
        # If HTF is bullish and LTF says SELL, reduce confidence
        if ltf_signal == "BUY":
            adjusted_confidence = ltf_confidence * (1 + htf_bias * 0.5)
        elif ltf_signal == "SELL":
            adjusted_confidence = ltf_confidence * (1 - htf_bias * 0.5)
        else:
            adjusted_confidence = ltf_confidence
        
        # Determine final signal
        if ltf_signal == "HOLD":
            final_signal = "HOLD"
        elif adjusted_confidence >= 0.65:
            final_signal = ltf_signal
        elif adjusted_confidence <= 0.35:
            final_signal = "HOLD"
        else:
            # Medium confidence - check alignment
            if (ltf_signal == "BUY" and htf_bias > 0.2) or \
               (ltf_signal == "SELL" and htf_bias < -0.2):
                final_signal = ltf_signal
            else:
                final_signal = "HOLD"
        
        return {
            "signal": final_signal,
            "adjusted_confidence": min(1.0, max(0.0, adjusted_confidence)),
            "ltf_signal": ltf_signal,
            "ltf_confidence": ltf_confidence,
            "htf_bias": htf_bias,
            "htf_trend": self.get_higher_timeframe_trend(symbol).get("trend", "UNKNOWN"),
            "alignment": "ALIGNED" if (htf_bias > 0 and ltf_signal == "BUY") or (htf_bias < 0 and ltf_signal == "SELL") or (htf_bias == 0) else "CONFLICTED"
        }
```

### 4.2 Live Multi-Timeframe Data Pipeline

```python
import asyncio
from typing import Dict, List
import websockets
import json

class MultiTimeframeDataStream:
    """Stream and aggregate data across multiple timeframes"""
    
    def __init__(self, data_provider, timeframes: List[Timeframe] = None):
        self.data_provider = data_provider
        self.timeframes = timeframes or [
            Timeframe.MINUTE_1,
            Timeframe.MINUTE_5,
            Timeframe.MINUTE_15,
            Timeframe.HOUR_1,
            Timeframe.HOUR_4,
            Timeframe.DAY_1
        ]
        self.analyzer = MultiTimeframeAnalyzer()
        self.running = False
        self.subscribers: Dict[str, List[callable]] = {}
    
    async def start(self, symbols: List[str]):
        """Start streaming data untuk all symbols"""
        self.running = True
        
        # Start WebSocket connections for live data
        tasks = []
        for symbol in symbols:
            for tf in self.timeframes:
                tasks.append(self._stream_symbol_tf(symbol, tf))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _stream_symbol_tf(self, symbol: str, timeframe: Timeframe):
        """Stream data for single symbol at timeframe"""
        ws_url = self._get_websocket_url(symbol, timeframe)
        
        async for message in self._websocket_connect(ws_url):
            data = self._parse_message(message, timeframe)
            self.analyzer.add_symbol_data(symbol, timeframe, data)
            
            # Notify subscribers
            await self._notify_subscribers(symbol, timeframe, data)
    
    def _get_websocket_url(self, symbol: str, timeframe: Timeframe) -> str:
        """Get WebSocket URL untuk data stream"""
        # Example for Binance
        return f"wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_{timeframe.value}"
    
    async def _websocket_connect(self, url: str):
        """Connect to WebSocket stream"""
        async with websockets.connect(url) as ws:
            async for message in ws:
                yield message
    
    def _parse_message(self, message: str, timeframe: Timeframe) -> pd.DataFrame:
        """Parse WebSocket message ke DataFrame"""
        data = json.loads(message)
        kline = data.get("k", {})
        
        # Extract OHLCV
        df = pd.DataFrame([{
            "open": float(kline["o"]),
            "high": float(kline["h"]),
            "low": float(kline["l"]),
            "close": float(kline["c"]),
            "volume": float(kline["v"]),
            "time": pd.to_datetime(kline["t"], unit='ms')
        }])
        
        df.set_index("time", inplace=True)
        return df
    
    async def _notify_subscribers(self, symbol: str, timeframe: Timeframe, data: pd.DataFrame):
        """Notify subscribers of new data"""
        if symbol in self.subscribers:
            for callback in self.subscribers[symbol]:
                try:
                    callback(symbol, timeframe, data)
                except Exception as e:
                    print(f"Subscriber callback failed: {e}")
    
    def subscribe(self, symbol: str, callback: callable):
        """Subscribe to updates for a symbol"""
        if symbol not in self.subscribers:
            self.subscribers[symbol] = []
        self.subscribers[symbol].append(callback)
    
    def get_analysis(self, symbol: str) -> dict:
        """Get full analysis for a symbol across all timeframes"""
        return {
            "symbol": symbol,
            "htf_trend": self.analyzer.get_higher_timeframe_trend(symbol),
            "all_timeframes": {
                tf.value: data.latest 
                for tf, data in self.analyzer.data.get(symbol, {}).items()
            }
        }
```

---

## 5. UI/UX Architecture Decision

### 5.1 Comparison: WebUI vs Terminal UI vs Dashboard

| Criteria | WebUI (Rich) | Terminal UI (CLI/TUI) | Dashboard (Streamlit) |
|----------|--------------|----------------------|----------------------|
| **Performance** | High (browser) | Very High (local) | Medium (Python) |
| **Interactivity** | Excellent | Good | Good |
| **Lightweight** | Medium | Very High | Medium |
| **Setup Complexity** | Medium | Low | Low |
| **Live Charts** | Excellent (JS libs) | Limited (curses) | Good (Plotly) |
| **Customization** | High (HTML/CSS/JS) | Medium (Python) | Medium (Python) |
| **Deployment** | Server + Browser | Local only | Local/Server |
| **Best For** | Production web app | Dev/Ops/Quick check | Quick analytics |

### 5.2 Recommendation: Hybrid Approach

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RECOMMENDED UI ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    LAYER 1: TERMINAL (Primary)               │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  Rich TUI (Textual)                                  │    │    │
│  │  │  - Live candles in terminal                          │    │    │
│  │  │  - Real-time portfolio P&L                           │    │    │
│  │  │  - Color-coded signals                               │    │    │
│  │  │  - Keyboard shortcuts                                │    │    │
│  │  │  - Low latency, no browser                           │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  │                                                               │    │
│  │  Tools: Textual (https://textual.textualize.io/)             │    │
│  │         Rich (https://rich.readthedocs.io/)                  │    │
│  │         Blessed (https://blessed.readthedocs.io/)             │    │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                       │
│                              │ (API Gateway)                         │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │               LAYER 2: OPTIONAL WEB UI                      │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  Streamlit Dashboard (Optional, for charts/analytics)│    │    │
│  │  │  - Interactive candlestick charts                   │    │    │
│  │  │  - Portfolio analytics                              │    │    │
│  │  │  - Strategy comparison                              │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  │                                                               │    │
│  │ 启动: streamlit run dashboard.py                             │    │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                       │
│                              │ (REST API + WebSocket)                 │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │               LAYER 3: CORE TRADING ENGINE                   │    │
│  │  All logic runs here, accessible via API                    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.3 Textual TUI Implementation

```python
from textual.app import App, ComposeResult
from textual.containers import Container, Grid, Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Button, ProgressBar
from textual.reactive import reactive
from datetime import datetime
import asyncio

class TradingDashboard(App):
    """Main TUI Dashboard for AI Hedge Fund"""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-rows: 3;
    }
    .header {
        column-span: 2;
        background: $accent;
        color: $text;
        height: 3;
    }
    .portfolio {
        column-span: 1;
        border: solid $accent;
        padding: 1;
    }
    .positions {
        column-span: 1;
        border: solid $accent;
        padding: 1;
    }
    .chart {
        column-span: 2;
        border: solid $accent;
        height: 20;
    }
    .status {
        column-span: 2;
        background: $surface-darken-1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("a", "analyze", "Analyze All"),
        ("s", "settings", "Settings"),
    ]
    
    portfolio_value = reactive(100000.0)
    daily_pnl = reactive(0.0)
    positions_count = reactive(0)
    active_signal = reactive("HOLD")
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Container(classes="header"):
            yield Static("AI QUANT HEDGE FUND v2.0", classes="title")
            yield Static(id="timestamp")
        
        with Grid(classes="portfolio"):
            yield Static("💰 PORTFOLIO", classes="section-title")
            yield Static(id="balance", classes="value")
            yield Static(id="equity", classes="value")
            yield Static(id="daily_pnl", classes="value")
            yield ProgressBar(total=100, show_eta=False, id="margin_usage")
        
        with Grid(classes="positions"):
            yield Static("📊 OPEN POSITIONS", classes="section-title")
            yield Static(id="positions_list", classes="positions")
        
        with Container(classes="chart"):
            yield Static("🕯️ LIVE CHART", classes="section-title")
            yield Static(id="chart_display", classes="chart")
        
        with Horizontal(classes="status"):
            yield Static(id="signal_indicator", classes="signal")
            yield Static(id="connection_status", classes="status")
            yield Static(id="active_strategy", classes="strategy")
        
        yield Footer()
    
    def watch_portfolio_value(self, value: float):
        """Update portfolio display"""
        self.query_one("#balance", Static).update(f"Balance: ${value:,.2f}")
    
    def watch_daily_pnl(self, value: float):
        """Update PnL display"""
        pnl_str = f"Daily PnL: ${value:+,.2f}" if value >= 0 else f"Daily PnL: ${value:,.2f}"
        color = "green" if value >= 0 else "red"
        self.query_one("#daily_pnl", Static).update(pnl_str)
        self.query_one("#daily_pnl", Static).styles.color = color
    
    def watch_active_signal(self, signal: str):
        """Update signal indicator"""
        emoji = {"HOLD": "🟡", "BUY": "🟢", "SELL": "🔴"}
        self.query_one("#signal_indicator", Static).update(
            f"{emoji.get(signal, '⚪')} SIGNAL: {signal}"
        )
    
    def action_analyze(self):
        """Trigger analysis"""
        # Call trading engine for analysis
        pass
    
    def action_refresh(self):
        """Refresh all data"""
        pass
    
    def action_settings(self):
        """Open settings"""
        pass


class CandlestickWidget(Static):
    """Custom widget for candlestick display in TUI"""
    
    CSS = """
    CandlestickWidget {
        height: 100%;
        width: 100%;
        overflow: hidden;
    }
    """
    
    def __init__(self, data: list = None):
        super().__init__()
        self.data = data or []
    
    def render(self) -> str:
        """Render simplified candlestick chart"""
        if not self.data:
            return "No data available"
        
        # Create ASCII candlestick chart
        lines = []
        for i, candle in enumerate(self.data[-30:]):  # Last 30 candles
            if candle["close"] >= candle["open"]:
                char = "🟢"  # Bullish
                high_low = "│"
            else:
                char = "🔴"  # Bearish
                high_low = "│"
            
            line = f"{char} {candle['time']} O:{candle['open']:.2f} H:{candle['high']:.2f} L:{candle['low']:.2f} C:{candle['close']:.2f}"
            lines.append(line)
        
        return "\n".join(lines)
```

### 5.4 Streamlit Dashboard (Optional)

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

class TradingDashboard:
    """Streamlit dashboard untuk AI Hedge Fund"""
    
    def __init__(self):
        st.set_page_config(
            page_title="AI Hedge Fund v2.0",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render(self):
        """Render dashboard"""
        # Header
        st.title("🤖 AI Quant Hedge Fund v2.0")
        st.markdown("---")
        
        # Top metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Portfolio Value", "$125,432.10", "+2.5%")
        with col2:
            st.metric("Daily PnL", "+$1,234.56", "+1.2%")
        with col3:
            st.metric("Open Positions", "5", "+2")
        with col4:
            st.metric("Win Rate", "68%", "+5%")
        with col5:
            st.metric("Sharpe Ratio", "2.34", "+0.12")
        
        st.markdown("---")
        
        # Main chart
        col_chart, col_orders = st.columns([3, 1])
        
        with col_chart:
            self.render_candlestick_chart()
        
        with col_orders:
            self.render_positions()
            self.render_recent_trades()
        
        # Strategy signals
        st.subheader("🎯 Strategy Signals")
        self.render_strategy_signals()
        
        # Backtest results
        st.subheader("📊 Backtest Results")
        self.render_backtest_results()
    
    def render_candlestick_chart(self):
        """Render interactive candlestick chart"""
        # Get data from backend
        df = self.get_chart_data()
        
        if df.empty:
            st.warning("No data available")
            return
        
        # Create candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=df['time'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        )])
        
        # Add indicators
        df['sma20'] = df['close'].rolling(20).mean()
        df['sma50'] = df['close'].rolling(50).mean()
        
        fig.add_trace(go.Scatter(
            x=df['time'], y=df['sma20'],
            line=dict(color='blue', width=1),
            name='SMA20'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['time'], y=df['sma50'],
            line=dict(color='orange', width=1),
            name='SMA50'
        ))
        
        fig.update_layout(
            title="Live Price Chart",
            yaxis_title="Price (USD)",
            xaxis_title="Time",
            template="plotly_dark",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_positions(self):
        """Render open positions"""
        positions = self.get_positions()
        
        if not positions:
            st.info("No open positions")
            return
        
        df = pd.DataFrame(positions)
        st.dataframe(
            df.style.format({
                'pnl': '${:+.2f}',
                'pnl_pct': '{:+.2f}%',
                'volume': '{:.2f}'
            }),
            use_container_width=True
        )
    
    def render_strategy_signals(self):
        """Render all strategy signals"""
        signals = self.get_strategy_signals()
        
        df = pd.DataFrame(signals)
        if df.empty:
            st.warning("No signals available")
            return
        
        # Color code by signal
        def color_signal(val):
            if val == 'BUY':
                return 'color: green'
            elif val == 'SELL':
                return 'color: red'
            return ''
        
        st.dataframe(
            df.style.applymap(color_signal, subset=['signal']),
            use_container_width=True
        )
    
    def get_chart_data(self) -> pd.DataFrame:
        """Get chart data from backend"""
        # This would call the trading engine API
        return pd.DataFrame()
    
    def get_positions(self) -> list:
        """Get open positions from backend"""
        return []
    
    def get_strategy_signals(self) -> list:
        """Get all strategy signals"""
        return []
    
    def get_backtest_results(self) -> pd.DataFrame:
        """Get backtest results"""
        return pd.DataFrame()


# Run dashboard
if __name__ == "__main__":
    dashboard = TradingDashboard()
    dashboard.render()
```

---

## 6. Live Terminal Dashboard

### 6.1 Dashboard Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AI QUANT HEDGE FUND - LIVE TERMINAL                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  💰 PORTFOLIO                    📊 MARKET STATUS                    │  │
│  │  ────────────────               ─────────────────                    │  │
│  │  Balance:   $125,432.10         Symbol: EURUSD                      │  │
│  │  Equity:    $126,789.45         Price:  1.0875                      │  │
│  │  Daily PnL: +$1,234.56 (+1.2%)   Change: +0.15%                      │  │
│  │  Margin:    $15,000 (12%)       Volume: 12.5M                       │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  📈 OPEN POSITIONS                         🔔 ACTIVE SIGNALS          │  │
│  │  ───────────────────                      ────────────────            │  │
│  │  ┌──────┬──────┬───────┬────────┬─────────┬────────┐                │  │
│  │  │Ticket│Symbol│ Type  │ Volume │   PnL   │  SL/TP │                │  │
│  │  ├──────┼──────┼───────┼────────┼─────────┼────────┤                │  │
│  │  │123456│EURUSD│  BUY  │  1.00  │ +$125.00│1.075/1.10│               │  │
│  │  │123457│GBPUSD│  BUY  │  0.50  │ +$78.50 │1.265/1.28│               │  │
│  │  │123458│USDJPY│  SELL │  0.75  │ -$45.00 │149.5/147 │               │  │
│  │  └──────┴──────┴───────┴────────┴─────────┴────────┘                │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  🕯️ LIVE CHART (EURUSD, 1m)                                          │  │
│  │  ───────────────────────────────────────────────────────────────────  │  │
│  │                                                                     │  │
│  │        ┌───┐              ┌───┐         __                          │  │
│  │     ┌──┘   └──┐   ┌───┐ ┌───┐       ████  ╱                         │  │
│  │     │  █████  │   │   │ │   │      ███████╱                          │  │
│  │  ───┘   └──┘   └───┘ └───┘  └───     █████                            │  │
│  │     14:30   14:45  15:00  15:15    15:30                             │  │
│  │                                                                     │  │
│  │  Indicators: RSI(14)=65 │ MACD=+0.002 │ ATR=0.0085                    │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  🎯 STRATEGY SIGNALS (34 Total)                                       │  │
│  │  ───────────────────────────────────────────────────────────────────  │  │
│  │                                                                     │  │
│  │  Layer 1: Retail/SMC (18)  │  BUY:12  │  HOLD:4  │  SELL:2           │  │
│  │  Layer 2: Quantitative (6) │  BUY:4   │  HOLD:1  │  SELL:1           │  │
│  │  Layer 3: Legendary (10)   │  BUY:6   │  HOLD:2  │  SELL:2           │  │
│  │                                                                     │  │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │  📊 CONSENSUS: BUY (72% confidence)  │  Final Signal: 🟢 BUY        │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  [A] Analyze All  [R] Refresh  [O] Orders  [S] Settings  [Q] Quit          │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Last Update: 2026-01-16 15:30:45  │  Status: CONNECTED  │  MT5: ONLINE    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Live Chart Implementation (ASCII/Unicode)

```python
class LiveChart:
    """ASCII/Unicode candlestick chart for terminal"""
    
    def __init__(self, width: int = 80, height: int = 20):
        self.width = width
        self.height = height
        self.candles = []
    
    def add_candle(self, open_p: float, high: float, low: float, close: float, time: str):
        """Add new candle"""
        self.candles.append({
            'open': open_p,
            'high': high,
            'low': low,
            'close': close,
            'time': time
        })
        # Keep only last N candles
        if len(self.candles) > self.width:
            self.candles = self.candles[-self.width:]
    
    def render(self) -> str:
        """Render chart as string"""
        if not self.candles:
            return "No data"
        
        # Find price range
        min_price = min(c['low'] for c in self.candles)
        max_price = max(c['high'] for c in self.candles)
        price_range = max_price - min_price
        if price_range == 0:
            price_range = 1
        
        # Render each row
        lines = []
        for row in range(self.height - 1, -1, -1):
            price_level = min_price + (row / self.height) * price_range
            line = ""
            
            for candle in self.candles:
                # Determine candle character
                if candle['close'] >= candle['open']:
                    body_top = candle['close']
                    body_bottom = candle['open']
                    color_char = "🟢"
                else:
                    body_top = candle['open']
                    body_bottom = candle['close']
                    color_char = "🔴"
                
                # Check what this row represents
                if price_level >= body_bottom and price_level <= body_top:
                    # Body
                    line += color_char
                elif price_level >= candle['low'] and price_level <= candle['high']:
                    # Wick only
                    line += "│"
                elif row == self.height - 1:
                    line += "●"  # Top indicator
                elif row == 0:
                    line += "○"  # Bottom indicator
                else:
                    line += " "
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def render_simple(self) -> str:
        """Simpler bar chart for limited terminal"""
        if not self.candles:
            return "No data"
        
        # Normalize prices
        closes = [c['close'] for c in self.candles]
        min_p, max_p = min(closes), max(closes)
        rng = max_p - min_p or 1
        
        lines = []
        for c in self.candles[-40:]:  # Last 40 candles
            bar_len = int((c['close'] - min_p) / rng * 20)
            if c['close'] >= c['open']:
                lines.append(f"🟢 {'█' * bar_len}")
            else:
                lines.append(f"🔴 {'█' * bar_len}")
        
        return "\n".join(lines)
```

---

## 7. System Interaction Modes

### 7.1 Mode Definitions

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from datetime import datetime

class TradingMode(Enum):
    """Trading mode options"""
    MANUAL = "manual"       # View only, no auto analysis
    SEMI_AUTO = "semi"      # Auto analysis, manual confirmation
    FULL_AUTO = "auto"      # Full autonomous trading

@dataclass
class ModeConfig:
    """Configuration for each mode"""
    auto_analyze: bool
    auto_signal: bool
    auto_execute: bool
    require_confirmation: bool
    notify_user: bool
    
    @classmethod
    def manual(cls):
        return ModeConfig(
            auto_analyze=False,
            auto_signal=False,
            auto_execute=False,
            require_confirmation=False,
            notify_user=True
        )
    
    @classmethod
    def semi_auto(cls):
        return ModeConfig(
            auto_analyze=True,
            auto_signal=True,
            auto_execute=False,
            require_confirmation=True,
            notify_user=True
        )
    
    @classmethod
    def full_auto(cls):
        return ModeConfig(
            auto_analyze=True,
            auto_signal=True,
            auto_execute=True,
            require_confirmation=False,
            notify_user=False
        )


class ModeManager:
    """Manage trading modes"""
    
    def __init__(self):
        self.current_mode = TradingMode.SEMI_AUTO
        self.config = ModeConfig.semi_auto()
        self.mode_history: List[dict] = []
    
    def set_mode(self, mode: TradingMode):
        """Change trading mode"""
        self.current_mode = mode
        self.config = {
            TradingMode.MANUAL: ModeConfig.manual(),
            TradingMode.SEMI_AUTO: ModeConfig.semi_auto(),
            TradingMode.FULL_AUTO: ModeConfig.full_auto()
        }[mode]
        
        self.mode_history.append({
            'timestamp': datetime.now().isoformat(),
            'mode': mode.value,
            'config': self.config.__dict__
        })
    
    def can_execute(self) -> bool:
        """Check if auto-execution is allowed"""
        return self.config.auto_execute
    
    def should_confirm(self) -> bool:
        """Check if user confirmation is required"""
        return self.config.require_confirmation
    
    def should_analyze(self) -> bool:
        """Check if auto-analysis is enabled"""
        return self.config.auto_analyze
```

### 7.2 Mode-Specific Workflows

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MODE WORKFLOWS                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │  MODE: MANUAL (View Only)                                        │      │
│  │  ───────────────────────────────                                  │      │
│  │                                                                 │      │
│  │  User starts system                                              │      │
│  │       │                                                         │      │
│  │       ▼                                                         │      │
│  │  ┌─────────────────┐                                            │      │
│  │  │  Manual Request │◀─── User triggers analysis                 │      │
│  │  └────────┬────────┘                                            │      │
│  │           │                                                     │      │
│  │           ▼                                                     │      │
│  │  ┌─────────────────┐                                            │      │
│  │  │  Show Results   │◀─── Display signals, no execution          │      │
│  │  └─────────────────┘                                            │      │
│  │                                                                 │      │
│  │  User must manually execute trades via broker terminal          │      │
│  └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │  MODE: SEMI-AUTO (Recommended)                                   │      │
│  │  ────────────────────────────────────────                        │      │
│  │                                                                 │      │
│  │  System runs continuously                                       │      │
│  │       │                                                         │      │
│  │       ▼                                                         │      │
│  │  ┌─────────────────┐                                            │      │
│  │  │  Auto Analysis  │───▶ Update all strategies                  │      │
│  │  └────────┬────────┘                                            │      │
│  │           │                                                     │      │
│  │           ▼                                                     │      │
│  │  ┌─────────────────┐                                            │      │
│  │  │  Generate Signal │───▶ BUY/SELL/HOLD                         │      │
│  │  └────────┬────────┘                                            │      │
│  │           │                                                     │      │
│  │           ▼                                                     │      │
│  │  ┌─────────────────┐     ┌─────────────────┐                    │      │
│  │  │  Show to User   │────▶│  Wait for       │                    │      │
│  │  └─────────────────┘     │  Confirmation   │                    │      │
│  │                          └───────┬─────────┘                    │      │
│  │                                  │                              │      │
│  │                     User clicks │ CONFIRM or CANCEL             │      │
│  │                                  │                              │      │
│  │              ┌───────────────────┴──────────────┐               │      │
│  │              │                                  │               │      │
│  │              ▼ CONFIRM                         ▼ CANCEL        │      │
│  │  ┌─────────────────────────┐      ┌─────────────────┐          │      │
│  │  │  Execute Trade         │      │  Log cancelled  │          │      │
│  │  │  - Place order         │      │  - Update stats │          │      │
│  │  │  - Update portfolio    │      │  - Continue     │          │      │
│  │  │  - Notify user         │      └─────────────────┘          │      │
│  │  └─────────────────────────┘                                 │      │
│  └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │  MODE: FULL AUTO (High Risk)                                    │      │
│  │  ─────────────────────────────────────                          │      │
│  │                                                                 │      │
│  │  System runs autonomously                                      │      │
│  │       │                                                         │      │
│  │       ▼                                                         │      │
│  │  ┌─────────────────┐                                            │      │
│  │  │  Auto Analysis  │───▶ Continuous analysis                    │      │
│  │  └────────┬────────┘                                            │      │
│  │           │                                                     │      │
│  │           ▼                                                     │      │
│  │  ┌─────────────────┐                                            │      │
│  │  │  Risk Check     │───▶ Validate against limits                │      │
│  │  └────────┬────────┘                                            │      │
│  │           │                                                     │      │
│  │           ▼                                                     │      │
│  │  ┌─────────────────┐     ┌─────────────────┐                    │      │
│  │  │  Execute Trade  │────▶│  Update         │                    │      │
│  │  │  (No confirm)   │     │  portfolio/PnL  │                    │      │
│  │  └─────────────────┘     └─────────────────┘                    │      │
│  │                                                                 │      │
│  │  ⚠️  WARNING: High risk! Monitor closely.                       │      │
│  │  ⚠️  Set stop limits and monitoring alerts.                     │      │
│  └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Execution Controller

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum
import asyncio

class ExecutionStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    EXECUTED = "EXECUTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

@dataclass
class TradeProposal:
    """Proposed trade from analysis"""
    timestamp: datetime
    symbol: str
    side: str  # BUY/SELL
    volume: float
    entry_price: float
    sl: Optional[float]
    tp: Optional[float]
    confidence: float
    strategy: str
    reasoning: List[str]
    status: ExecutionStatus = ExecutionStatus.PENDING

class ExecutionController:
    """Controller for trade execution based on mode"""
    
    def __init__(self, mode_manager: ModeManager, broker, notifier=None):
        self.mode_manager = mode_manager
        self.broker = broker
        self.notifier = notifier
        self.pending_proposals: List[TradeProposal] = []
        self.executed_trades: List[TradeProposal] = []
        self.cancelled_trades: List[TradeProposal] = []
        self.execution_callbacks: List[Callable] = []
    
    async def process_signal(self, proposal: TradeProposal) -> dict:
        """
        Process trading signal based on current mode
        
        Returns:
            dict with execution result
        """
        mode = self.mode_manager.current_mode
        
        if mode == TradingMode.MANUAL:
            # Just log and notify
            return await self._handle_manual(proposal)
        
        elif mode == TradingMode.SEMI_AUTO:
            # Add to pending, wait for confirmation
            return await self._handle_semi_auto(proposal)
        
        elif mode == TradingMode.FULL_AUTO:
            # Auto execute
            return await self._handle_full_auto(proposal)
    
    async def _handle_manual(self, proposal: TradeProposal) -> dict:
        """Manual mode: Notify user, wait for manual action"""
        self.pending_proposals.append(proposal)
        
        # Notify user
        if self.notifier:
            await self.notifier.notify_trade_proposal(proposal)
        
        return {
            "status": "PENDING_USER_ACTION",
            "proposal": proposal,
            "message": "Signal generated. Execute manually via broker terminal."
        }
    
    async def _handle_semi_auto(self, proposal: TradeProposal) -> dict:
        """Semi-auto mode: Require confirmation"""
        # Check if we should auto-execute based on confidence
        if proposal.confidence >= 0.85:
            # High confidence - auto approve
            proposal.status = ExecutionStatus.APPROVED
            return await self._execute_trade(proposal)
        else:
            # Medium confidence - add to pending for confirmation
            self.pending_proposals.append(proposal)
            
            # Notify user
            if self.notifier:
                await self.notifier.request_confirmation(proposal)
            
            return {
                "status": "PENDING_CONFIRMATION",
                "proposal": proposal,
                "message": f"Signal confidence: {proposal.confidence:.0%}. Confirm execution?"
            }
    
    async def _handle_full_auto(self, proposal: TradeProposal) -> dict:
        """Full auto mode: Execute immediately"""
        # Quick risk check
        risk_ok = await self._check_risk_limits(proposal)
        if not risk_ok:
            proposal.status = ExecutionStatus.REJECTED
            return {
                "status": "REJECTED",
                "reason": "Risk limit exceeded",
                "proposal": proposal
            }
        
        proposal.status = ExecutionStatus.APPROVED
        return await self._execute_trade(proposal)
    
    async def _execute_trade(self, proposal: TradeProposal) -> dict:
        """Execute the trade"""
        try:
            # Place order via broker
            result = self.broker.place_order(
                symbol=proposal.symbol,
                action=proposal.side,
                volume=proposal.volume,
                stop_loss=proposal.sl,
                take_profit=proposal.tp
            )
            
            proposal.status = ExecutionStatus.EXECUTED
            self.executed_trades.append(proposal)
            
            # Notify
            if self.notifier:
                await self.notifier.notify_execution(proposal, result)
            
            # Callback
            for callback in self.execution_callbacks:
                callback(proposal, result)
            
            return {
                "status": "EXECUTED",
                "order_id": result.get("order"),
                "proposal": proposal
            }
            
        except Exception as e:
            proposal.status = ExecutionStatus.REJECTED
            return {
                "status": "ERROR",
                "error": str(e),
                "proposal": proposal
            }
    
    async def confirm_proposal(self, proposal_id: int, confirm: bool):
        """Confirm or reject pending proposal"""
        for i, prop in enumerate(self.pending_proposals):
            if i == proposal_id:
                if confirm:
                    prop.status = ExecutionStatus.APPROVED
                    return await self._execute_trade(prop)
                else:
                    prop.status = ExecutionStatus.CANCELLED
                    self.cancelled_trades.append(prop)
                    self.pending_proposals.pop(i)
                    return {"status": "CANCELLED", "proposal": prop}
        
        return {"status": "NOT_FOUND"}
    
    async def _check_risk_limits(self, proposal: TradeProposal) -> bool:
        """Check if trade is within risk limits"""
        # Implement risk checks:
        # - Max position size
        # - Max daily loss
        # - Max correlation
        # - Max drawdown
        return True
    
    def add_execution_callback(self, callback: Callable):
        """Add callback for trade execution"""
        self.execution_callbacks.append(callback)
```

---

## 8. Architecture Overview (Complete)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        AI QUANT HEDGE FUND v2.0 - COMPLETE ARCHITECTURE        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                         USER INTERFACE LAYER                             │ │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────────────────┐ │ │
│  │  │  TERMINAL UI  │  │  WEBUI (Opt)  │  │  REST API + WebSocket        │ │ │
│  │  │  (Textual)    │  │(Streamlit)    │  │  (for external access)      │ │ │
│  │  │  • Dashboard  │  │  • Charts     │  │  • GET /portfolio           │ │ │
│  │  │  • Live Chart │  │  • Analytics  │  │  │ POST /execute              │ │ │
│  │  │  • Controls   │  │  • Settings   │  │  │ WS /updates                │ │ │
│  │  └───────┬───────┘  └───────┬───────┘  └───────────────┬───────────────┘ │ │
│  └──────────┼──────────────────┼───────────────────────────┼─────────────────┘ │
│             │                  │                           │                   │
│             └──────────────────┼───────────────────────────┘                   │
│                                │                                               │
│  ┌──────────────────────────────▼───────────────────────────────────────────┐ │
│  │                          CORE LAYER                                      │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐  │ │
│  │  │                    TRADING ENGINE                                  │  │ │
│  │  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │  │ │
│  │  │  │  ANALYSIS ENGINE │  │ DECISION ENGINE  │  │ EXECUTION ENGINE │  │  │ │
│  │  │  │  • 34+ Strategies│  │ • Signal Aggre-  │  │ • Order Manager  │  │  │ │
│  │  │  │  • Multi-TF     │  │   gation        │  │ • Risk Check     │  │  │ │
│  │  │  │  • Indicators   │  │ • Confidence    │  │ • Broker Connect │  │  │ │
│  │  │  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  │  │ │
│  │  │           │                     │                     │            │  │ │
│  │  │           └─────────────────────┼─────────────────────┘            │  │ │
│  │  │                                 │                                  │  │ │
│  │  │  ┌──────────────────────────────▼──────────────────────────────┐   │  │ │
│  │  │  │              MODE MANAGER & EXECUTION CONTROLLER          │   │  │ │
│  │  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐   │   │  │ │
│  │  │  │  │ MANUAL  │  │ SEMI    │  │  FULL   │  │  NOTIFIER   │   │   │  │ │
│  │  │  │  │         │  │ AUTO    │  │  AUTO   │  │  (Telegram) │   │   │  │ │
│  │  │  │  └─────────┘  └─────────┘  └─────────┘  └─────────────┘   │   │  │ │
│  │  │  └────────────────────────────────────────────────────────────┘   │  │ │
│  │  └────────────────────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                     │                                          │
│  ┌──────────────────────────────────▼──────────────────────────────────────┐ │
│  │                          DATA & CONNECTIONS                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │ │
│  │  │  METATRADER5 │  │   ALPACA     │  │   BINANCE   │  │   CCXT     │  │ │
│  │  │  (MT5)       │  │   API        │  │   API       │  │   (Multi)  │  │ │
│  │  │  • Forex/CFD │  │  • US Stocks │  │  • Crypto   │  │  • Universal│  │ │
│  │  │  • WebSocket │  │  • WebSocket │  │  • WebSocket│  │  • Unified │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │ │
│  │                                                                         │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐  │ │
│  │  │ DATA PROVIDER│  │ PORTFOLIO    │  │  MEMORY & STATISTICS        │  │ │
│  │  │  • Yahoo     │  │  MANAGER     │  │  • BacktestMemory          │  │ │
│  │  │  • CoinGecko │  │  • PnL Calc  │  │  • InteractionLogger      │  │ │
│  │  │  • Forex API │  │  • Position  │  │  • StatisticsManager     │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Implementation Plan

### Phase 1: Core Infrastructure (Week 1-2)

| Task | Duration | Dependencies | Priority |
|------|----------|--------------|----------|
| Implement `MT5Broker` class | 3 days | None | HIGH |
| Implement `Portfolio` data model | 2 days | None | HIGH |
| Implement `RealTimePortfolioMonitor` | 2 days | MT5Broker | HIGH |
| Implement `ModeManager` | 1 day | None | HIGH |
| Create `ExecutionController` | 2 days | ModeManager | HIGH |
| Setup WebSocket server for portfolio | 2 days | PortfolioMonitor | MEDIUM |

### Phase 2: UI Development (Week 3-4)

| Task | Duration | Dependencies | Priority |
|------|----------|--------------|----------|
| Implement `LiveChart` (ASCII) | 2 days | None | MEDIUM |
| Create TUI Dashboard (Textual) | 4 days | LiveChart | HIGH |
| Create Streamlit Dashboard (optional) | 3 days | None | LOW |
| Add WebSocket API endpoints | 2 days | WebSocket server | MEDIUM |

### Phase 3: Integration & Testing (Week 5-6)

| Task | Duration | Dependencies | Priority |
|------|----------|--------------|----------|
| Integrate all components | 3 days | All Phase 1&2 | HIGH |
| Test with MT5 demo account | 2 days | Integration | HIGH |
| Test all 3 modes | 2 days | Integration | HIGH |
| Performance testing | 2 days | Testing | MEDIUM |
| Documentation | 2 days | All | MEDIUM |

### Phase 4: Polish & Deploy (Week 7-8)

| Task | Duration | Dependencies | Priority |
|------|----------|--------------|----------|
| Bug fixes & optimization | 3 days | Testing | HIGH |
| User guide documentation | 2 days | All | HIGH |
| Deployment configuration | 2 days | None | MEDIUM |
| Final testing & release | 2 days | All | HIGH |

---

## 10. Research References

### 10.1 MT5 Integration

| Source | URL | Key Features |
|--------|-----|--------------|
| MetaTrader5 Python | https://github.com/Metatrader5/Python | Official Python binding |
| MetaTrader5 Official Docs | https://www.mql5.com/en/docs/python | Full API documentation |
| DWX ZeroMQ Connector | https://github.com/darwinex/dwx-zeromq-connector | Network-based communication |
| MT5 Docker | https://github.com/nevmerzhitsky/headless-metatrader4 | Headless container |

### 10.2 WebSocket & Real-time Data

| Source | URL | Key Features |
|--------|-----|--------------|
| Binance WebSocket | https://github.com/binance/binance-connector-python | Real-time crypto data |
| Alpaca Streams | https://github.com/alpacahq/alpaca-trade-api-python | Stock data streaming |
| CCXT Pro WebSocket | https://github.com/ccxt/ccxt.pro.manual.md | Multi-exchange streaming |

### 10.3 Trading UI Frameworks

| Source | URL | Key Features |
|--------|-----|--------------|
| Textual TUI | https://textual.textualize.io/ | Modern Python TUI framework |
| Rich Library | https://rich.readthedocs.io/ | Terminal output formatting |
| Streamlit | https://streamlit.io/ | Quick data dashboards |
| Plotly | https://plotly.com/python/ | Interactive charts |

### 10.4 Academic Papers

| Paper | Authors | Key Contributions |
|-------|---------|------------------|
| Neural Network-Based Algorithmic Trading Systems | Zhang Wei (2025) | Multi-timeframe analysis, high-frequency execution |
| Orchestration Framework for Financial Agents | Li et al. (2025) | Agentic trading framework, FinAgent |
| AI Hedge Fund | virattt (2025) | Production multi-agent trading system |

### 10.5 Open Source References

| Project | URL | Key Features |
|---------|-----|--------------|
| AutoTrader | https://github.com/kieran-mackle/AutoTrader | Complete trading framework |
| Freqtrade | https://github.com/freqtrade/freqtrade | Open source crypto bot |
| FinRL | https://github.com/AI4Finance-Foundation/FinRL | Deep reinforcement learning trading |
| QuantConnect | https://github.com/QuantConnect/Lean | Algorithmic trading platform |

---

## 11. Checklist

### MT5 Integration
- [ ] Implement MT5Broker class
- [ ] Add order placement
- [ ] Add position management
- [ ] Add account info retrieval
- [ ] Implement ZeroMQ alternative
- [ ] Add connection monitoring
- [ ] Test with demo account

### Portfolio & PnL
- [ ] Implement Position class
- [ ] Implement Trade class
- [ ] Implement Portfolio class
- [ ] Create RealTimePortfolioMonitor
- [ ] Implement WebSocket server
- [ ] Add statistics calculation

### Multi-Timeframe
- [ ] Define Timeframe enum
- [ ] Implement MultiTimeframeAnalyzer
- [ ] Add HTF trend detection
- [ ] Create signal combination logic
- [ ] Implement live data streaming

### UI/UX
- [ ] Decide on UI approach (Hybrid)
- [ ] Implement LiveChart (ASCII)
- [ ] Create Textual TUI Dashboard
- [ ] Create Streamlit Dashboard (optional)
- [ ] Add WebSocket API

### Modes
- [ ] Define TradingMode enum
- [ ] Implement ModeManager
- [ ] Implement ExecutionController
- [ ] Add confirmation workflow
- [ ] Test all 3 modes

### Documentation
- [ ] Update README.md
- [ ] Update CHANGELOG.md
- [ ] Update AGENTS.md
- [ ] Create user guide
- [ ] Create API documentation

---

**Document Version**: 2.0-ADDENDUM
**Last Updated**: 2026-01-16
**Next Review**: 2026-01-23
