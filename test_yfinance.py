#!/usr/bin/env python3
"""Test yfinance with real market data"""

try:
    import yfinance as yf
    print('✅ yfinance imported successfully')

    # Test real data fetch
    print('📊 Testing real data fetch for AAPL...')
    data = yf.download('AAPL', period='5d', interval='1d')
    print(f'✅ Data retrieved: {len(data)} rows')
    if not data.empty:
        latest_price = float(data["Close"].iloc[-1])
        print(f'Latest price: ${latest_price:.2f}')
        print(f'Data columns: {list(data.columns)}')
        print('✅ Real market data working!')
    else:
        print('❌ No data received')

except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()