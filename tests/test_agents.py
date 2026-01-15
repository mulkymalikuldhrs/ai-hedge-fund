#!/usr/bin/env python3
"""
Unit tests for AI Agents Module
Tests run_multi_agent_analysis and agent output validation
"""

import sys
sys.path.insert(0, '.')

import pytest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np


class TestAgentOutputs:
    """Tests for agent output dataclasses"""
    
    def test_agent_output_fields(self):
        """Test AgentOutput has all required fields"""
        from src.agents.enhanced_agents import AgentOutput
        
        output = AgentOutput(
            agent_name="test_agent",
            ticker="AAPL",
            signal="buy",
            confidence=0.85,
            reasoning="Strong momentum",
            metadata={}
        )
        
        assert output.agent_name == "test_agent"
        assert output.ticker == "AAPL"
        assert output.signal == "buy"
        assert output.confidence == 0.85
        assert output.reasoning == "Strong momentum"
        assert isinstance(output.metadata, dict)
    
    def test_agent_output_confidence_range(self):
        """Test confidence is validated 0-1"""
        from src.agents.enhanced_agents import AgentOutput
        
        # Valid confidence
        output = AgentOutput(
            agent_name="test",
            ticker="AAPL",
            signal="buy",
            confidence=0.5,
            reasoning="test"
        )
        assert 0 <= output.confidence <= 1
    
    def test_agent_output_signal_types(self):
        """Test valid signal types"""
        from src.agents.enhanced_agents import AgentOutput
        
        for signal in ["buy", "sell", "hold"]:
            output = AgentOutput(
                agent_name="test",
                ticker="AAPL",
                signal=signal,
                confidence=0.5,
                reasoning="test"
            )
            assert output.signal == signal


class TestMultiAgentAnalysis:
    """Tests for multi-agent analysis function"""
    
    @pytest.fixture
    def sample_prices(self):
        """Generate sample price data"""
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', periods=100, freq='1D')
        closes = pd.Series(np.cumsum(np.random.randn(100)) + 100, index=dates)
        return closes.tolist()
    
    @pytest.fixture
    def sample_context(self):
        """Sample analysis context"""
        return {
            "market_condition": "bullish",
            "sector_performance": "positive",
            "volatility": "low"
        }
    
    def test_run_multi_agent_analysis_import(self):
        """Test run_multi_agent_analysis can be imported"""
        from src.agents.enhanced_agents import run_multi_agent_analysis
        assert callable(run_multi_agent_analysis)
    
    @patch('src.agents.enhanced_agents.call_llm')
    def test_single_ticker_analysis(self, mock_call_llm, sample_prices, sample_context):
        """Test analysis of single ticker"""
        from src.agents.enhanced_agents import run_multi_agent_analysis
        
        # Mock LLM response
        mock_call_llm.return_value = {
            "signal": "buy",
            "confidence": 0.75,
            "reasoning": "Test reasoning"
        }
        
        result = run_multi_agent_analysis("AAPL", sample_prices, sample_context)
        
        assert isinstance(result, dict)
        assert "AAPL" in result or len(result) > 0
    
    @patch('src.agents.enhanced_agents.call_llm')
    def test_multiple_tickers_analysis(self, mock_call_llm, sample_prices, sample_context):
        """Test analysis of multiple tickers"""
        from src.agents.enhanced_agents import run_multi_agent_analysis
        
        mock_call_llm.return_value = {
            "signal": "hold",
            "confidence": 0.60,
            "reasoning": "Test reasoning"
        }
        
        tickers = ["AAPL", "MSFT", "GOOGL"]
        result = run_multi_agent_analysis(tickers, sample_prices, sample_context)
        
        assert isinstance(result, dict)


class TestAgentSignals:
    """Tests for agent signal aggregation"""
    
    def test_signal_aggregation_import(self):
        """Test signal_aggregation can be imported"""
        from src.agents.signal_aggregation import aggregate_signals
        assert callable(aggregate_signals)
    
    def test_weighted_voting(self):
        """Test weighted voting of agent signals"""
        from src.agents.signal_aggregation import aggregate_signals
        
        signals = [
            {"agent": "simons", "signal": "buy", "confidence": 0.8, "weight": 1.5},
            {"agent": "momentum", "signal": "buy", "confidence": 0.7, "weight": 1.2},
            {"agent": "mean_reversion", "signal": "sell", "confidence": 0.6, "weight": 1.0},
        ]
        
        result = aggregate_signals(signals)
        
        assert "final_signal" in result
        assert "confidence" in result
        assert "details" in result


class TestJimSimonsAgent:
    """Tests for Jim Simons quantitative agent"""
    
    def test_import(self):
        """Test Jim Simons agent can be imported"""
        try:
            from src.agents.enhanced_agents import jim_simmons_agent
            assert callable(jim_simmons_agent)
        except ImportError:
            pytest.skip("Jim Simons agent not implemented yet")


class TestQuantitativeAnalystAgent:
    """Tests for Quantitative Analyst agent"""
    
    def test_import(self):
        """Test Quantitative Analyst agent can be imported"""
        try:
            from src.agents.enhanced_agents import quantitative_analyst_agent
            assert callable(quantitative_analyst_agent)
        except ImportError:
            pytest.skip("Quantitative Analyst agent not implemented yet")


class TestTechnicalAnalystAgent:
    """Tests for Technical Analyst agent"""
    
    def test_import(self):
        """Test Technical Analyst agent can be imported"""
        try:
            from src.agents.enhanced_agents import technical_analyst_agent
            assert callable(technical_analyst_agent)
        except ImportError:
            pytest.skip("Technical Analyst agent not implemented yet")


class TestDecisionParsing:
    """Tests for BUY/SELL/HOLD decision parsing"""
    
    def test_decision_from_string(self):
        """Test parsing decision from string"""
        from src.agents.enhanced_agents import parse_agent_decision
        
        for text in ["BUY", "Buy", "buy", " BUY "]:
            decision = parse_agent_decision(text)
            assert decision == "buy"
        
        for text in ["SELL", "Sell", "sell"]:
            decision = parse_agent_decision(text)
            assert decision == "sell"
        
        for text in ["HOLD", "Hold", "hold"]:
            decision = parse_agent_decision(text)
            assert decision == "hold"
    
    def test_invalid_decision(self):
        """Test handling of invalid decisions"""
        from src.agents.enhanced_agents import parse_agent_decision
        
        decision = parse_agent_decision("INVALID")
        assert decision is None or decision == "hold"


class TestConfidenceCalculation:
    """Tests for confidence score calculation"""
    
    def test_confidence_weighted_average(self):
        """Test weighted average confidence calculation"""
        from src.agents.enhanced_agents import calculate_weighted_confidence
        
        confidences = [0.8, 0.7, 0.9]
        weights = [1.5, 1.2, 1.0]
        
        result = calculate_weighted_confidence(confidences, weights)
        
        assert isinstance(result, float)
        assert 0 <= result <= 1
    
    def test_confidence_from_agents(self):
        """Test extracting confidence from agent outputs"""
        from src.agents.enhanced_agents import extract_agent_confidences
        
        agents = [
            {"signal": "buy", "confidence": 0.8},
            {"signal": "buy", "confidence": 0.7},
            {"signal": "sell", "confidence": 0.6},
        ]
        
        result = extract_agent_confidences(agents)
        
        assert len(result) == 3
        assert all(0 <= c <= 1 for c in result)


class TestAgentMetadata:
    """Tests for agent metadata handling"""
    
    def test_metadata_passthrough(self):
        """Test metadata is passed through correctly"""
        from src.agents.enhanced_agents import AgentOutput
        
        metadata = {
            "indicators_used": ["RSI", "MACD"],
            "timeframe": "1d",
            "additional_info": "test"
        }
        
        output = AgentOutput(
            agent_name="test",
            ticker="AAPL",
            signal="buy",
            confidence=0.75,
            reasoning="test",
            metadata=metadata
        )
        
        assert output.metadata == metadata
        assert output.metadata["indicators_used"] == ["RSI", "MACD"]


class TestEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_empty_price_data(self):
        """Test handling of empty price data"""
        from src.agents.enhanced_agents import run_multi_agent_analysis
        
        result = run_multi_agent_analysis("AAPL", [], {})
        
        # Should return fallback or empty result
        assert isinstance(result, dict)
    
    def test_missing_context(self):
        """Test handling of missing context"""
        from src.agents.enhanced_agents import run_multi_agent_analysis
        
        prices = [100, 101, 102, 103, 104]
        result = run_multi_agent_analysis("AAPL", prices, None)
        
        assert isinstance(result, dict)
    
    def test_long_price_history(self):
        """Test handling of long price history"""
        from src.agents.enhanced_agents import run_multi_agent_analysis
        
        # 1000 days of data
        prices = list(range(100, 1100))
        result = run_multi_agent_analysis("AAPL", prices, {})
        
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
