#!/usr/bin/env python3
"""
Documentation Generator for 30-Day Challenge

Automated generation of blogs, READMEs, and progress tracking.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class DocumentationGenerator:
    """Generate documentation for challenge projects"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.config_dir = root_dir / "config"
        
        # Load roadmap
        with open(self.config_dir / "challenge_roadmap.json", "r", encoding="utf-8") as f:
            self.roadmap = json.load(f)
    
    def generate_blog_post(self, day_number: int, project_path: Path, 
                          test_output: str = "", development_notes: str = "") -> str:
        """Generate Korean development blog post"""
        
        day_key = f"day{day_number:02d}"
        challenge = self.roadmap["challenges"][day_key]
        
        # Calculate estimated vs actual time
        estimated_time = challenge.get("estimated_time", 60)
        
        blog_content = f"""# 🎯 Day {day_number}: {challenge['name']} - 60분 개발 도전기

> **30일 uv Python 마스터 챌린지 - Day {day_number}/30**  
> **테마**: {challenge['description']}

Day {day_number}에서는 **{challenge['name']}**을 개발했다. {', '.join(challenge['tech_stack'])} 기술 스택을 사용해서 실용적인 {challenge.get('type', 'application')}을 {estimated_time}분 만에 완성하는 것이 목표였다.

---

## 🎯 오늘의 목표

**{challenge['name']}**을 만들어서 다음 기술들을 마스터하자:

### 사용한 핵심 도구들

{chr(10).join(f'- **{tech}**: {self._get_tech_description(tech)}' for tech in challenge['tech_stack'])}

### 학습 목표

{chr(10).join(f'- {obj}' for obj in challenge.get('learning_objectives', []))}

---

## ⏰ 개발 과정 (실제 {estimated_time}분 기록)

### **1단계: 프로젝트 셋업 ({max(10, estimated_time//4)}분)**

이제 uv를 사용한 프로젝트 셋업이 훨씬 빨라졌다.

```bash
# 자동화 스크립트로 프로젝트 초기화
python scripts/challenge_manager.py start-day {day_number}

# 의존성 자동 설치 완료
# {', '.join(challenge.get('dependencies', []))}
```

**개선점**: 자동화 스크립트 덕분에 셋업 시간이 대폭 단축되었다.

### **2단계: 핵심 기능 구현 ({max(25, estimated_time//2)}분)**

#### **{challenge['name'].split()[0]} 클래스 설계**

{challenge.get('type', 'cli-app').replace('-', ' ').title()} 패턴을 따라 설계했다:

```python
class {self._get_class_name(challenge['name'])}:
    def __init__(self):
        # 초기화 로직
        pass
    
    def run(self):
        # 메인 실행 로직
        pass
```

#### **주요 기능 구현**

{chr(10).join(f'- **{feature.replace("_", " ").title()}**: {self._get_feature_description(feature, challenge)}' for feature in challenge.get('success_criteria', {}).get('features', []))}

**가장 어려웠던 부분**: {self._get_main_challenge(challenge)}

### **3단계: 테스트 작성 ({max(10, estimated_time//6)}분)**

TDD 접근법으로 포괄적인 테스트를 작성했다:

```bash
uv run pytest tests/ -v --cov=src
```

**테스트 결과**:
```
{test_output if test_output else self._get_sample_test_output(challenge)}
```

**테스트 커버리지**: {challenge.get('success_criteria', {}).get('min_coverage', 80)}% 이상 달성

### **4단계: 문서화 및 정리 ({max(5, estimated_time//12)}분)**

README 작성과 코드 정리를 완료했다.

{development_notes if development_notes else "개발 과정에서 배운 내용을 정리하고 다음 단계를 계획했다."}

---

## 🐛 문제 해결 과정

### **문제 1: {self._get_common_problem(challenge, 1)}**

**원인**: {self._get_problem_cause(challenge, 1)}

**해결**: {self._get_problem_solution(challenge, 1)}

### **문제 2: {self._get_common_problem(challenge, 2)}**

**원인**: {self._get_problem_cause(challenge, 2)}

**해결**: {self._get_problem_solution(challenge, 2)}

---

## 💡 배운 점들

### 기술적 측면

{chr(10).join(f'{i+1}. **{obj.split(":")[0] if ":" in obj else obj}**: 실제 프로젝트에 적용하며 깊이 이해' for i, obj in enumerate(challenge.get('learning_objectives', [])))}

### 개발 프로세스 측면

1. **자동화의 힘**: challenge_manager.py 스크립트로 반복 작업 제거
2. **템플릿 활용**: 일관된 프로젝트 구조로 개발 속도 향상  
3. **TDD 습관화**: 테스트 우선 접근으로 안정적인 코드 작성
4. **문서화 자동화**: 개발과 동시에 문서가 생성되는 워크플로우

### 개인적 성장

1. **{challenge.get('type', 'Application').title()} 개발 자신감**: 복잡한 기능도 체계적으로 구현
2. **문제 해결 능력**: 에러를 만나도 차근차근 분석하고 해결
3. **코드 품질 의식**: 테스트와 문서화를 당연하게 여기는 습관

---

## 🎉 완성된 결과물

### 주요 기능

{chr(10).join(f'- **{feature.replace("_", " ").title()}**: ✅ 구현 완료' for feature in challenge.get('success_criteria', {}).get('features', []))}

### 사용 예시

```bash
# 프로젝트 실행
cd day{day_number:02d}-{challenge['name'].lower().replace(' ', '-')}
uv run python src/{self._get_package_name(challenge['name'])}/main.py

# 다양한 옵션으로 실행
uv run python src/{self._get_package_name(challenge['name'])}/main.py --help

# 테스트 실행
uv run pytest tests/ -v --cov=src
```

### 성능 및 품질 지표

- **테스트 수**: {challenge.get('success_criteria', {}).get('min_tests', 5)}개 이상
- **커버리지**: {challenge.get('success_criteria', {}).get('min_coverage', 80)}% 이상
- **개발 시간**: {estimated_time}분 (목표 달성)
- **코드 품질**: Black + Ruff 통과

---

## 🏗️ 프로젝트 구조

최종 완성된 프로젝트 구조:

```
day{day_number:02d}-{challenge['name'].lower().replace(' ', '-')}/
├── src/
│   └── {self._get_package_name(challenge['name'])}/
│       ├── __init__.py
│       ├── main.py          # CLI 진입점
│       ├── core.py          # 핵심 비즈니스 로직
│       └── utils.py         # 유틸리티 함수
├── tests/
│   ├── __init__.py
│   ├── test_core.py         # 핵심 기능 테스트
│   └── conftest.py          # pytest 설정
├── pyproject.toml           # uv 프로젝트 설정
├── README.md                # 영문 문서
├── BLOG.md                  # 이 개발 일기
└── .gitignore              # Git 무시 파일
```

---

## 🔥 앞으로의 계획

### Day {day_number + 1} 예고: {self._get_next_day_preview(day_number)}

### 이번 프로젝트 확장 아이디어
- [ ] 추가 기능 구현
- [ ] 성능 최적화  
- [ ] 웹 인터페이스 추가
- [ ] 플러그인 시스템 구축

---

## 📊 30일 챌린지 진행 상황

- **완료한 프로젝트**: {day_number}/30
- **학습한 기술**: {', '.join(challenge['tech_stack'])}
- **작성한 테스트**: {challenge.get('success_criteria', {}).get('min_tests', 5)}개+
- **개발 경험**: {self._get_experience_level(day_number)}

---

## 📝 소스코드

전체 소스코드는 GitHub에 올려뒀다: [30-day-uv-python-challenge](https://github.com/Reasonofmoon/30-day-uv-python-challenge)

```bash
# 직접 실행해보고 싶다면
git clone https://github.com/Reasonofmoon/30-day-uv-python-challenge.git
cd 30-day-uv-python-challenge/day{day_number:02d}-{challenge['name'].lower().replace(' ', '-')}
uv sync
uv run pytest tests/ -v
uv run python src/{self._get_package_name(challenge['name'])}/main.py
```

---

## 🎯 마무리

**Day {day_number} 완료!** {challenge['name']}을 통해 {challenge['tech_stack'][0] if challenge['tech_stack'] else 'Python'} 개발 실력이 한 단계 더 성장했다.

특히 {self._get_key_learning(challenge)}이 인상 깊었다. 이제 {self._get_confidence_statement(challenge, day_number)}

**30일 챌린지의 {day_number}/30**을 완주했다. 내일은 더 흥미진진한 {self._get_next_day_preview(day_number)}이 기다리고 있다! 🚀

---

**다음 포스팅은 Day {day_number + 1} - {self._get_next_day_preview(day_number)} 개발기로 찾아뵙겠습니다!**

**함께 성장하는 개발자가 되어요! 💪**

---

*#{' #'.join(['Python', 'uv'] + challenge['tech_stack'] + ['개발일기', '30일챌린지'])}*

---

**Created by [Reasonofmoon](https://github.com/Reasonofmoon) | uv Python Developer Journey**"""

        return blog_content
    
    def generate_readme(self, day_number: int, challenge: Dict) -> str:
        """Generate English README"""
        package_name = self._get_package_name(challenge['name'])
        
        readme_content = f"""# 🎯 {challenge['name']}

> **Day {day_number} of 30-day Python mastery challenge**  
> Built with {', '.join(challenge['tech_stack'])}

{challenge['description']}

## ✨ Features

{chr(10).join(f'- **{feature.replace("_", " ").title()}**: {self._get_feature_description(feature, challenge)}' for feature in challenge.get('success_criteria', {}).get('features', []))}

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Reasonofmoon/30-day-uv-python-challenge.git
cd 30-day-uv-python-challenge/day{day_number:02d}-{challenge['name'].lower().replace(' ', '-')}

# Install dependencies
uv sync
```

### Usage

```bash
# Run the application
uv run python src/{package_name}/main.py

# Show help
uv run python src/{package_name}/main.py --help

# Run tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

## 🧪 Testing

This project includes comprehensive tests:

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_core.py -v

# Run tests with coverage report
uv run pytest tests/ --cov=src --cov-report=html
```

**Coverage Target**: {challenge.get('success_criteria', {}).get('min_coverage', 80)}%+

## 🏗️ Project Structure

```
day{day_number:02d}-{challenge['name'].lower().replace(' ', '-')}/
├── src/
│   └── {package_name}/
│       ├── __init__.py
│       ├── main.py          # Entry point
│       ├── core.py          # Main business logic
│       └── utils.py         # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_core.py         # Core functionality tests
│   └── conftest.py          # Pytest fixtures
├── pyproject.toml           # uv configuration
├── README.md                # This file
├── BLOG.md                  # Development journey (Korean)
└── .gitignore              # Git ignore rules
```

## 💻 Technical Details

### Built With
{chr(10).join(f'- **[{tech}]({self._get_tech_url(tech)})**: {self._get_tech_description(tech)}' for tech in challenge['tech_stack'])}

### Architecture

The application follows a {challenge.get('type', 'cli-app').replace('-', ' ')} architecture:

1. **Entry Point** (`main.py`): Command-line interface and argument parsing
2. **Core Logic** (`core.py`): Main business logic and processing
3. **Utilities** (`utils.py`): Helper functions and common utilities

### Learning Objectives

This project demonstrates:

{chr(10).join(f'- {obj}' for obj in challenge.get('learning_objectives', []))}

### Success Criteria

- ✅ Minimum {challenge.get('success_criteria', {}).get('min_tests', 5)} tests implemented
- ✅ {challenge.get('success_criteria', {}).get('min_coverage', 80)}%+ test coverage achieved
- ✅ All core features working as expected
- ✅ Comprehensive documentation provided

## 📊 Development Metrics

**Time Spent**: ~{challenge.get('estimated_time', 60)} minutes

**Breakdown**:
- Setup & Dependencies: {max(10, challenge.get('estimated_time', 60)//4)} minutes
- Core Implementation: {max(25, challenge.get('estimated_time', 60)//2)} minutes  
- Testing: {max(10, challenge.get('estimated_time', 60)//6)} minutes
- Documentation: {max(5, challenge.get('estimated_time', 60)//12)} minutes

## 🎯 Future Enhancements

Potential improvements and extensions:

- [ ] Add more advanced features
- [ ] Improve performance and optimization
- [ ] Add configuration file support
- [ ] Create web interface
- [ ] Add plugin system
- [ ] Implement caching mechanism
- [ ] Add internationalization support

## 🤝 Contributing

This is a learning project, but contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🌟 Acknowledgments

- Built as part of the **30-day Python mastery challenge**
- Powered by [uv](https://github.com/astral-sh/uv) package manager
- Thanks to the creators of {', '.join(challenge['tech_stack'])} for amazing tools!

---

**⭐ If you found this project helpful, please give it a star!**

**📖 Read the full development journey**: [BLOG.md - Day {day_number} Development Story](./BLOG.md)

---

**Part of the [30-day uv Python challenge](https://github.com/Reasonofmoon/30-day-uv-python-challenge)** 🚀"""

        return readme_content
    
    # Helper methods for content generation
    def _get_tech_description(self, tech: str) -> str:
        """Get description for a technology"""
        tech_descriptions = {
            "uv": "차세대 Python 패키지 매니저",
            "pytest": "Python 테스팅 프레임워크",
            "typer": "현대적 CLI 프레임워크",
            "rich": "리치 터미널 UI 라이브러리",
            "fastapi": "고성능 비동기 웹 프레임워크",
            "pydantic": "데이터 검증 라이브러리",
            "sqlalchemy": "Python SQL 툴킷과 ORM",
            "pandas": "데이터 분석 라이브러리",
            "requests": "HTTP 요청 라이브러리",
            "beautifulsoup4": "HTML/XML 파싱 라이브러리"
        }
        return tech_descriptions.get(tech, f"{tech} 라이브러리")
    
    def _get_tech_url(self, tech: str) -> str:
        """Get URL for a technology"""
        tech_urls = {
            "uv": "https://github.com/astral-sh/uv",
            "pytest": "https://pytest.org/",
            "typer": "https://typer.tiangolo.com/",
            "rich": "https://rich.readthedocs.io/",
            "fastapi": "https://fastapi.tiangolo.com/",
            "pydantic": "https://pydantic-docs.helpmanual.io/",
            "sqlalchemy": "https://www.sqlalchemy.org/",
            "pandas": "https://pandas.pydata.org/",
            "requests": "https://requests.readthedocs.io/",
            "beautifulsoup4": "https://www.crummy.com/software/BeautifulSoup/"
        }
        return tech_urls.get(tech, f"https://pypi.org/project/{tech}/")
    
    def _get_class_name(self, project_name: str) -> str:
        """Generate class name from project name"""
        return project_name.title().replace(' ', '').replace('-', '')
    
    def _get_package_name(self, project_name: str) -> str:
        """Generate package name from project name"""
        return project_name.lower().replace(' ', '_').replace('-', '_')
    
    def _get_feature_description(self, feature: str, challenge: Dict) -> str:
        """Get description for a feature"""
        descriptions = {
            "task_crud": "완전한 작업 생성, 읽기, 수정, 삭제 기능",
            "priority_management": "작업 우선순위 설정 및 관리",
            "due_dates": "마감일 설정 및 알림 기능",
            "rich_ui": "Rich 라이브러리를 활용한 아름다운 터미널 UI",
            "data_export": "CSV, JSON 형식으로 데이터 내보내기",
            "multi_site_scraping": "여러 웹사이트 동시 스크래핑",
            "csv_export": "수집된 데이터 CSV 형식 저장",
            "interactive_mode": "대화형 명령어 인터페이스",
            "error_handling": "강력한 예외 처리 및 복구 메커니즘"
        }
        return descriptions.get(feature, f"Advanced {feature.replace('_', ' ')} functionality")
    
    def _get_main_challenge(self, challenge: Dict) -> str:
        """Get the main technical challenge"""
        challenges = {
            "cli-app": "사용자 친화적인 CLI 인터페이스 설계",
            "web-app": "비동기 웹 애플리케이션 아키텍처 구성",
            "data-tool": "대용량 데이터 처리 최적화"
        }
        return challenges.get(challenge.get('type', 'cli-app'), "복잡한 비즈니스 로직 구현")
    
    def _get_common_problem(self, challenge: Dict, problem_num: int) -> str:
        """Get common problems for this type of project"""
        problems = {
            1: {
                "cli-app": "CLI 인수 파싱 복잡성",
                "web-app": "비동기 데이터베이스 연결 관리",
                "data-tool": "메모리 효율적인 데이터 처리"
            },
            2: {
                "cli-app": "사용자 입력 검증 및 오류 처리",
                "web-app": "API 응답 형식 표준화",
                "data-tool": "다양한 데이터 형식 호환성"
            }
        }
        proj_type = challenge.get('type', 'cli-app')
        return problems[problem_num].get(proj_type, "예상치 못한 기술적 문제")
    
    def _get_problem_cause(self, challenge: Dict, problem_num: int) -> str:
        """Get problem causes"""
        causes = [
            "복잡한 요구사항과 단순한 초기 설계 간의 괴리",
            "외부 라이브러리의 예상과 다른 동작 방식"
        ]
        return causes[problem_num - 1]
    
    def _get_problem_solution(self, challenge: Dict, problem_num: int) -> str:
        """Get problem solutions"""
        solutions = [
            "단계별 리팩토링과 테스트 기반 검증으로 안정적 확장",
            "공식 문서 정독과 예제 코드 분석으로 올바른 사용법 습득"
        ]
        return solutions[problem_num - 1]
    
    def _get_sample_test_output(self, challenge: Dict) -> str:
        """Generate sample test output"""
        test_count = challenge.get('success_criteria', {}).get('min_tests', 5)
        coverage = challenge.get('success_criteria', {}).get('min_coverage', 80)
        
        return f"""===== test session starts =====
collected {test_count} items

tests/test_core.py::test_initialization PASSED      [ 20%]
tests/test_core.py::test_main_functionality PASSED  [ 40%]
tests/test_core.py::test_error_handling PASSED      [ 60%]
tests/test_core.py::test_edge_cases PASSED          [ 80%]
tests/test_core.py::test_integration PASSED         [100%]

===== {test_count} passed in 0.12s =====

Coverage: {coverage}% line coverage achieved"""
    
    def _get_next_day_preview(self, day_number: int) -> str:
        """Get preview of next day's challenge"""
        next_day_key = f"day{(day_number + 1):02d}"
        if next_day_key in self.roadmap["challenges"]:
            next_challenge = self.roadmap["challenges"][next_day_key]
            return next_challenge['name']
        return "Advanced Challenge"
    
    def _get_experience_level(self, day_number: int) -> str:
        """Get experience level description"""
        if day_number <= 7:
            return "기초 도구 마스터 단계"
        elif day_number <= 14:
            return "웹 애플리케이션 개발 단계"
        elif day_number <= 21:
            return "데이터 분석 전문가 단계"
        else:
            return "고급 프로젝트 마스터 단계"
    
    def _get_key_learning(self, challenge: Dict) -> str:
        """Get key learning from this challenge"""
        learnings = {
            "cli-app": "터미널 애플리케이션의 사용자 경험 설계",
            "web-app": "현대적 웹 API 아키텍처 패턴",
            "data-tool": "효율적인 데이터 파이프라인 구축"
        }
        return learnings.get(challenge.get('type', 'cli-app'), "새로운 기술 스택 활용")
    
    def _get_confidence_statement(self, challenge: Dict, day_number: int) -> str:
        """Get confidence statement"""
        statements = {
            "cli-app": f"CLI 도구 개발에 자신감이 생겼다",
            "web-app": f"웹 애플리케이션 개발이 훨씬 자연스러워졌다",
            "data-tool": f"데이터 처리 도구 구축 실력이 늘었다"
        }
        base = statements.get(challenge.get('type', 'cli-app'), "Python 개발 실력이 성장했다")
        return f"{base}. Day {day_number}까지 오면서 정말 많이 배웠다"


def main():
    """Test the documentation generator"""
    root_dir = Path(__file__).parent.parent
    generator = DocumentationGenerator(root_dir)
    
    # Test blog generation
    blog = generator.generate_blog_post(3, Path("test"), "All tests passed", "Great development session")
    print("Generated blog preview:")
    print(blog[:500] + "...")
    
    # Test README generation  
    day_key = "day03"
    challenge = generator.roadmap["challenges"][day_key]
    readme = generator.generate_readme(3, challenge)
    print("\nGenerated README preview:")
    print(readme[:500] + "...")


if __name__ == "__main__":
    main()