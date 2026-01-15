#!/usr/bin/env python3
"""
Unit tests for LLM JSON Parsing Module
Tests OpenCodeChatModel and PuterChatModel JSON extraction
"""

import sys
sys.path.insert(0, '.')

import pytest
from unittest.mock import Mock, patch
import json


class TestJSONParsing:
    """Tests for JSON extraction from LLM responses"""
    
    def test_extract_json_from_markdown_code_block(self):
        """Test extraction of JSON from markdown code blocks"""
        from src.llm.parsing import extract_json_from_response
        
        response = """
Here is the analysis you requested:

```json
{
    "signal": "buy",
    "confidence": 85,
    "reasoning": "Strong momentum indicators"
}
```

Let me know if you need more details.
"""
        result = extract_json_from_response(response)
        assert result is not None
        assert result['signal'] == 'buy'
        assert result['confidence'] == 85
    
    def test_extract_json_without_code_block(self):
        """Test extraction of JSON without markdown code blocks"""
        from src.llm.parsing import extract_json_from_response
        
        response = '{"signal": "sell", "confidence": 70, "reasoning": "Overbought conditions"}'
        result = extract_json_from_response(response)
        assert result is not None
        assert result['signal'] == 'sell'
    
    def test_extract_json_with_partial_content(self):
        """Test extraction when response has partial JSON"""
        from src.llm.parsing import extract_json_from_response
        
        response = """
The market analysis shows:
{"signal": "hold", "confidence": 60
Please consider the following factors...
"""
        result = extract_json_from_response(response)
        # Should handle gracefully or return None
        assert result is None or isinstance(result, dict)
    
    def test_invalid_json_returns_none(self):
        """Test that invalid JSON returns None"""
        from src.llm.parsing import extract_json_from_response
        
        response = "This is not JSON at all"
        result = extract_json_from_response(response)
        assert result is None
    
    def test_empty_response(self):
        """Test handling of empty response"""
        from src.llm.parsing import extract_json_from_response
        
        result = extract_json_from_response("")
        assert result is None
        
        result = extract_json_from_response(None)
        assert result is None


class TestPartialFieldExtraction:
    """Tests for partial JSON field extraction"""
    
    def test_extract_single_field(self):
        """Test extraction of a single field from response"""
        from src.llm.parsing import extract_field_from_response
        
        response = '{"signal": "buy", "confidence": 85}'
        result = extract_field_from_response(response, 'signal')
        assert result == 'buy'
    
    def test_extract_missing_field(self):
        """Test extraction of missing field returns None"""
        from src.llm.parsing import extract_field_from_response
        
        response = '{"signal": "buy"}'
        result = extract_field_from_response(response, 'confidence')
        assert result is None
    
    def test_extract_numeric_confidence(self):
        """Test confidence extraction as integer"""
        from src.llm.parsing import extract_field_from_response
        
        response = '{"confidence": 85.5}'
        result = extract_field_from_response(response, 'confidence')
        assert result == 85.5


class TestSignalParsing:
    """Tests for trading signal parsing"""
    
    def test_parse_buy_signal(self):
        """Test parsing of BUY signal"""
        from src.llm.parsing import parse_trading_signal
        
        for signal_text in ['BUY', 'buy', 'Buy', 'BUY ', '  buy']:
            result = parse_trading_signal(signal_text)
            assert result == 'buy', f"Failed for {signal_text}"
    
    def test_parse_sell_signal(self):
        """Test parsing of SELL signal"""
        from src.llm.parsing import parse_trading_signal
        
        for signal_text in ['SELL', 'sell', 'Sell', 'SELL ', '  sell']:
            result = parse_trading_signal(signal_text)
            assert result == 'sell', f"Failed for {signal_text}"
    
    def test_parse_hold_signal(self):
        """Test parsing of HOLD signal"""
        from src.llm.parsing import parse_trading_signal
        
        for signal_text in ['HOLD', 'hold', 'Hold', 'HOLD ', '  hold']:
            result = parse_trading_signal(signal_text)
            assert result == 'hold', f"Failed for {signal_text}"
    
    def test_parse_invalid_signal(self):
        """Test parsing of invalid signal returns None"""
        from src.llm.parsing import parse_trading_signal
        
        result = parse_trading_signal('INVALID')
        assert result is None


class TestConfidenceNormalization:
    """Tests for confidence score normalization"""
    
    def test_confidence_0_to_1(self):
        """Test confidence normalized to 0-1 range"""
        from src.llm.parsing import normalize_confidence
        
        assert normalize_confidence(0.75) == 0.75
        assert normalize_confidence(1) == 1.0
        assert normalize_confidence(0) == 0.0
    
    def test_confidence_percentage_to_decimal(self):
        """Test confidence percentage converted to decimal"""
        from src.llm.parsing import normalize_confidence
        
        assert normalize_confidence(75) == 0.75
        assert normalize_confidence(100) == 1.0
        assert normalize_confidence(0) == 0.0
    
    def test_confidence_out_of_range(self):
        """Test confidence values clamped to 0-1"""
        from src.llm.parsing import normalize_confidence
        
        # Values above 1 should be clamped
        assert normalize_confidence(150) == 1.0
        # Values below 0 should be clamped
        assert normalize_confidence(-10) == 0.0


class TestFallbackHandling:
    """Tests for fallback mechanisms"""
    
    def test_fallback_response_structure(self):
        """Test fallback response has correct structure"""
        from src.llm.parsing import create_fallback_response
        
        result = create_fallback_response()
        assert 'signal' in result
        assert 'confidence' in result
        assert 'reasoning' in result
        assert result['signal'] == 'hold'
        assert result['confidence'] == 0.0
    
    def test_fallback_with_ticker(self):
        """Test fallback response includes ticker info"""
        from src.llm.parsing import create_fallback_response
        
        result = create_fallback_response('AAPL')
        assert 'ticker' in result or 'symbol' in result.lower()


class TestJSONValidation:
    """Tests for JSON schema validation"""
    
    def test_validate_trading_signal_schema(self):
        """Test validation of trading signal JSON schema"""
        from src.llm.parsing import validate_signal_schema
        
        valid_signal = {
            'signal': 'buy',
            'confidence': 85,
            'reasoning': 'Strong upward momentum'
        }
        assert validate_signal_schema(valid_signal) == True
    
    def test_validate_missing_fields(self):
        """Test validation fails for missing required fields"""
        from src.llm.parsing import validate_signal_schema
        
        invalid_signal = {
            'signal': 'buy'
            # Missing confidence and reasoning
        }
        assert validate_signal_schema(invalid_signal) == False
    
    def test_validate_invalid_signal_type(self):
        """Test validation fails for invalid signal type"""
        from src.llm.parsing import validate_signal_schema
        
        invalid_signal = {
            'signal': 'invalid_signal',
            'confidence': 85,
            'reasoning': 'Some reasoning'
        }
        assert validate_signal_schema(invalid_signal) == False
    
    def test_validate_invalid_confidence(self):
        """Test validation fails for invalid confidence"""
        from src.llm.parsing import validate_signal_schema
        
        invalid_signal = {
            'signal': 'buy',
            'confidence': 150,  # Out of range
            'reasoning': 'Some reasoning'
        }
        assert validate_signal_schema(invalid_signal) == False


class TestErrorHandling:
    """Tests for error handling in parsing"""
    
    def test_malformed_json_recovery(self):
        """Test recovery from malformed JSON"""
        from src.llm.parsing import extract_json_from_response
        
        # JSON with trailing comma (invalid)
        response = '{"signal": "buy", "confidence": 85,}'
        result = extract_json_from_response(response)
        # Should handle gracefully
        assert result is None or isinstance(result, dict)
    
    def test_unicode_handling(self):
        """Test handling of unicode characters in JSON"""
        from src.llm.parsing import extract_json_from_response
        
        response = '{"signal": "buy", "reasoning": "Strong momentum 📈"}'
        result = extract_json_from_response(response)
        assert result is not None
        assert '📈' in result['reasoning']
    
    def test_nested_json(self):
        """Test handling of nested JSON structures"""
        from src.llm.parsing import extract_json_from_response
        
        response = """
        {
            "signal": "buy",
            "confidence": 85,
            "metadata": {
                "indicators": ["RSI", "MACD"],
                "timeframe": "1d"
            }
        }
        """
        result = extract_json_from_response(response)
        assert result is not None
        assert result['signal'] == 'buy'
        assert 'indicators' in result['metadata']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
