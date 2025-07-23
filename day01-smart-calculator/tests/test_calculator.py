"""
계산기 테스트
"""
import pytest
from src.smart_calculator.calculator import SmartCalculator, CalculatorError

def test_basic_arithmetic():
    """기본 사칙연산 테스트"""
    calc = SmartCalculator()
    
    assert calc.evaluate("2 + 3") == 5
    assert calc.evaluate("10 - 4") == 6
    assert calc.evaluate("3 * 4") == 12
    assert calc.evaluate("15 / 3") == 5

def test_complex_expressions():
    """복잡한 표현식 테스트"""
    calc = SmartCalculator()
    
    assert calc.evaluate("2 + 3 * 4") == 14
    assert calc.evaluate("(2 + 3) * 4") == 20

def test_functions():
    """함수 테스트"""
    calc = SmartCalculator()
    
    assert abs(calc.evaluate("sqrt(16)") - 4) < 0.001
    assert abs(calc.evaluate("pi") - 3.14159) < 0.01

def test_history():
    """히스토리 테스트"""
    calc = SmartCalculator()
    
    calc.evaluate("2 + 2")
    calc.evaluate("3 * 3")
    
    history = calc.get_history()
    assert len(history) == 2
    assert history[0]['result'] == 4
    assert history[1]['result'] == 9

def test_error_handling():
    """에러 처리 테스트"""
    calc = SmartCalculator()
    
    with pytest.raises(CalculatorError):
        calc.evaluate("1 / 0")