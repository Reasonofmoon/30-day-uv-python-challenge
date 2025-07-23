# 🧮 Day 1: uv로 60분 만에 스마트 계산기 CLI 만들기

> **30일 uv Python 마스터 챌린지 - Day 1/30**  
> **테마**: CLI 개발 & 현대적 Python 도구

처음으로 uv 패키지 매니저를 사용해서 실무급 CLI 애플리케이션을 만들어봤다. 60분 만에 테스트까지 완벽한 스마트 계산기를 완성했는데, 그 과정을 모두 기록해봤다.

---

## 🎯 오늘의 목표

**기능이 풍부한 명령줄 계산기**를 만들어서 현대적인 Python 개발 관행을 배우자.

### 사용한 핵심 도구들

- **uv**: 차세대 Python 패키지 매니저
- **typer**: 현대적 CLI 프레임워크
- **rich**: 터미널 UI 라이브러리
- **pytest**: 테스트 프레임워크

---

## ⏰ 개발 과정 (실제 60분 기록)

### **1단계: 프로젝트 셋업 (10분)**

처음 uv를 사용해보는 거라 설치부터 시작했다.

```bash
# uv 설치 확인
uv --version

# 프로젝트 생성
mkdir day01-smart-calculator
cd day01-smart-calculator
uv init

# 필요한 패키지 설치
uv add rich typer
uv add --dev pytest pytest-cov ruff black
```

**첫 인상:** uv가 정말 빠르다! pip 대비 10배는 빠른 것 같다.

### **2단계: 핵심 기능 구현 (30분)**

#### **계산기 엔진 설계**

객체지향으로 설계하기로 했다. `SmartCalculator` 클래스에 모든 기능을 담았다.

```python
class SmartCalculator:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.memory: float = 0.0
    
    def evaluate(self, expression: str) -> float:
        # 수학 함수 처리
        expression = self._process_functions(expression)
        
        # 안전한 계산
        result = eval(expression)  # 보안 검증 포함
        
        # 히스토리 저장
        self.history.append({
            'expression': original_expr,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        return result
```

**가장 어려웠던 부분:** 정규표현식으로 입력 검증하기

#### **CLI 인터페이스 구현**

처음에는 typer와 rich를 사용하려 했지만, Windows 호환성 문제로 간단한 방식으로 변경했다.

```python
def main():
    if len(sys.argv) < 2:
        print("Smart Calculator")
        print("Usage:")
        print("  python main.py calculate '2 + 3'")
        print("  python main.py interactive")
        return
    
    command = sys.argv[1]
    calc = SmartCalculator()
    
    if command == "calculate":
        expression = sys.argv[2]
        try:
            result = calc.evaluate(expression)
            print(f"Result: {expression} = {result}")
        except CalculatorError as e:
            print(f"Error: {e}")
```

### **3단계: 테스트 작성 (15분)**

TDD(Test-Driven Development)를 처음 시도해봤다.

```python
def test_basic_arithmetic():
    calc = SmartCalculator()
    
    assert calc.evaluate("2 + 3") == 5
    assert calc.evaluate("sqrt(16)") == 4

def test_error_handling():
    calc = SmartCalculator()
    
    with pytest.raises(CalculatorError):
        calc.evaluate("1 / 0")
```

**배운 점:** 테스트를 먼저 작성하니까 버그를 미리 찾을 수 있었다.

### **4단계: 실행 및 디버깅 (5분)**

```bash
# 테스트 실행
uv run pytest tests/ -v

# 실제 실행
uv run python src/smart_calculator/main.py calculate "sqrt(16)"
```

---

## 🐛 만난 문제들과 해결 과정

### **문제 1: ImportError - SmartCalculator를 찾을 수 없음**

```
ImportError: cannot import name 'SmartCalculator' from 'src.smart_calculator.calculator'
```

**원인:** calculator.py 파일에 코드가 제대로 저장되지 않았음

**해결:** 파일을 다시 열어서 코드를 완전히 복사-붙여넣기

### **문제 2: 정규표현식 검증 오류**

```
CalculatorError: 허용되지 않은 문자가 포함되어 있습니다
```

**원인:** `sqrt(16)` → `math.sqrt(16)`으로 변환된 후, `math`라는 문자가 정규식에서 허용되지 않음

**해결:** 정규식을 `r'^[0-9+\-*/().\s]+`에서 `r'^[0-9+\-*/().\sa-z_]+`로 수정

### **문제 3: Unicode 인코딩 에러**

```
UnicodeEncodeError: 'cp949' codec can't encode character '\U0001f9ee'
```

**원인:** Windows 터미널에서 이모지 문자 지원 안 됨

**해결:** 모든 이모지를 일반 텍스트로 교체

---

## 🎉 완성된 결과물

### **단일 계산 모드**

```bash
$ uv run python src/smart_calculator/main.py calculate "sqrt(16)"
Result: sqrt(16) = 4.0

$ uv run python src/smart_calculator/main.py calculate "(5 + 3) * 2"
Result: (5 + 3) * 2 = 16
```

### **대화형 모드**

```
Interactive Calculator Mode
Type 'quit' to exit.

calc> 2 + 3 * 4
= 14
calc> sqrt(25)
= 5.0
calc> pi * 2
= 6.283185307179586
calc> history
Calculation History:
  1. 2 + 3 * 4 = 14
  2. sqrt(25) = 5.0
  3. pi * 2 = 6.283185307179586
calc> quit
Goodbye!
```

### **테스트 결과**

```bash
$ uv run pytest tests/ -v
===== test session starts =====
tests/test_calculator.py::test_basic_arithmetic PASSED      [ 20%]
tests/test_calculator.py::test_complex_expressions PASSED   [ 40%]
tests/test_calculator.py::test_functions PASSED             [ 60%]
tests/test_calculator.py::test_history PASSED               [ 80%]
tests/test_calculator.py::test_error_handling PASSED        [100%]

===== 5 passed in 0.05s =====
```

---

## 💡 배운 점들

### **기술적 측면**

1. **uv의 강력함**: pip + venv + pip-tools를 하나로 통합한 혁신적 도구
2. **모던 Python 개발**: 깔끔한 프로젝트 구조와 의존성 관리
3. **TDD의 중요성**: 테스트 먼저 작성하니 더 안정적인 코드 작성
4. **에러 처리의 중요성**: 사용자 친화적인 예외 메시지의 가치
5. **정규표현식**: 입력 검증에서 핵심적인 역할

### **개발 프로세스 측면**

1. **작은 단위로 개발**: 한 번에 모든 걸 만들려 하지 말고 단계별로
2. **문제 해결 능력**: 에러 메시지를 꼼꼼히 읽고 원인 파악하기
3. **문서화의 중요성**: 코드에 주석과 docstring 작성 습관
4. **도구 활용**: 좋은 도구를 사용하면 개발 효율성이 10배 향상

### **개인적 성장**

1. **자신감 향상**: "나도 실무급 도구를 만들 수 있구나!"
2. **문제 해결 인내심**: 에러가 나도 차근차근 해결하는 능력
3. **학습 욕구**: 더 많은 기능을 추가하고 싶어짐

---

## 🏗️ 프로젝트 구조

최종적으로 완성된 프로젝트 구조:

```
day01-smart-calculator/
├── src/
│   └── smart_calculator/
│       ├── __init__.py
│       ├── main.py          # CLI 진입점
│       ├── calculator.py    # 핵심 계산기 클래스
│       └── cli.py          # CLI 유틸리티
├── tests/
│   ├── __init__.py
│   └── test_calculator.py  # 테스트 스위트
├── pyproject.toml          # uv 프로젝트 설정
├── uv.lock                # 의존성 잠금 파일
└── README.md              # 프로젝트 문서
```

---

## 🔥 앞으로의 계획

### **Day 2 예고: 웹 크롤러 프로젝트**
- requests + BeautifulSoup4로 실전 웹 스크래핑
- 뉴스 헤드라인 자동 수집
- pandas로 데이터 분석 및 CSV 저장
- 스케줄링으로 자동화

### **30일 챌린지 로드맵**
- **Week 1**: 기초 도구들 (계산기, 크롤러, 스크립트)
- **Week 2**: 웹 애플리케이션 (FastAPI, 데이터베이스)
- **Week 3**: 데이터 사이언스 (분석, 시각화)
- **Week 4**: 실무 프로젝트 (통합 시스템, 오픈소스 기여)

---

## 🎯 마무리

**60분 만에 실무급 CLI 애플리케이션을 완성**했다는 게 아직도 신기하다.

특히 uv의 빠른 속도와 간편함, 체계적인 테스트 작성, 실제 동작하는 인터랙티브 인터페이스가 인상 깊었다.

무엇보다 **"처음부터 끝까지 완성했다"**는 성취감이 크다. 테스트까지 작성하고, 에러도 해결하고, 실제로 작동하는 프로그램을 만들었다.

**Day 1에서 이 정도라면, 30일 후에는 얼마나 성장해있을까?** 정말 기대된다! 🚀

---

## 📝 소스코드

전체 소스코드는 GitHub에 올려뒀다: [30-day-uv-python-challenge](https://github.com/Reasonofmoon/30-day-uv-python-challenge)

```bash
# 직접 실행해보고 싶다면
git clone https://github.com/Reasonofmoon/30-day-uv-python-challenge.git
cd 30-day-uv-python-challenge/day01-smart-calculator
uv sync
uv run python src/smart_calculator/main.py interactive
```

---

**다음 포스팅은 Day 2 - 웹 크롤러 개발기로 찾아뵙겠습니다!** 

**함께 성장하는 개발자가 되어요! 💪**

---

*#Python #uv #CLI #개발일기 #30일챌린지 #초보개발자 #계산기 #pytest*

---

**Created by [Reasonofmoon](https://v0-neobrutalist-ui-design-sigma-seven.vercel.app/) | uv Python Developer Journey**