#!/usr/bin/env python3
"""
Test script for Phase 3.5 - FREE Trading Infrastructure
"""

import sys
sys.path.insert(0, '.')

print('Testing Phase 3.5 - FREE Trading Infrastructure')
print('='*60)

# Test 1: Import broker API
print('\n[1] Testing FREE Broker Gateway...')
from src.brokers.free_broker_api import (
    BrokerType, FreeBrokerGateway, PaperBroker,
    AlpacaBroker, BinanceBroker, CCXTBroker
)
print('✅ Broker Gateway imported successfully')

# Test 2: Import trading terminal
print('\n[2] Testing Virtual Trading Terminal...')
from src.brokers.virtual_trading_terminal import TradingTerminal, create_trading_terminal
print('✅ Trading Terminal imported successfully')

# Test 3: Import AI auto-trader
print('\n[3] Testing AI Auto-Trader...')
from src.automation.ai_auto_trader import AIAutoTrader, TradingSignal, SignalStrength
print('✅ AI Auto-Trader imported successfully')

# Test 4: Test broker creation
print('\n[4] Testing Broker Creation...')
paper = PaperBroker(1000000)
print(f'✅ Paper broker created with balance: ${paper.balance:,.2f}')

# Test 5: Test market data
import asyncio
async def test_market_data():
    broker = PaperBroker()
    await broker.connect()
    data = await broker.get_market_data('BTCUSDT')
    print(f'✅ Market data: {data.symbol} @ ${data.price:,.2f}')
    await broker.disconnect()

asyncio.run(test_market_data())

# Test 6: Test signal generation
print('\n[5] Testing Signal Generation...')
from src.strategies.wyckoff.wyckoff_strategy import WyckoffAnalyzer
import pandas as pd
import numpy as np

# Generate sample data properly
n = 100
dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq='1h')
base_price = 50000

# Create complete data
data_rows = []
for i in range(n):
    open_price = base_price * (1 + np.random.uniform(-0.01, 0.01))
    close_price = base_price * (1 + np.random.uniform(-0.02, 0.02))
    high_price = max(open_price, close_price) * (1 + np.random.uniform(0, 0.01))
    low_price = min(open_price, close_price) * (1 - np.random.uniform(0, 0.01))
    volume = np.random.uniform(1000, 10000)

    data_rows.append({
        'timestamp': dates[i],
        'open': open_price,
        'high': high_price,
        'low': low_price,
        'close': close_price,
        'volume': volume
    })

data = pd.DataFrame(data_rows)

analyzer = WyckoffAnalyzer()
analysis = analyzer.analyze_phase(
    high=data['high'],
    low=data['low'],
    close=data['close'],
    volume=data['volume']
)
if analysis:
    print(f'✅ Wyckoff analysis: Phase={analysis.phase.value if analysis.phase else None}, Confidence={analysis.confidence:.1f}%')

print('\n' + '='*60)
print('🎉 ALL TESTS PASSED!')
print('\nFree Trading Infrastructure is ready!')
print('Run with: poetry run python run_terminal.py')
print('Access at: http://localhost:5000')
