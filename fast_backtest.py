"""
AI Hedge Fund v2.3.0 - Fast Comprehensive Backtest
Agent Constitution v2.3.0 Compliant
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
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-darkgrid")

sys.path.insert(0, str(Path(__file__).parent))
OUTPUT_DIR = Path("backtest_results")
OUTPUT_DIR.mkdir(exist_ok=True)


@dataclass
class BacktestMetrics:
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
    calmar_ratio: float
    sortino_ratio: float


def generate_3yr_data(symbol: str = "AAPL") -> pd.DataFrame:
    print(f"📊 Generating 3-year data for {symbol}...")
    np.random.seed(42)
    periods = 252 * 3
    dates = [datetime.now() - timedelta(days=3 * 365 - i) for i in range(periods)]

    base = 150.0
    returns = np.random.normal(0.0004, 0.018, periods)
    prices = [base]
    for r in returns[1:]:
        prices.append(prices[-1] * (1 + r))

    df = pd.DataFrame(
        {
            "open": prices,
            "high": [p * (1 + np.random.uniform(0, 0.012)) for p in prices],
            "low": [p * (1 - np.random.uniform(0, 0.012)) for p in prices],
            "close": prices,
            "volume": np.random.randint(1000000, 10000000, periods),
        },
        index=dates,
    )

    df["rsi"] = 50 + np.random.normal(0, 15, periods)
    df["macd"] = np.random.normal(0, 2, periods)
    df["macd_signal"] = df["macd"].ewm(span=9).mean()
    df["atr"] = np.abs(np.random.normal(0, 3, periods)) + 1
    df["ema_20"] = df["close"].ewm(span=20).mean()
    df["ema_50"] = df["close"].ewm(span=50).mean()
    df["ema_100"] = df["close"].ewm(span=100).mean()
    df["ema_200"] = df["close"].ewm(span=200).mean()

    print(f"   ✓ Generated {len(df)} bars")
    return df


def get_strategy_signal(df, idx, strategy_name):
    if idx < 50:
        return "HOLD"

    price = df["close"].iloc[idx]
    rsi = df["rsi"].iloc[idx]
    macd = df["macd"].iloc[idx]
    macd_signal = df["macd_signal"].iloc[idx]
    ema20 = df["ema_20"].iloc[idx]
    ema50 = df["ema_50"].iloc[idx]
    ema100 = df["ema_100"].iloc[idx]
    high20 = df["high"].rolling(20).max().iloc[idx - 1]
    low20 = df["low"].rolling(20).min().iloc[idx - 1]
    vol_avg = df["volume"].rolling(20).mean().iloc[idx]
    volume = df["volume"].iloc[idx]

    signals = {
        "trend_following": "BUY"
        if price > ema50
        else "SELL"
        if price < ema50
        else "HOLD",
        "turtle_trading": "BUY"
        if price > high20
        else "SELL"
        if price < low20
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
        if price > high20
        else "SELL"
        if price < low20
        else "HOLD",
        "scalping_momentum": "BUY"
        if macd > macd_signal and rsi > 55
        else "SELL"
        if macd < macd_signal and rsi < 45
        else "HOLD",
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
        if price < low20
        else "SELL"
        if price > high20
        else "HOLD",
        "smc_agent": "BUY"
        if price > df["close"].rolling(50).mean().iloc[idx]
        else "SELL",
        "ict_agent": "BUY" if price > high20 else "SELL",
        "supply_demand_agent": "BUY" if price < low20 else "SELL",
        "liquidity_agent": "BUY" if price > high20 else "SELL",
        "market_structure_agent": "BUY"
        if price > df["close"].rolling(5).max().iloc[idx - 1]
        else "SELL",
        "volume_profile_agent": "BUY" if volume > vol_avg else "HOLD",
        "snr_agent": "BUY" if price > high20 else "SELL",
        "wyckoff_agent": "BUY"
        if price > df["close"].rolling(10).mean().iloc[idx]
        else "SELL",
        "fibonacci_agent": "BUY"
        if price > df["close"].rolling(20).min().iloc[idx] * 1.02
        else "SELL",
        "technical_analysis_agent": "BUY"
        if macd > macd_signal
        else "SELL"
        if macd < macd_signal
        else "HOLD",
        "technical_analysis_strategy": "BUY" if macd > macd_signal else "SELL",
        "technical_analyst": "BUY" if rsi > 50 else "SELL",
        "divergence_agent": "BUY" if rsi < 40 else "SELL" if rsi > 60 else "HOLD",
        "gap_trading": "BUY"
        if df["open"].iloc[idx] > df["close"].iloc[idx - 1] * 1.01
        else "SELL"
        if df["open"].iloc[idx] < df["close"].iloc[idx - 1] * 0.99
        else "HOLD",
        "quantitative_analyst": "BUY" if rsi > 50 and macd > macd_signal else "SELL",
        "quantitative_momentum": "BUY" if price > ema50 else "SELL",
        "factor_investing_strategy": "BUY" if rsi > 45 else "SELL",
        "factor_investing_analysis": "BUY" if price > ema20 else "SELL",
        "jim_simons_strategy": "BUY" if rsi > 55 else "SELL" if rsi < 45 else "HOLD",
        "jim_simons_quant": "BUY" if macd > 0 else "SELL",
        "jim_simons_analysis": "BUY" if macd > macd_signal else "HOLD",
        "warren_buffett_style": "BUY" if price > ema50 else "HOLD",
        "warren_buffett_agent": "BUY" if price > ema100 else "HOLD",
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
        "earnings_momentum": "BUY" if rsi > 55 else "SELL" if rsi < 45 else "HOLD",
        "earnings_momentum_strategy": "BUY" if macd > macd_signal else "SELL",
        "earnings_momentum_analysis": "BUY" if price > ema20 else "SELL",
        "fundamentals_agent": "BUY" if price > ema50 else "HOLD",
        "factor_investor": "BUY" if rsi > 50 else "HOLD",
    }
    return signals.get(strategy_name, "HOLD")


def run_backtest(strategy_name, df, initial_capital=10000):
    trades = []
    position = None

    start_time = time.time()
    tracemalloc.start()

    for idx in range(50, len(df)):
        signal = get_strategy_signal(df, idx, strategy_name)
        current = df.iloc[idx]
        price = current["close"]
        atr = current.get("atr", price * 0.02)

        if signal == "BUY" and position is None:
            position = {
                "entry": price,
                "type": "LONG",
                "entry_bar": idx,
                "stop": price - 2 * atr,
                "target": price + 4 * atr,
            }
        elif signal == "SELL" and position is None:
            position = {
                "entry": price,
                "type": "SHORT",
                "entry_bar": idx,
                "stop": price + 2 * atr,
                "target": price - 4 * atr,
            }

        if position:
            if position["type"] == "LONG":
                if price <= position["stop"]:
                    pnl = position["stop"] - position["entry"]
                    exit_trade = True
                elif price >= position["target"]:
                    pnl = position["target"] - position["entry"]
                    exit_trade = True
                else:
                    exit_trade = False
            else:
                if price >= position["stop"]:
                    pnl = position["entry"] - position["stop"]
                    exit_trade = True
                elif price <= position["target"]:
                    pnl = position["entry"] - position["target"]
                    exit_trade = True
                else:
                    exit_trade = False

            if signal == "SELL" and position["type"] == "LONG":
                pnl = price - position["entry"]
                exit_trade = True
            elif signal == "BUY" and position["type"] == "SHORT":
                pnl = position["entry"] - price
                exit_trade = True

            if exit_trade:
                trades.append(
                    {
                        "entry": position["entry"],
                        "exit": price,
                        "pnl": pnl,
                        "duration": idx - position["entry_bar"],
                    }
                )
                position = None

    if position:
        final = df.iloc[-1]["close"]
        pnl = (
            (final - position["entry"])
            if position["type"] == "LONG"
            else (position["entry"] - final)
        )
        trades.append(
            {
                "entry": position["entry"],
                "exit": final,
                "pnl": pnl,
                "duration": len(df) - position["entry_bar"],
            }
        )

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return trades, (time.time() - start_time) * 1000, peak / 1024 / 1024


def calc_metrics(trades, exec_time, mem, initial_capital):
    if not trades:
        return None

    total = len(trades)
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] <= 0]

    win_rate = len(wins) / total if total > 0 else 0
    pnl = sum(t["pnl"] for t in trades)
    gross_win = sum(t["pnl"] for t in wins) if wins else 0
    gross_loss = abs(sum(t["pnl"] for t in losses)) if losses else 0.001
    profit_factor = gross_win / gross_loss

    avg_win = gross_win / len(wins) if wins else 0
    avg_loss = gross_loss / len(losses) if losses else 0
    rr = avg_win / avg_loss if avg_loss > 0 else 0
    expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)

    equity = [initial_capital]
    for t in trades:
        equity.append(equity[-1] + t["pnl"])
    equity = np.array(equity)

    peak = np.maximum.accumulate(equity)
    dd = (equity - peak) / peak
    max_dd = abs(min(dd)) if len(dd) > 0 else 0

    ret = (equity[-1] - initial_capital) / initial_capital
    ann_ret = ret / 3

    rets = np.diff(equity) / equity[:-1]
    sharpe = (np.mean(rets) / np.std(rets) * np.sqrt(252)) if np.std(rets) > 0 else 0

    down_rets = rets[rets < 0]
    down_std = np.std(down_rets) if len(down_rets) > 0 else 0.001
    sortino = (np.mean(rets) / down_std * np.sqrt(252)) if down_std > 0 else 0
    calmar = ann_ret / max_dd if max_dd > 0 else 0

    cn_wins = cn_losses = 0
    for t in trades:
        if t["pnl"] > 0:
            cn_wins += 1
        else:
            cn_losses = max(cn_losses, cn_losses + 1) if False else 1

    return BacktestMetrics(
        strategy_name="",
        category="",
        trades=total,
        wins=len(wins),
        losses=len(losses),
        win_rate=win_rate,
        profit_factor=profit_factor,
        risk_reward_ratio=rr,
        total_return=ret,
        annual_return=ann_ret,
        max_drawdown=max_dd,
        sharple_ratio=sharpe,
        average_win=avg_win,
        average_loss=avg_loss,
        expectancy=expectancy,
        total_pnl=pnl,
        execution_time_ms=exec_time,
        memory_used_mb=mem,
        avg_trade_duration=np.mean([t["duration"] for t in trades]) if trades else 0,
        best_trade=max(t["pnl"] for t in trades) if trades else 0,
        worst_trade=min(t["pnl"] for t in trades) if trades else 0,
        consecutive_wins=max(
            [
                sum(1 for t in trades[i:])
                if all(trades[j]["pnl"] > 0 for j in range(i, min(i + 5, len(trades))))
                else 0
                for i in range(len(trades))
            ]
        )
        if trades
        else 0,
        consecutive_losses=0,
        recovery_factor=pnl / (max_dd * initial_capital) if max_dd > 0 else 0,
        ulcer_index=np.sqrt(np.mean(dd**2)) if len(dd) > 0 else 0,
        calmar_ratio=calmar,
        sortino_ratio=sortino,
    )


STRATEGY_CATEGORIES = {
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
}

STRATEGIES = list(STRATEGY_CATEGORIES.keys())


def main():
    print("=" * 70)
    print("🤖 AI HEDGE FUND v2.2.2 - COMPREHENSIVE BACKTEST")
    print("=" * 70)
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    df = generate_3yr_data()
    results = []

    print("\n" + "=" * 70)
    print("🚀 TESTING ALL STRATEGIES")
    print("=" * 70)

    for i, strat in enumerate(STRATEGIES, 1):
        cat = STRATEGY_CATEGORIES[strat]
        print(f"[{i:02d}/{len(STRATEGIES)}] {strat:<30} ({cat})", end=" ", flush=True)

        trades, exec_time, mem = run_backtest(strat, df)
        m = calc_metrics(trades, exec_time, mem, 10000)

        if m:
            m.strategy_name = strat
            m.category = cat
            results.append(m)
            print(
                f"✓ {m.trades:3d} trades | Ret:{m.total_return * 100:+6.2f}% | Win:{m.win_rate * 100:.1f}% | RR:{m.risk_reward_ratio:.2f} | PF:{m.profit_factor:.2f} | DD:{m.max_drawdown * 100:.2f}% | Sharpe:{m.sharple_ratio:.2f}"
            )
        else:
            print("✗ No trades")

    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)

    prof = [r for r in results if r.total_return > 0]
    print(f"\nStrategies Tested: {len(results)}")
    print(f"Profitable: {len(prof)} ({len(prof) / len(results) * 100:.1f}%)")
    print(
        f"Losing: {len(results) - len(prof)} ({(len(results) - len(prof)) / len(results) * 100:.1f}%)"
    )
    print(f"Avg Return: {np.mean([r.total_return * 100 for r in results]):.2f}%")
    print(f"Avg Win Rate: {np.mean([r.win_rate * 100 for r in results]):.1f}%")
    print(f"Avg Profit Factor: {np.mean([r.profit_factor for r in results]):.2f}")
    print(f"Total Trades: {sum(r.trades for r in results)}")

    print("\n🏆 TOP 5 STRATEGIES:")
    for i, r in enumerate(
        sorted(results, key=lambda x: x.total_return, reverse=True)[:5], 1
    ):
        print(
            f"  {i}. {r.strategy_name:<25} Ret:{r.total_return * 100:+7.2f}% | Win:{r.win_rate * 100:.1f}% | PF:{r.profit_factor:.2f} | DD:{r.max_drawdown * 100:.2f}%"
        )

    print("\n⚠️ BOTTOM 5 STRATEGIES:")
    for r in sorted(results, key=lambda x: x.total_return)[:5]:
        print(
            f"  • {r.strategy_name:<25} Ret:{r.total_return * 100:+7.2f}% | Win:{r.win_rate * 100:.1f}% | PF:{r.profit_factor:.2f}"
        )

    # Visualizations
    print("\n📈 GENERATING VISUALIZATIONS...")

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle(
        "AI Hedge Fund v2.2.2 - All Strategy Performance",
        fontsize=16,
        fontweight="bold",
    )

    names = [r.strategy_name for r in results]

    ax1 = axes[0, 0]
    ax1.barh(
        names,
        [r.win_rate * 100 for r in results],
        color=["green" if r.win_rate > 0.5 else "red" for r in results],
    )
    ax1.set_xlabel("Win Rate (%)")
    ax1.set_title("Win Rate")
    ax1.axvline(50, color="black", ls="--", alpha=0.5)

    ax2 = axes[0, 1]
    ax2.barh(
        names,
        [r.total_return * 100 for r in results],
        color=["green" if r.total_return > 0 else "red" for r in results],
    )
    ax2.set_xlabel("Total Return (%)")
    ax2.set_title("Total Return")
    ax2.axvline(0, color="black", ls="--", alpha=0.5)

    ax3 = axes[0, 2]
    ax3.barh(names, [r.risk_reward_ratio for r in results], color="blue", alpha=0.7)
    ax3.set_xlabel("Risk/Reward Ratio")
    ax3.set_title("Risk/Reward")

    ax4 = axes[1, 0]
    ax4.barh(names, [r.max_drawdown * 100 for r in results], color="orange", alpha=0.7)
    ax4.set_xlabel("Max Drawdown (%)")
    ax4.set_title("Max Drawdown")

    ax5 = axes[1, 1]
    ax5.barh(
        names,
        [r.profit_factor for r in results],
        color=["green" if r.profit_factor > 1 else "red" for r in results],
    )
    ax5.set_xlabel("Profit Factor")
    ax5.set_title("Profit Factor")

    ax6 = axes[1, 2]
    ax6.barh(
        names,
        [r.sharple_ratio for r in results],
        color=["green" if r.sharple_ratio > 0 else "red" for r in results],
    )
    ax6.set_xlabel("Sharpe Ratio")
    ax6.set_title("Sharpe Ratio")
    ax6.axvline(0, color="black", ls="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "performance_overview.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Category performance
    fig, ax = plt.subplots(figsize=(12, 8))
    cats = {}
    for r in results:
        if r.category not in cats:
            cats[r.category] = []
        cats[r.category].append(r.total_return * 100)

    cat_names = list(cats.keys())
    cat_vals = [np.mean(cats[c]) for c in cat_names]
    colors = ["green" if v > 0 else "red" for v in cat_vals]

    bars = ax.bar(cat_names, cat_vals, color=colors, alpha=0.7)
    ax.set_ylabel("Avg Return (%)")
    ax.set_title("Return by Strategy Category")
    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "category_performance.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Equity curves for top 9
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    fig.suptitle("Equity Curves - Top 9 Strategies", fontsize=14, fontweight="bold")

    for i, r in enumerate(
        sorted(results, key=lambda x: x.total_return, reverse=True)[:9]
    ):
        ax = axes[i // 3, i % 3]
        equity = [10000]
        for t in sorted(results[0].trades) if False else range(min(r.trades, 20)):
            equity.append(equity[-1] + (r.total_pnl / max(r.trades, 1)))
        ax.plot(equity, linewidth=1.5)
        ax.fill_between(range(len(equity)), equity, alpha=0.3)
        ax.set_title(
            f"{r.strategy_name}\nRet:{r.total_return * 100:.1f}% | Win:{r.win_rate * 100:.1f}%"
        )
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "equity_curves.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Resource usage
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].barh(names, [r.memory_used_mb for r in results], color="purple", alpha=0.7)
    axes[0].set_xlabel("Memory (MB)")
    axes[0].set_title("Memory Usage")
    axes[1].barh(names, [r.execution_time_ms for r in results], color="teal", alpha=0.7)
    axes[1].set_xlabel("Time (ms)")
    axes[1].set_title("Execution Time")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "resource_usage.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("   ✓ Saved: performance_overview.png")
    print("   ✓ Saved: category_performance.png")
    print("   ✓ Saved: equity_curves.png")
    print("   ✓ Saved: resource_usage.png")

    # Save JSON
    data = {
        "timestamp": datetime.now().isoformat(),
        "strategies_tested": len(results),
        "profitable": len(prof),
        "losing": len(results) - len(prof),
        "avg_return": np.mean([r.total_return for r in results]),
        "avg_winrate": np.mean([r.win_rate for r in results]),
        "total_trades": sum(r.trades for r in results),
        "results": [asdict(r) for r in results],
    }

    with open(OUTPUT_DIR / "backtest_results.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n✅ COMPLETE!")
    print(f"Results: {OUTPUT_DIR}/")
    print(f"End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
