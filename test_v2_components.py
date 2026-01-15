"""
Tests for v2.0 new components:
- MT5 Broker integration
- Portfolio models
- Portfolio monitor
- Mode manager
- Execution controller
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestMT5Broker:
    """Tests for MT5 Broker integration."""
    
    def test_broker_initialization(self):
        """Test broker initialization."""
        from src.execution.mt5_broker import MT5Broker
        
        broker = MT5Broker(
            login=123456,
            password="password",
            server="server"
        )
        
        assert broker.login == 123456
        assert broker.password == "password"
        assert broker.server == "server"
        assert broker.connected == False
    
    def test_timeframe_mapping(self):
        """Test timeframe mapping."""
        from src.execution.mt5_broker import MT5Broker
        
        broker = MT5Broker()
        
        assert broker._timeframe_map["M1"] == 1
        assert broker._timeframe_map["H1"] == 16399
        assert broker._timeframe_map["D1"] == 16408
    
    def test_place_order_params(self):
        """Test place order parameter handling."""
        from src.execution.mt5_broker import MT5Broker
        
        broker = MT5Broker()
        
        result = broker.place_order(
            symbol="EURUSD",
            action="BUY",
            volume=1.0,
            stop_loss=1.0850,
            take_profit=1.0950,
            magic=9001
        )
        
        assert result["success"] == False
        assert "MetaTrader5" in result["error"] or "Not connected" in result["error"]


class TestPortfolioModels:
    """Tests for Portfolio data models."""
    
    def test_position_creation(self):
        """Test Position creation."""
        from src.monitoring.portfolio_models import Position, OrderSide
        
        position = Position(
            ticket=12345,
            symbol="EURUSD",
            side=OrderSide.BUY,
            volume=1.0,
            open_price=1.0850,
            open_time=datetime.now(),
            sl=1.0750,
            tp=1.0950
        )
        
        assert position.ticket == 12345
        assert position.symbol == "EURUSD"
        assert position.side == OrderSide.BUY
        assert position.is_long == True
        assert position.is_short == False
    
    def test_position_pnl_calculation(self):
        """Test Position PnL calculation."""
        from src.monitoring.portfolio_models import Position, OrderSide
        
        position = Position(
            ticket=12345,
            symbol="EURUSD",
            side=OrderSide.BUY,
            volume=1.0,
            open_price=1.0850,
            open_time=datetime.now(),
            current_price=1.0875
        )
        
        assert position.pnl > 0
        assert position.is_profitable == True
    
    def test_position_short_pnl(self):
        """Test short position PnL."""
        from src.monitoring.portfolio_models import Position, OrderSide
        
        position = Position(
            ticket=12345,
            symbol="EURUSD",
            side=OrderSide.SELL,
            volume=1.0,
            open_price=1.0850,
            open_time=datetime.now(),
            current_price=1.0875
        )
        
        assert position.pnl < 0
        assert position.is_profitable == False
    
    def test_trade_from_position(self):
        """Test Trade creation from Position."""
        from src.monitoring.portfolio_models import Position, Trade, OrderSide
        
        position = Position(
            ticket=12345,
            symbol="EURUSD",
            side=OrderSide.BUY,
            volume=1.0,
            open_price=1.0850,
            open_time=datetime.now()
        )
        
        trade = Trade.from_position(
            position,
            exit_price=1.0900,
            exit_time=datetime.now()
        )
        
        assert trade.ticket == 12345
        assert trade.symbol == "EURUSD"
        assert trade.is_win == True
    
    def test_portfolio_statistics(self):
        """Test Portfolio statistics calculation."""
        from src.monitoring.portfolio_models import Portfolio, Trade, OrderSide
        
        portfolio = Portfolio(
            account_balance=100000.0,
            account_equity=100000.0
        )
        
        assert portfolio.win_count == 0
        assert portfolio.loss_count == 0
        assert portfolio.profit_factor == 0
    
    def test_portfolio_exposure(self):
        """Test Portfolio exposure calculation."""
        from src.monitoring.portfolio_models import Portfolio, Position, OrderSide
        
        portfolio = Portfolio(account_balance=100000.0)
        
        portfolio.add_position(Position(
            ticket=1,
            symbol="EURUSD",
            side=OrderSide.BUY,
            volume=1.0,
            open_price=1.0,
            open_time=datetime.now(),
            current_price=1.1
        ))
        
        portfolio.add_position(Position(
            ticket=2,
            symbol="GBPUSD",
            side=OrderSide.SELL,
            volume=0.5,
            open_price=1.25,
            open_time=datetime.now(),
            current_price=1.26
        ))
        
        assert portfolio.open_positions_count == 2
        assert portfolio.long_exposure > 0
        assert portfolio.short_exposure > 0


class TestModeManager:
    """Tests for Mode Manager."""
    
    def test_mode_creation(self):
        """Test ModeManager creation."""
        from src.modes.mode_manager import ModeManager, TradingMode
        
        manager = ModeManager(initial_mode=TradingMode.SEMI_AUTO)
        
        assert manager.current_mode == TradingMode.SEMI_AUTO
        assert manager.is_semi_auto == True
        assert manager.is_manual == False
    
    def test_mode_switching(self):
        """Test mode switching."""
        from src.modes.mode_manager import ModeManager, TradingMode
        
        manager = ModeManager()
        
        result = manager.set_mode(TradingMode.MANUAL, "Testing")
        
        assert result == True
        assert manager.current_mode == TradingMode.MANUAL
        assert len(manager.mode_history) == 2
    
    def test_same_mode_no_change(self):
        """Test same mode doesn't create duplicate history."""
        from src.modes.mode_manager import ModeManager, TradingMode
        
        manager = ModeManager()
        initial_history_count = len(manager.mode_history)
        
        manager.set_mode(TradingMode.SEMI_AUTO)
        
        assert len(manager.mode_history) == initial_history_count
    
    def test_execution_allowed(self):
        """Test execution allowed check."""
        from src.modes.mode_manager import ModeManager, TradingMode
        
        manager = ModeManager()
        
        allowed, reason = manager.is_execution_allowed(
            confidence=0.7,
            position_size=1.0,
            current_daily_loss=0.01
        )
        
        assert allowed == False
        assert "Auto-execution is disabled" in reason
    
    def test_full_auto_execution(self):
        """Test execution in full auto mode."""
        from src.modes.mode_manager import ModeManager, TradingMode
        
        manager = ModeManager(initial_mode=TradingMode.FULL_AUTO)
        
        allowed, reason = manager.is_execution_allowed(
            confidence=0.7,
            position_size=5.0,
            current_daily_loss=0.01
        )
        
        assert allowed == True
        assert "Execution allowed" in reason
    
    def test_emergency_stop(self):
        """Test emergency stop functionality."""
        from src.modes.mode_manager import ModeManager, TradingMode
        
        manager = ModeManager(initial_mode=TradingMode.FULL_AUTO)
        
        manager.activate_emergency_stop("Test stop")
        
        assert manager.is_emergency_stop == True
        assert manager.can_execute == False
        
        manager.deactivate_emergency_stop()
        
        assert manager.is_emergency_stop == False
    
    def test_mode_summary(self):
        """Test mode summary."""
        from src.modes.mode_manager import ModeManager, TradingMode
        
        manager = ModeManager()
        summary = manager.get_mode_summary()
        
        assert "current_mode" in summary
        assert "config" in summary
        assert "emergency_stop" in summary


class TestExecutionController:
    """Tests for Execution Controller."""
    
    def test_trade_proposal_creation(self):
        """Test TradeProposal creation."""
        from src.modes.execution_controller import TradeProposal
        
        proposal = TradeProposal(
            timestamp=datetime.now(),
            symbol="EURUSD",
            side="BUY",
            volume=1.0,
            entry_price=1.0850,
            sl=1.0750,
            tp=1.0950,
            confidence=0.75,
            strategy="Test Strategy",
            reasoning=["Reason 1", "Reason 2"]
        )
        
        assert proposal.symbol == "EURUSD"
        assert proposal.order_id is not None
        assert proposal.risk_reward_ratio > 0
    
    def test_execution_result_creation(self):
        """Test ExecutionResult creation."""
        from src.modes.execution_controller import ExecutionResult, ExecutionStatus, ExecutionReason
        
        result = ExecutionResult(
            order_id="test123",
            status=ExecutionStatus.EXECUTED,
            reason=ExecutionReason.SIGNAL,
            timestamp=datetime.now()
        )
        
        assert result.order_id == "test123"
        assert result.status == ExecutionStatus.EXECUTED
    
    def test_controller_creation(self):
        """Test ExecutionController creation."""
        from src.modes.execution_controller import create_execution_controller
        from src.modes.mode_manager import create_mode_manager
        
        mode_manager = create_mode_manager("semi_auto")
        controller = create_execution_controller(mode=mode_manager)
        
        assert controller.mode_manager.current_mode.value == "semi_auto"
    
    def test_process_signal_manual_mode(self):
        """Test signal processing in manual mode."""
        from src.modes.execution_controller import TradeProposal, create_execution_controller
        
        controller = create_execution_controller(mode="manual")
        
        proposal = TradeProposal(
            timestamp=datetime.now(),
            symbol="EURUSD",
            side="BUY",
            volume=1.0,
            entry_price=1.0850,
            sl=1.0750,
            tp=1.0950,
            confidence=0.75,
            strategy="Test",
            reasoning=[]
        )
        
        result = asyncio.run(controller.process_signal(proposal))
        
        assert result.status.value == "PENDING"
        assert len(controller.get_pending_proposals()) == 1
    
    def test_execution_statistics(self):
        """Test execution statistics."""
        from src.modes.execution_controller import create_execution_controller
        
        controller = create_execution_controller()
        stats = controller.get_execution_statistics()
        
        assert "total_signals" in stats
        assert "executed" in stats
        assert "pending" in stats


class TestTerminalDashboard:
    """Tests for Terminal Dashboard."""
    
    def test_dashboard_creation(self):
        """Test Dashboard creation."""
        from src.ui.terminal_dashboard import TerminalDashboard, DashboardConfig
        
        config = DashboardConfig(
            refresh_rate=2.0,
            show_positions=True,
            chart_candles=20
        )
        
        dashboard = TerminalDashboard(config=config)
        
        assert dashboard.config.refresh_rate == 2.0
        assert dashboard.config.chart_candles == 20
    
    def test_demo_snapshot(self):
        """Test demo snapshot generation."""
        from src.ui.terminal_dashboard import TerminalDashboard
        
        dashboard = TerminalDashboard()
        snapshot = dashboard._get_demo_snapshot()
        
        assert "account" in snapshot
        assert "positions" in snapshot
        assert snapshot["account"]["balance"] > 0
    
    def test_demo_candles(self):
        """Test demo candle data."""
        from src.ui.terminal_dashboard import TerminalDashboard
        
        dashboard = TerminalDashboard()
        candles = dashboard._get_demo_candles()
        
        assert len(candles) == 40
        assert "open" in candles[0]
        assert "close" in candles[0]
    
    def test_demo_signals(self):
        """Test demo signal data."""
        from src.ui.terminal_dashboard import TerminalDashboard
        
        dashboard = TerminalDashboard()
        signals = dashboard._get_demo_signals()
        
        assert len(signals) == 10
        assert "signal" in signals[0]
        assert "confidence" in signals[0]


async def test_async_monitoring():
    """Test async monitoring functionality."""
    from src.monitoring.portfolio_monitor import PortfolioMonitor
    
    monitor = PortfolioMonitor()
    
    assert monitor.running == False
    
    monitor.subscribe(lambda p, t, d: None)
    
    assert len(monitor._subscribers) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
