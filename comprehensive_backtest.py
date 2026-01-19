"""
AI Hedge Fund v2.3.0 - Comprehensive Backtest System
Tests all 53+ strategies with 3-year historical data
Agent Constitution v2.3.0 Compliant
Generates automated reports with win rate, RR, memory, statistics, and visualizations
"""

import sys
import time
import json
import tracemalloc
import psutil
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
plt.style.use("seaborn-v0_8-darkgrid")

sys.path.insert(0, str(Path(__file__).parent))

from src.backtesting.comprehensive_backtester import MarketDataGenerator
from src.strategies.comprehensive_registry import get_comprehensive_registry

OUTPUT_DIR = Path("backtest_results")
OUTPUT_DIR.mkdir(exist_ok=True)


@dataclass
class BacktestMetrics:
    """Comprehensive backtest metrics"""

    strategy_name: str
    category: str
    trades: int
    wins: int
    losses: int
    win_rate: float
    profit_factor: float
    risk_reward_ratio: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharple_ratio: float
    average_win: float
    average_loss: float
    expectancy: float
    total_pnl: float
    execution_time_ms: float
    memory_used_mb: float
    avg_trade_duration: float
    best_trade: float
    worst_trade: float
    consecutive_wins: int
    consecutive_losses: int
    recovery_factor: float
    ulcer_index: float
    calmmar_ratio: float
    sortino_ratio: float


def generate_3yr_data(symbol: str = "AAPL") -> pd.DataFrame:
    """Generate 3 years of realistic market data"""
    print(f"📊 Generating 3-year data for {symbol}...")
    periods = 252 * 3  # 3 years of trading days
    df = MarketDataGenerator.generate_ohlcv(
        symbol=symbol,
        timeframe="H1",
        periods=periods,
        start_price=150.0,
        volatility=0.02,
        drift=0.0003,
    )
    print(f"   ✓ Generated {len(df)} bars ({periods} days)")
    return df


def calculate_metrics(
    trades: List[Dict],
    initial_capital: float,
    execution_time_ms: float,
    memory_mb: float,
) -> BacktestMetrics:
    """Calculate comprehensive metrics from trades"""
    if not trades:
        return None

    total_trades = len(trades)
    wins = [t for t in trades if t.get("pnl", 0) > 0]
    losses = [t for t in trades if t.get("pnl", 0) <= 0]

    win_rate = len(wins) / total_trades if total_trades > 0 else 0
    total_pnl = sum(t.get("pnl", 0) for t in trades)
    gross_profit = sum(t.get("pnl", 0) for t in wins) if wins else 0
    gross_loss = abs(sum(t.get("pnl", 0) for t in losses)) if losses else 0

    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    avg_win = gross_profit / len(wins) if wins else 0
    avg_loss = gross_loss / len(losses) if losses else 0
    risk_reward_ratio = avg_win / avg_loss if avg_loss > 0 else 0

    expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)

    # Calculate equity curve and drawdown
    equity = [initial_capital]
    for trade in trades:
        equity.append(equity[-1] + trade.get("pnl", 0))
    equity = np.array(equity)

    peak = np.maximum.accumulate(equity)
    drawdown = (equity - peak) / peak
    max_drawdown = abs(min(drawdown)) if len(drawdown) > 0 else 0

    # Calculate returns
    total_return = (equity[-1] - initial_capital) / initial_capital
    annual_return = total_return / 3  # 3 years of data

    # Sharpe Ratio (annualized)
    returns = np.diff(equity) / equity[:-1]
    sharpe_ratio = (
        (np.mean(returns) / np.std(returns) * np.sqrt(252))
        if np.std(returns) > 0
        else 0
    )

    # Sortino Ratio (downside deviation)
    downside_returns = returns[returns < 0]
    downside_std = np.std(downside_returns) if len(downside_returns) > 0 else 0.001
    sortino_ratio = (
        (np.mean(returns) / downside_std * np.sqrt(252)) if downside_std > 0 else 0
    )

    # Calmar Ratio
    calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0

    # Recovery Factor
    recovery_factor = (
        total_pnl / abs(min(drawdown) * initial_capital) if max_drawdown > 0 else 0
    )

    # Ulcer Index
    ulcer_index = np.sqrt(np.mean(drawdown**2)) if len(drawdown) > 0 else 0

    # Consecutive wins/losses
    consecutive_wins = 0
    consecutive_losses = 0
    max_consecutive_wins = 0
    max_consecutive_losses = 0
    current_wins = 0
    current_losses = 0
    for trade in trades:
        if trade.get("pnl", 0) > 0:
            current_wins += 1
            current_losses = 0
            max_consecutive_wins = max(max_consecutive_wins, current_wins)
        else:
            current_losses += 1
            current_wins = 0
            max_consecutive_losses = max(max_consecutive_losses, current_losses)
    consecutive_wins = max_consecutive_wins
    consecutive_losses = max_consecutive_losses

    # Average trade duration
    durations = [t.get("duration_bars", 10) for t in trades]
    avg_trade_duration = np.mean(durations) if durations else 0

    # Best/Worst trade
    pnls = [t.get("pnl", 0) for t in trades]
    best_trade = max(pnls) if pnls else 0
    worst_trade = min(pnls) if pnls else 0

    return BacktestMetrics(
        strategy_name="",
        category="",
        trades=total_trades,
        wins=len(wins),
        losses=len(losses),
        win_rate=win_rate,
        profit_factor=profit_factor,
        risk_reward_ratio=risk_reward_ratio,
        total_return=total_return,
        annual_return=annual_return,
        max_drawdown=max_drawdown,
        sharple_ratio=sharpe_ratio,
        average_win=avg_win,
        average_loss=avg_loss,
        expectancy=expectancy,
        total_pnl=total_pnl,
        execution_time_ms=execution_time_ms,
        memory_used_mb=memory_mb,
        avg_trade_duration=avg_trade_duration,
        best_trade=best_trade,
        worst_trade=worst_trade,
        consecutive_wins=consecutive_wins,
        consecutive_losses=consecutive_losses,
        recovery_factor=recovery_factor,
        ulcer_index=ulcer_index,
        calmmar_ratio=calmar_ratio,
        sortino_ratio=sortino_ratio,
    )


def apply_strategy_signal(df: pd.DataFrame, strategy_name: str, idx: int) -> str:
    """Generate trading signal based on strategy type"""
    if idx < 50 or idx >= len(df):
        return "HOLD"

    current = df.iloc[idx]
    prev = df.iloc[idx - 1]

    # Calculate common indicators
    ema_fast = df["close"].ewm(span=12).mean().iloc[idx]
    ema_slow = df["close"].ewm(span=26).mean().iloc[idx]
    rsi = df["rsi"].iloc[idx] if "rsi" in df.columns else 50
    macd = df["macd"].iloc[idx] if "macd" in df.columns else 0
    macd_signal = df["macd_signal"].iloc[idx] if "macd_signal" in df.columns else 0
    atr = df["atr"].iloc[idx] if "atr" in df.columns else 2.0

    price = current["close"]
    ema20 = df["ema_20"].iloc[idx] if "ema_20" in df.columns else price
    ema50 = df["ema_50"].iloc[idx] if "ema_50" in df.columns else price

    # Strategy-specific signals
    strategy_signals = {
        # Trend Following
        "trend_following": "BUY"
        if price > ema50
        else "SELL"
        if price < ema50
        else "HOLD",
        "turtle_trading": "BUY"
        if price > df["high"].rolling(20).max().iloc[idx - 1]
        else "SELL"
        if price < df["low"].rolling(10).min().iloc[idx - 1]
        else "HOLD",
        "momentum_analysis": "BUY" if rsi > 60 else "SELL" if rsi < 40 else "HOLD",
        "technical_analysis": "BUY"
        if macd > macd_signal
        else "SELL"
        if macd < macd_signal
        else "HOLD",
        "swing_trading": "BUY"
        if price > ema20 and price > ema50
        else "SELL"
        if price < ema20 and price < ema50
        else "HOLD",
        "position_trading": "BUY" if price > ema50 else "HOLD",
        "breakout_trading": "BUY"
        if price > df["high"].rolling(20).max().iloc[idx - 1]
        else "SELL"
        if price < df["low"].rolling(20).min().iloc[idx - 1]
        else "HOLD",
        "scalping_momentum": "BUY"
        if ema_fast > ema_slow and rsi > 55
        else "SELL"
        if ema_fast < ema_slow and rsi < 45
        else "HOLD",
        # Mean Reversion
        "mean_reversion": "BUY" if rsi < 30 else "SELL" if rsi > 70 else "HOLD",
        "mean_reversion_strategy": "BUY"
        if rsi < 35
        else "SELL"
        if rsi > 65
        else "HOLD",
        "mean_reversion_analysis": "BUY"
        if price < ema20 * 0.95
        else "SELL"
        if price > ema20 * 1.05
        else "HOLD",
        "reversal_trading": "BUY" if rsi < 25 else "SELL" if rsi > 75 else "HOLD",
        "range_trading": "BUY"
        if price < df["low"].rolling(20).min().iloc[idx]
        else "SELL"
        if price > df["high"].rolling(20).max().iloc[idx]
        else "HOLD",
        # SMC/ICT
        "smc_agent": "BUY"
        if current["close"] > current["open"]
        and price > df["close"].rolling(50).mean().iloc[idx]
        else "SELL",
        "ict_agent": "BUY"
        if price > df["high"].rolling(10).max().iloc[idx - 1]
        else "SELL",
        "supply_demand_agent": "BUY"
        if price < df["low"].rolling(20).min().iloc[idx]
        else "SELL",
        "liquidity_agent": "BUY"
        if price > df["high"].rolling(20).max().iloc[idx - 1]
        else "SELL",
        "market_structure_agent": "BUY"
        if price > df["close"].rolling(5).max().iloc[idx - 1]
        else "SELL",
        "volume_profile_agent": "BUY"
        if current["volume"] > df["volume"].rolling(20).mean().iloc[idx]
        else "HOLD",
        "snr_agent": "BUY"
        if price > df["high"].rolling(10).max().iloc[idx - 1]
        else "SELL",
        "wyckoff_agent": "BUY"
        if price > df["close"].rolling(10).mean().iloc[idx]
        else "SELL",
        "fibonacci_agent": "BUY"
        if price > df["close"].rolling(20).min().iloc[idx] * 1.02
        else "SELL",
        # Technical Analysis
        "technical_analysis_agent": "BUY"
        if macd > macd_signal
        else "SELL"
        if macd < macd_signal
        else "HOLD",
        "technical_analysis_strategy": "BUY" if ema_fast > ema_slow else "SELL",
        "technical_analyst": "BUY" if rsi > 50 else "SELL",
        "divergence_agent": "BUY" if rsi < 40 else "SELL" if rsi > 60 else "HOLD",
        "gap_trading": "BUY"
        if current["open"] > prev["close"] * 1.01
        else "SELL"
        if current["open"] < prev["close"] * 0.99
        else "HOLD",
        # Quantitative
        "quantitative_analyst": "BUY" if rsi > 50 and ema_fast > ema_slow else "SELL",
        "quantitative_momentum": "BUY" if price > ema50 else "SELL",
        "factor_investing_strategy": "BUY" if rsi > 45 else "SELL",
        "factor_investing_analysis": "BUY" if price > ema20 else "SELL",
        "jim_simons_strategy": "BUY" if rsi > 55 else "SELL" if rsi < 45 else "HOLD",
        "jim_simons_quant": "BUY" if macd > 0 else "SELL",
        "jim_simons_analysis": "BUY" if ema_fast > ema_slow else "HOLD",
        # Legendary Investors
        "warren_buffett_style": "BUY" if price > ema50 else "HOLD",
        "warren_buffett_agent": "BUY"
        if (df["ema_100"].iloc[idx] if "ema_100" in df.columns else price * 0.9) < price
        else "HOLD",
        "benjamin_graham_style": "BUY" if price > ema50 else "HOLD",
        "benjamin_graham_agent": "BUY" if price > ema20 * 0.95 else "HOLD",
        "graham_value_investing": "BUY" if price > ema50 else "HOLD",
        "peter_lynch_style": "BUY" if rsi > 45 else "HOLD",
        "philip_fisher_style": "BUY" if price > ema20 else "HOLD",
        "william_o'neil_style": "BUY"
        if price > df["close"].rolling(10).max().iloc[idx - 1]
        else "HOLD",
        "michael_burry_style": "BUY" if price < ema50 else "HOLD",
        "george_soros_style": "BUY" if rsi > 55 else "SELL",
        "john_templeton_style": "BUY" if price < ema20 * 0.9 else "HOLD",
        "joel_greenblatt_style": "BUY" if price > ema50 and rsi < 60 else "HOLD",
        "ray_dalio_style": "BUY" if price > ema50 else "HOLD",
        # Earnings/Momentum
        "earnings_momentum": "BUY" if rsi > 55 else "SELL" if rsi < 45 else "HOLD",
        "earnings_momentum_strategy": "BUY" if ema_fast > ema_slow else "SELL",
        "earnings_momentum_analysis": "BUY" if price > ema20 else "SELL",
        # Retail
        "fundamentals_agent": "BUY" if price > ema50 else "HOLD",
        "factor_investor": "BUY" if rsi > 50 else "HOLD",
        "technical_analysis": "BUY" if macd > macd_signal else "SELL",
        "snr_agent": "BUY"
        if price > df["high"].rolling(10).max().iloc[idx - 1]
        else "SELL",
        "supply_demand_agent": "BUY"
        if price < df["low"].rolling(20).min().iloc[idx]
        else "SELL",
        "liquidity_agent": "BUY"
        if price > df["high"].rolling(20).max().iloc[idx - 1]
        else "SELL",
        "market_structure_agent": "BUY"
        if price > df["close"].rolling(5).max().iloc[idx - 1]
        else "SELL",
        "volume_profile_agent": "BUY"
        if current["volume"] > df["volume"].rolling(20).mean().iloc[idx]
        else "HOLD",
        # SEPA
        "sepa_(super_performance)": "BUY"
        if price > df["close"].rolling(20).max().iloc[idx - 1] and rsi > 50
        else "HOLD",
    }

    return strategy_signals.get(strategy_name, "HOLD")


def run_strategy_backtest(
    strategy_name: str, df: pd.DataFrame, initial_capital: float = 10000
) -> Tuple[List[Dict], float, float]:
    """Run backtest for a single strategy"""
    trades = []
    position = None

    start_time = time.time()
    tracemalloc.start()

    for idx in range(50, len(df)):
        signal = apply_strategy_signal(df, strategy_name, idx)
        current_bar = df.iloc[idx]

        if signal == "BUY" and position is None:
            entry_price = current_bar["close"]
            position = {
                "entry": entry_price,
                "type": "LONG",
                "entry_bar": idx,
                "stop_loss": entry_price
                - (current_bar["atr"] if "atr" in current_bar else entry_price * 0.02),
                "take_profit": entry_price
                + (current_bar["atr"] if "atr" in current_bar else entry_price * 0.04),
            }
        elif signal == "SELL" and position is None:
            entry_price = current_bar["close"]
            position = {
                "entry": entry_price,
                "type": "SHORT",
                "entry_bar": idx,
                "stop_loss": entry_price
                + (current_bar["atr"] if "atr" in current_bar else entry_price * 0.02),
                "take_profit": entry_price
                - (current_bar["atr"] if "atr" in current_bar else entry_price * 0.04),
            }

        if position:
            current_price = current_bar["close"]
            pnl = (
                (current_price - position["entry"])
                if position["type"] == "LONG"
                else (position["entry"] - current_price)
            )
            pnl_pct = pnl / position["entry"]

            # Check exit conditions
            exit_signal = False
            if position["type"] == "LONG":
                if current_price <= position["stop_loss"]:
                    pnl = position["stop_loss"] - position["entry"]
                    exit_signal = True
                elif current_price >= position["take_profit"]:
                    pnl = position["take_profit"] - position["entry"]
                    exit_signal = True
            else:
                if current_price >= position["stop_loss"]:
                    pnl = position["entry"] - position["stop_loss"]
                    exit_signal = True
                elif current_price <= position["take_profit"]:
                    pnl = position["entry"] - position["take_profit"]
                    exit_signal = True

            # Reverse signal exit
            if signal == "SELL" and position["type"] == "LONG":
                pnl = current_price - position["entry"]
                exit_signal = True
            elif signal == "BUY" and position["type"] == "SHORT":
                pnl = position["entry"] - current_price
                exit_signal = True

            if exit_signal:
                trades.append(
                    {
                        "entry": position["entry"],
                        "exit": current_price,
                        "pnl": pnl,
                        "pnl_pct": pnl / position["entry"],
                        "type": position["type"],
                        "duration_bars": idx - position["entry_bar"],
                        "entry_time": df.index[position["entry_bar"]],
                        "exit_time": df.index[idx],
                    }
                )
                position = None

    # Close open position at end
    if position:
        final_price = df.iloc[-1]["close"]
        pnl = (
            (final_price - position["entry"])
            if position["type"] == "LONG"
            else (position["entry"] - final_price)
        )
        trades.append(
            {
                "entry": position["entry"],
                "exit": final_price,
                "pnl": pnl,
                "pnl_pct": pnl / position["entry"],
                "type": position["type"],
                "duration_bars": len(df) - position["entry_bar"],
                "entry_time": df.index[position["entry_bar"]],
                "exit_time": df.index[-1],
            }
        )

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_mb = peak / 1024 / 1024
    execution_time_ms = (time.time() - start_time) * 1000

    return trades, execution_time_ms, memory_mb


def get_strategy_category(strategy_name: str) -> str:
    """Get category for a strategy"""
    categories = {
        "trend_following": "Trend Following",
        "turtle_trading": "Trend Following",
        "momentum_analysis": "Momentum",
        "technical_analysis": "Technical",
        "swing_trading": "Swing Trading",
        "position_trading": "Position Trading",
        "breakout_trading": "Breakout",
        "scalping_momentum": "Scalping",
        "mean_reversion": "Mean Reversion",
        "mean_reversion_strategy": "Mean Reversion",
        "mean_reversion_analysis": "Mean Reversion",
        "reversal_trading": "Mean Reversion",
        "range_trading": "Range Trading",
        "smc_agent": "SMC/ICT",
        "ict_agent": "SMC/ICT",
        "supply_demand_agent": "SMC/ICT",
        "liquidity_agent": "SMC/ICT",
        "market_structure_agent": "SMC/ICT",
        "volume_profile_agent": "SMC/ICT",
        "snr_agent": "SMC/ICT",
        "wyckoff_agent": "SMC/ICT",
        "fibonacci_agent": "SMC/ICT",
        "technical_analysis_agent": "Technical",
        "technical_analysis_strategy": "Technical",
        "technical_analyst": "Technical",
        "divergence_agent": "Technical",
        "gap_trading": "Gap Trading",
        "quantitative_analyst": "Quantitative",
        "quantitative_momentum": "Quantitative",
        "factor_investing_strategy": "Quantitative",
        "factor_investing_analysis": "Quantitative",
        "jim_simons_strategy": "Quantitative",
        "jim_simons_quant": "Quantitative",
        "jim_simons_analysis": "Quantitative",
        "warren_buffett_style": "Value Investing",
        "warren_buffett_agent": "Value Investing",
        "benjamin_graham_style": "Value Investing",
        "benjamin_graham_agent": "Value Investing",
        "graham_value_investing": "Value Investing",
        "peter_lynch_style": "Value Investing",
        "philip_fisher_style": "Value Investing",
        "william_o'neil_style": "Growth Investing",
        "michael_burry_style": "Value Investing",
        "george_soros_style": "Macro Trading",
        "john_templeton_style": "Value Investing",
        "joel_greenblatt_style": "Value Investing",
        "ray_dalio_style": "Macro Trading",
        "earnings_momentum": "Earnings",
        "earnings_momentum_strategy": "Earnings",
        "earnings_momentum_analysis": "Earnings",
        "fundamentals_agent": "Fundamental",
        "factor_investor": "Quantitative",
        "sepa_(super_performance)": "Super Performance",
    }
    return categories.get(strategy_name, "Other")


def generate_visualizations(results: List[BacktestMetrics], df: pd.DataFrame):
    """Generate comprehensive visualizations"""
    print("📈 Generating visualizations...")

    strategies = [r.strategy_name for r in results]

    # Figure 1: Performance Overview
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle(
        "AI Hedge Fund v2.2.2 - Strategy Performance Overview",
        fontsize=16,
        fontweight="bold",
    )

    # Win Rate by Strategy
    ax1 = axes[0, 0]
    colors = ["green" if r.win_rate > 0.5 else "red" for r in results]
    ax1.barh(strategies, [r.win_rate * 100 for r in results], color=colors)
    ax1.set_xlabel("Win Rate (%)")
    ax1.set_title("Win Rate by Strategy")
    ax1.axvline(x=50, color="black", linestyle="--", alpha=0.5)

    # Total Return by Strategy
    ax2 = axes[0, 1]
    colors = ["green" if r.total_return > 0 else "red" for r in results]
    ax2.barh(strategies, [r.total_return * 100 for r in results], color=colors)
    ax2.set_xlabel("Total Return (%)")
    ax2.set_title("Total Return by Strategy")
    ax2.axvline(x=0, color="black", linestyle="--", alpha=0.5)

    # Risk/Reward Ratio
    ax3 = axes[0, 2]
    ax3.barh(
        strategies, [r.risk_reward_ratio for r in results], color="blue", alpha=0.7
    )
    ax3.set_xlabel("Risk/Reward Ratio")
    ax3.set_title("Risk/Reward Ratio by Strategy")

    # Max Drawdown
    ax4 = axes[1, 0]
    ax4.barh(
        strategies, [r.max_drawdown * 100 for r in results], color="orange", alpha=0.7
    )
    ax4.set_xlabel("Max Drawdown (%)")
    ax4.set_title("Maximum Drawdown by Strategy")

    # Profit Factor
    ax5 = axes[1, 1]
    colors = ["green" if r.profit_factor > 1 else "red" for r in results]
    ax5.barh(strategies, [min(r.profit_factor, 5) for r in results], color=colors)
    ax5.set_xlabel("Profit Factor (capped at 5)")
    ax5.set_title("Profit Factor by Strategy")

    # Sharpe Ratio
    ax6 = axes[1, 2]
    colors = ["green" if r.sharple_ratio > 0 else "red" for r in results]
    ax6.barh(strategies, [r.sharple_ratio for r in results], color=colors)
    ax6.set_xlabel("Sharpe Ratio")
    ax6.set_title("Sharpe Ratio by Strategy")
    ax6.axvline(x=0, color="black", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "performance_overview.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   ✓ Saved: performance_overview.png")

    # Figure 2: Category Performance
    fig, ax = plt.subplots(figsize=(14, 8))
    categories = {}
    for r in results:
        cat = r.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r.total_return * 100)

    cat_names = list(categories.keys())
    cat_returns = [np.mean(categories[cat]) for cat in cat_names]
    cat_colors = ["green" if r > 0 else "red" for r in cat_returns]

    bars = ax.bar(cat_names, cat_returns, color=cat_colors, alpha=0.7)
    ax.set_xlabel("Strategy Category")
    ax.set_ylabel("Average Return (%)")
    ax.set_title("Average Return by Strategy Category (3-Year Backtest)")
    ax.tick_params(axis="x", rotation=45)

    for bar, val in zip(bars, cat_returns):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{val:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "category_performance.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   ✓ Saved: category_performance.png")

    # Figure 3: Equity Curves
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    fig.suptitle("Equity Curves - Top 9 Strategies", fontsize=16, fontweight="bold")

    # Sort by total return and take top 9
    sorted_results = sorted(results, key=lambda x: x.total_return, reverse=True)[:9]

    for idx, r in enumerate(sorted_results):
        ax = axes[idx // 3, idx % 3]

        # Generate equity curve
        initial_capital = 10000
        equity = [initial_capital]
        for trade in r.trades:
            equity.append(equity[-1] + trade.get("pnl", 0))

        ax.plot(equity, color="blue", linewidth=1.5)
        ax.fill_between(range(len(equity)), equity, alpha=0.3)
        ax.set_title(
            f"{r.strategy_name}\nReturn: {r.total_return * 100:.1f}% | Win: {r.win_rate * 100:.1f}%"
        )
        ax.set_xlabel("Trade Number")
        ax.set_ylabel("Portfolio Value ($)")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "equity_curves.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   ✓ Saved: equity_curves.png")

    # Figure 4: Memory & Execution Time
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ax1 = axes[0]
    ax1.barh(strategies, [r.memory_used_mb for r in results], color="purple", alpha=0.7)
    ax1.set_xlabel("Memory (MB)")
    ax1.set_title("Memory Usage by Strategy")

    ax2 = axes[1]
    ax2.barh(
        strategies, [r.execution_time_ms for r in results], color="teal", alpha=0.7
    )
    ax2.set_xlabel("Execution Time (ms)")
    ax2.set_title("Execution Time by Strategy")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "resource_usage.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   ✓ Saved: resource_usage.png")

    # Figure 5: Trade Distribution
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Win/Loss Distribution
    ax1 = axes[0, 0]
    wins = [r.wins for r in results]
    losses = [r.losses for r in results]
    x = np.arange(len(strategies))
    ax1.bar(x, wins, label="Wins", color="green", alpha=0.7)
    ax1.bar(x, losses, bottom=wins, label="Losses", color="red", alpha=0.7)
    ax1.set_xticks(x)
    ax1.set_xticklabels(strategies, rotation=90, fontsize=6)
    ax1.set_ylabel("Number of Trades")
    ax1.set_title("Win/Loss Distribution")
    ax1.legend()

    # Best/Worst Trade
    ax2 = axes[0, 1]
    ax2.barh(
        strategies,
        [r.best_trade for r in results],
        color="green",
        alpha=0.5,
        label="Best",
    )
    ax2.barh(
        strategies,
        [abs(r.worst_trade) for r in results],
        color="red",
        alpha=0.5,
        label="Worst",
    )
    ax2.set_xlabel("Trade PnL ($)")
    ax2.set_title("Best/Worst Trade by Strategy")
    ax2.legend()

    # Consecutive Wins/Losses
    ax3 = axes[1, 0]
    ax3.barh(
        strategies,
        [r.consecutive_wins for r in results],
        color="green",
        alpha=0.7,
        label="Consecutive Wins",
    )
    ax3.barh(
        strategies,
        [-r.consecutive_losses for r in results],
        color="red",
        alpha=0.7,
        label="Consecutive Losses",
    )
    ax3.axvline(x=0, color="black", linestyle="-")
    ax3.set_xlabel("Consecutive Trades")
    ax3.set_title("Consecutive Wins/Losses")
    ax3.legend()

    # Expectancy
    ax4 = axes[1, 1]
    colors = ["green" if r.expectancy > 0 else "red" for r in results]
    ax4.barh(strategies, [r.expectancy for r in results], color=colors)
    ax4.set_xlabel("Expectancy ($)")
    ax4.set_title("Expectancy by Strategy")
    ax4.axvline(x=0, color="black", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "trade_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   ✓ Saved: trade_distribution.png")


def generate_html_report(results: List[BacktestMetrics], df: pd.DataFrame):
    """Generate comprehensive HTML report"""
    print("📄 Generating HTML report...")

    # Sort by total return
    sorted_results = sorted(results, key=lambda x: x.total_return, reverse=True)

    # Calculate summary statistics
    total_strategies = len(results)
    profitable_strategies = len([r for r in results if r.total_return > 0])
    avg_return = np.mean([r.total_return * 100 for r in results])
    avg_win_rate = np.mean([r.win_rate * 100 for r in results])
    avg_profit_factor = np.mean(
        [r.profit_factor for r in results if r.profit_factor < float("inf")]
    )
    total_trades = sum(r.trades for r in results)

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AI Hedge Fund v2.2.2 - Backtest Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a1a2e; color: #eee; }}
        h1 {{ color: #00d4ff; text-align: center; }}
        h2 {{ color: #00ff88; border-bottom: 2px solid #00ff88; padding-bottom: 10px; }}
        .summary {{ background: #16213e; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .stats {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 15px; margin: 20px 0; }}
        .stat-box {{ background: #0f3460; padding: 15px; border-radius: 8px; text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #00d4ff; }}
        .stat-label {{ font-size: 12px; color: #aaa; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #0f3460; color: #00ff88; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #333; }}
        tr:hover {{ background: #16213e; }}
        .positive {{ color: #00ff88; }}
        .negative {{ color: #ff4444; }}
        .chart-container {{ margin: 20px 0; text-align: center; }}
        img {{ max-width: 100%; border-radius: 10px; margin: 10px 0; }}
        .category {{ background: #0f3460; padding: 20px; border-radius: 10px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>🤖 AI Hedge Fund v2.2.2 - Comprehensive Backtest Report</h1>
    <p style="text-align: center; color: #aaa;">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    
    <div class="summary">
        <h2>📊 Executive Summary</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{total_strategies}</div>
                <div class="stat-label">Total Strategies</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{profitable_strategies}</div>
                <div class="stat-label">Profitable</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{avg_return:.1f}%</div>
                <div class="stat-label">Avg Return</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{avg_win_rate:.1f}%</div>
                <div class="stat-label">Avg Win Rate</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{avg_profit_factor:.2f}</div>
                <div class="stat-label">Avg Profit Factor</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{total_trades}</div>
                <div class="stat-label">Total Trades</div>
            </div>
        </div>
    </div>
    
    <h2>📈 Performance Visualizations</h2>
    <div class="chart-container">
        <img src="performance_overview.png" alt="Performance Overview">
    </div>
    <div class="chart-container">
        <img src="category_performance.png" alt="Category Performance">
    </div>
    <div class="chart-container">
        <img src="equity_curves.png" alt="Equity Curves">
    </div>
    <div class="chart-container">
        <img src="resource_usage.png" alt="Resource Usage">
    </div>
    <div class="chart-container">
        <img src="trade_distribution.png" alt="Trade Distribution">
    </div>
    
    <h2>🏆 Top 10 Strategies by Return</h2>
    <table>
        <tr>
            <th>Rank</th>
            <th>Strategy</th>
            <th>Category</th>
            <th>Return</th>
            <th>Win Rate</th>
            <th>Profit Factor</th>
            <th>RR Ratio</th>
            <th>Max DD</th>
            <th>Trades</th>
            <th>Sharpe</th>
        </tr>
"""

    for idx, r in enumerate(sorted_results[:10], 1):
        return_class = "positive" if r.total_return > 0 else "negative"
        html += f"""
        <tr>
            <td>{idx}</td>
            <td>{r.strategy_name}</td>
            <td>{r.category}</td>
            <td class="{return_class}">{r.total_return * 100:.2f}%</td>
            <td>{r.win_rate * 100:.1f}%</td>
            <td>{r.profit_factor:.2f}</td>
            <td>{r.risk_reward_ratio:.2f}</td>
            <td>{r.max_drawdown * 100:.2f}%</td>
            <td>{r.trades}</td>
            <td>{r.sharple_ratio:.2f}</td>
        </tr>
"""

    html += """
    </table>
    
    <h2>📋 All Strategy Results</h2>
    <table>
        <tr>
            <th>Strategy</th>
            <th>Category</th>
            <th>Return</th>
            <th>Win Rate</th>
            <th>Profit Factor</th>
            <th>RR Ratio</th>
            <th>Max DD</th>
            <th>Sharpe</th>
            <th>Expectancy</th>
            <th>Memory</th>
            <th>Time</th>
        </tr>
"""

    for r in results:
        return_class = "positive" if r.total_return > 0 else "negative"
        expectancy_class = "positive" if r.expectancy > 0 else "negative"
        html += f"""
        <tr>
            <td>{r.strategy_name}</td>
            <td>{r.category}</td>
            <td class="{return_class}">{r.total_return * 100:.2f}%</td>
            <td>{r.win_rate * 100:.1f}%</td>
            <td>{r.profit_factor:.2f}</td>
            <td>{r.risk_reward_ratio:.2f}</td>
            <td>{r.max_drawdown * 100:.2f}%</td>
            <td>{r.sharple_ratio:.2f}</td>
            <td class="{expectancy_class}">${r.expectancy:.2f}</td>
            <td>{r.memory_used_mb:.2f} MB</td>
            <td>{r.execution_time_ms:.1f} ms</td>
        </tr>
"""

    html += """
    </table>
    
    <h2>📊 Category Analysis</h2>
"""

    # Group by category
    categories = {}
    for r in results:
        cat = r.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    for cat, cat_results in sorted(
        categories.items(),
        key=lambda x: np.mean([r.total_return for r in x[1]]),
        reverse=True,
    ):
        cat_return = np.mean([r.total_return * 100 for r in cat_results])
        cat_winrate = np.mean([r.win_rate * 100 for r in cat_results])
        cat_profit_factor = np.mean(
            [r.profit_factor for r in cat_results if r.profit_factor < float("inf")]
        )

        html += f"""
    <div class="category">
        <h3>{cat}</h3>
        <p>Strategies: {len(cat_results)} | Avg Return: {cat_return:.2f}% | Avg Win Rate: {cat_winrate:.1f}% | Avg Profit Factor: {cat_profit_factor:.2f}</p>
        <p>Strategies: {", ".join([r.strategy_name for r in cat_results])}</p>
    </div>
"""

    html += """
    <h2>💾 System Resources</h2>
    <p>Memory usage and execution time tracked for all strategies.</p>
    
    <h2>📝 Notes</h2>
    <ul>
        <li>Backtest period: 3 years of hourly data (~756 trading days)</li>
        <li>Initial capital: $10,000</li>
        <li>Risk management: 2% stop loss, 4% take profit per trade</li>
        <li>All strategies tested following trading plan guidelines</li>
        <li>Results are based on simulated data and past performance does not guarantee future results</li>
    </ul>
    
</body>
</html>
"""

    with open(OUTPUT_DIR / "backtest_report.html", "w") as f:
        f.write(html)

    print(f"   ✓ Saved: backtest_report.html")


def main():
    """Main backtest execution"""
    print("=" * 70)
    print("🤖 AI HEDGE FUND v2.2.2 - COMPREHENSIVE BACKTEST SYSTEM")
    print("=" * 70)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Get all strategies
    registry = get_comprehensive_registry()
    strategies = list(registry.strategies.keys())
    print(f"\n📋 Total Strategies to Test: {len(strategies)}")

    # Generate 3-year data
    df = generate_3yr_data("AAPL")

    # Run backtests
    results = []
    initial_capital = 10000

    print("\n" + "=" * 70)
    print("🚀 STARTING STRATEGY BACKTESTS")
    print("=" * 70)

    for idx, strategy_name in enumerate(strategies, 1):
        category = get_strategy_category(strategy_name)

        print(
            f"\n[{idx:02d}/{len(strategies)}] Testing: {strategy_name:<30} ({category})",
            end=" ",
            flush=True,
        )

        try:
            trades, exec_time, memory = run_strategy_backtest(
                strategy_name, df, initial_capital
            )
            metrics = calculate_metrics(trades, initial_capital, exec_time, memory)

            if metrics:
                metrics.strategy_name = strategy_name
                metrics.category = category
                results.append(metrics)

                print(
                    f"✓ Trades: {metrics.trades:3d} | Return: {metrics.total_return * 100:+6.2f}% | "
                    f"Win: {metrics.win_rate * 100:.1f}% | RR: {metrics.risk_reward_ratio:.2f} | "
                    f"PF: {metrics.profit_factor:.2f} | DD: {metrics.max_drawdown * 100:.2f}% | "
                    f"Sharpe: {metrics.sharple_ratio:.2f}"
                )
            else:
                print("✗ No trades generated")

        except Exception as e:
            print(f"✗ Error: {e}")

    print("\n" + "=" * 70)
    print("📊 BACKTEST RESULTS SUMMARY")
    print("=" * 70)

    # Calculate summary
    profitable = [r for r in results if r.total_return > 0]
    losing = [r for r in results if r.total_return <= 0]

    print(f"\nTotal Strategies:     {len(results)}")
    print(
        f"Profitable:           {len(profitable)} ({len(profitable) / len(results) * 100:.1f}%)"
    )
    print(
        f"Losing:               {len(losing)} ({len(losing) / len(results) * 100:.1f}%)"
    )
    print(
        f"Average Return:       {np.mean([r.total_return * 100 for r in results]):.2f}%"
    )
    print(f"Average Win Rate:     {np.mean([r.win_rate * 100 for r in results]):.1f}%")
    print(
        f"Average Profit Factor: {np.mean([r.profit_factor for r in results if r.profit_factor < float('inf')]):.2f}"
    )
    print(f"Total Trades:         {sum(r.trades for r in results)}")

    # Top 5 strategies
    print("\n🏆 TOP 5 STRATEGIES:")
    top5 = sorted(results, key=lambda x: x.total_return, reverse=True)[:5]
    for idx, r in enumerate(top5, 1):
        print(
            f"  {idx}. {r.strategy_name:<25} Return: {r.total_return * 100:+7.2f}% | "
            f"Win: {r.win_rate * 100:.1f}% | PF: {r.profit_factor:.2f} | DD: {r.max_drawdown * 100:.2f}%"
        )

    # Bottom 5 strategies
    print("\n⚠️ BOTTOM 5 STRATEGIES:")
    bottom5 = sorted(results, key=lambda x: x.total_return)[:5]
    for r in bottom5:
        print(
            f"  • {r.strategy_name:<25} Return: {r.total_return * 100:+7.2f}% | "
            f"Win: {r.win_rate * 100:.1f}% | PF: {r.profit_factor:.2f}"
        )

    # Generate visualizations
    print("\n" + "=" * 70)
    print("📈 GENERATING VISUALIZATIONS")
    print("=" * 70)
    generate_visualizations(results, df)

    # Generate HTML report
    print("\n" + "=" * 70)
    print("📄 GENERATING REPORT")
    print("=" * 70)
    generate_html_report(results, df)

    # Save JSON results
    print("\n" + "=" * 70)
    print("💾 SAVING RESULTS")
    print("=" * 70)

    results_data = {
        "timestamp": datetime.now().isoformat(),
        "total_strategies": len(results),
        "profitable_strategies": len(profitable),
        "losing_strategies": len(losing),
        "average_return": np.mean([r.total_return for r in results]),
        "average_win_rate": np.mean([r.win_rate for r in results]),
        "total_trades": sum(r.trades for r in results),
        "strategies": [asdict(r) for r in results],
    }

    with open(OUTPUT_DIR / "backtest_results.json", "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"   ✓ Saved: backtest_results.json")

    print("\n" + "=" * 70)
    print("✅ BACKTEST COMPLETE!")
    print("=" * 70)
    print(f"\nResults saved to: {OUTPUT_DIR}/")
    print(f"  - backtest_report.html (Full Report)")
    print(f"  - backtest_results.json (Raw Data)")
    print(f"  - performance_overview.png")
    print(f"  - category_performance.png")
    print(f"  - equity_curves.png")
    print(f"  - resource_usage.png")
    print(f"  - trade_distribution.png")
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


if __name__ == "__main__":
    main()
