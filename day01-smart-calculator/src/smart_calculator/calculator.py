"""
스마트 계산기 엔진
"""
import math
import re
from datetime import datetime
from typing import List, Dict, Any

class CalculatorError(Exception):
    """계산기 예외"""
    pass

class SmartCalculator:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.memory: float = 0.0
    
    def evaluate(self, expression: str) -> float:
        """수학 표현식 계산"""
        try:
            # 기본 정리
            expression = expression.strip().lower()
            original_expr = expression
            
            # 특수 함수 처리
            expression = self._process_functions(expression)
            
            # 안전한 계산을 위한 문자 검증 (수학 함수 허용)
            if not re.match(r'^[0-9+\-*/().\sa-z_]+$', expression):
                raise CalculatorError("허용되지 않은 문자가 포함되어 있습니다")
            
            # 계산 실행
            result = eval(expression)
            
            # 히스토리 저장
            self.history.append({
                'expression': original_expr,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
            
            return result
            
        except ZeroDivisionError:
            raise CalculatorError("0으로 나눌 수 없습니다")
        except Exception as e:
            raise CalculatorError(f"계산 오류: {str(e)}")
    
    def _process_functions(self, expression: str) -> str:
        """수학 함수 처리"""
        # sqrt(x) -> math.sqrt(x)
        expression = re.sub(r'sqrt\(([^)]+)\)', r'math.sqrt(\1)', expression)
        # pi, e 상수
        expression = expression.replace('pi', str(math.pi))
        expression = expression.replace('e', str(math.e))
        return expression
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """계산 히스토리 조회"""
        return self.history[-limit:]
    
    def clear_history(self):
        """히스토리 초기화"""
        self.history.clear()