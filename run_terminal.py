#!/usr/bin/env python3
"""
AI Hedge Fund - Virtual Trading Terminal Launcher

This launches our FREE, fully autonomous trading terminal
that replaces expensive MetaTrader API subscriptions.

Features:
- Web-based interface (accessible from any browser)
- AI-powered signal generation
- Multi-broker support (Alpaca, Binance, OANDA - all FREE)
- Autonomous trading capabilities
- Real-time market data
- Portfolio management
- Performance analytics
"""

import sys
import os
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.brokers.virtual_trading_terminal import create_trading_terminal
from src.automation.ai_auto_trader import create_auto_trader
from src.utils.logger import setup_logger, get_logger

logger = setup_logger("Terminal", level="INFO")


def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   🤖  AI HEDGE FUND - VIRTUAL TRADING TERMINAL  🤖               ║
    ║                                                                   ║
    ║   ✓ 100% FREE - No MetaTrader API subscription required!         ║
    ║   ✓ Multi-broker support (Alpaca, Binance, OANDA)                ║
    ║   ✓ AI-powered autonomous trading                                ║
    ║   ✓ Wyckoff + Multi-Timeframe analysis                           ║
    ║   ✓ Web-based interface                                          ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝

    """
    print(banner)


def main():
    print_banner()

    logger.info("🚀 Starting AI Hedge Fund Virtual Trading Terminal...")
    logger.info("📡 No paid MetaTrader API needed - we're building our own!")

    app, socketio, terminal = create_trading_terminal()

    auto_trader = create_auto_trader()

    logger.info("✅ Terminal initialized successfully!")
    logger.info("🌐 Starting web server...")

    print("\n" + "="*60)
    print("🌐 TRADING TERMINAL READY!")
    print("="*60)
    print("\n📍 Access the terminal at:")
    print("   http://localhost:5000")
    print("\n🔧 Features:")
    print("   • Live market data streaming")
    print("   • AI-powered signal analysis")
    print("   • One-click order execution")
    print("   • Autonomous trading mode")
    print("   • Portfolio management")
    print("   • Performance analytics")
    print("\n🛑 Press Ctrl+C to stop\n")

    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down terminal...")
        sys.exit(0)


if __name__ == "__main__":
    main()
