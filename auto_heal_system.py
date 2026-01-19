#!/usr/bin/env python3
"""
AI HEDGE FUND v2.3.0 - AUTO-HEAL SYSTEM
=======================================

Unified entry point for all auto-systems:
- Auto-Heal (health monitoring, auto-restart)
- Agent Constitution v2.3.0 Compliant
- Auto-Backup (daily backups)
- Strategy Evaluator (auto-ranking)
- Monitoring Dashboard (real-time metrics)

Usage:
    python3 auto_heal_system.py                    # Show status
    python3 auto_heal_system.py --daemon           # Run all systems daemon
    python3 auto_heal_system.py --health           # Health check
    python3 auto_heal_system.py --backup           # Create backup
    python3 auto_heal_system.py --evaluate         # Evaluate strategies
    python3 auto_heal_system.py --monitor          # Run dashboard
    python3 auto_heal_system.py --start            # Start all systems
    python3 auto_heal_system.py --stop             # Stop all systems
    python3 auto_heal_system.py --all              # Run all checks
"""

import sys
import os
import time
import json
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.auto_heal.health_monitor import HealthChecker, HealthConfig
from src.auto_heal.backup_manager import BackupManager, BackupConfig
from src.auto_heal.strategy_evaluator import StrategyEvaluator
from src.auto_heal.monitoring_dashboard import MonitoringDashboard
from src.auto_heal.orchestrator import SystemOrchestrator, OrchestratorConfig

VERSION = "1.0.0"
BUILD_DATE = "2026-01-16"


def print_banner():
    """Print system banner"""
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🤖 AI HEDGE FUND v2.2 - AUTO-HEAL SYSTEM                                 ║
║                                                                              ║
║   • Auto-Heal Monitoring      • Auto-Backup                                ║
║   • Strategy Evaluation       • Real-time Dashboard                        ║
║                                                                              ║
║   Version: {VERSION:<62}║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


def cmd_status():
    """Show system status"""
    orchestrator = SystemOrchestrator()
    orchestrator.print_unified_status()


def cmd_health():
    """Run health check"""
    print("\n🔍 Running health check...\n")

    health_config = HealthConfig(check_interval=30)
    health = HealthChecker(health_config)
    metrics = health.run_full_check()
    health.print_status()

    return metrics.status == "healthy"


def cmd_backup(backup_type: str):
    """Create backup"""
    print(f"\n💾 Creating {backup_type} backup...\n")

    backup_config = BackupConfig(retention_days=7)
    backup = BackupManager(backup_config)
    result = backup.create_backup(backup_type)

    if result:
        print(f"✅ Backup created: {result.filename}")
        print(f"   Size: {result.size_bytes / 1024 / 1024:.2f} MB")
        print(f"   Files: {result.files_count}")
        return True
    else:
        print("❌ Backup failed")
        return False


def cmd_evaluate():
    """Evaluate strategies"""
    print("\n📊 Evaluating strategies...\n")

    evaluator = StrategyEvaluator()
    evaluator.evaluate_all_strategies()
    evaluator.print_summary()

    return len(evaluator.strategies) > 0


def cmd_monitor(refresh: int = 2):
    """Run monitoring dashboard"""
    print(f"\n📈 Starting monitoring dashboard (refresh: {refresh}s)...\n")
    print("Press Ctrl+C to exit\n")

    monitor = MonitoringDashboard(MonitorConfig(refresh_interval=refresh))
    try:
        monitor.run_cli_dashboard()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")


def cmd_start():
    """Start all systems"""
    print("\n🚀 Starting all auto-systems...\n")

    config = OrchestratorConfig(
        run_health_monitor=True,
        run_backup_scheduler=True,
        run_strategy_evaluator=True,
        run_monitoring_dashboard=False,
        evaluate_on_start=True,
    )

    orchestrator = SystemOrchestrator(config)
    orchestrator.start_all(background=True)

    print("✅ All systems started in background")
    print("   Use --status to check")
    print("   Use --stop to stop\n")


def cmd_stop():
    """Stop all systems"""
    print("\n🛑 Stopping all systems...\n")

    orchestrator = SystemOrchestrator()
    orchestrator.stop_all()

    print("✅ All systems stopped\n")


def cmd_all():
    """Run all checks"""
    print("\n🔄 Running all checks...\n")

    results = {}

    # Health check
    print("1. Health Check")
    print("-" * 40)
    results["health"] = cmd_health()

    # Backup
    print("\n2. Backup")
    print("-" * 40)
    results["backup"] = cmd_backup("manual")

    # Strategy evaluation
    print("\n3. Strategy Evaluation")
    print("-" * 40)
    results["strategies"] = cmd_evaluate()

    # Summary
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    for check, passed in results.items():
        icon = "✅" if passed else "❌"
        print(f"  {icon} {check.upper()}: {'PASSED' if passed else 'FAILED'}")

    all_passed = all(results.values())
    print("\n" + ("✅ All checks passed!" if all_passed else "⚠️ Some checks failed"))

    return all_passed


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI Hedge Fund v2.2 - Auto-Heal System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 auto_heal_system.py              # Show status
  python3 auto_heal_system.py --daemon     # Run as daemon
  python3 auto_heal_system.py --health     # Health check
  python3 auto_heal_system.py --backup     # Create backup
  python3 auto_heal_system.py --evaluate   # Evaluate strategies
  python3 auto_heal_system.py --monitor    # Run dashboard
  python3 auto_heal_system.py --all        # Run all checks
        """,
    )

    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--health", action="store_true", help="Run health check")
    parser.add_argument(
        "--backup",
        type=str,
        default="manual",
        help="Create backup (daily, weekly, manual)",
    )
    parser.add_argument("--evaluate", action="store_true", help="Evaluate strategies")
    parser.add_argument(
        "--monitor", action="store_true", help="Run monitoring dashboard"
    )
    parser.add_argument("--refresh", type=int, default=2, help="Dashboard refresh rate")
    parser.add_argument("--start", action="store_true", help="Start all systems")
    parser.add_argument("--stop", action="store_true", help="Stop all systems")
    parser.add_argument("--all", action="store_true", help="Run all checks")

    args = parser.parse_args()

    print_banner()

    if args.status:
        cmd_status()
    elif args.daemon:
        config = OrchestratorConfig(
            run_health_monitor=True,
            run_backup_scheduler=True,
            run_strategy_evaluator=True,
            run_monitoring_dashboard=False,
        )
        orchestrator = SystemOrchestrator(config)
        orchestrator.run_daemon()
    elif args.health:
        cmd_health()
    elif args.backup:
        cmd_backup(args.backup)
    elif args.evaluate:
        cmd_evaluate()
    elif args.monitor:
        cmd_monitor(args.refresh)
    elif args.start:
        cmd_start()
    elif args.stop:
        cmd_stop()
    elif args.all:
        cmd_all()
    else:
        # Default: show status
        cmd_status()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
