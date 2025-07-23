# 🕷️ Day 2: 웹 스크래퍼로 60분 만에 뉴스 헤드라인 수집기 만들기

> **30일 uv Python 마스터 챌린지 - Day 2/30**  
> **테마**: 웹 스크래핑 & 데이터 분석

Day 1의 계산기에 이어 이번엔 실전에서 정말 유용한 웹 스크래퍼를 만들어봤다. requests + BeautifulSoup4 + pandas 조합으로 여러 뉴스 사이트에서 헤드라인을 자동 수집하고 CSV로 저장하는 CLI 도구를 60분 만에 완성했다.

---

## 🎯 오늘의 목표

**다중 사이트 뉴스 스크래퍼**를 만들어서 실제 웹 데이터를 수집하고 분석해보자.

### 사용한 핵심 도구들

- **requests**: HTTP 요청 처리
- **BeautifulSoup4**: HTML 파싱
- **pandas**: 데이터 분석 및 CSV 저장
- **lxml**: 빠른 XML/HTML 파싱
- **pytest**: 테스트 프레임워크

---

## ⏰ 개발 과정 (실제 60분 기록)

### **1단계: 프로젝트 셋업 (15분)**

Day 1에서 uv를 써봤으니 이번엔 더 빨랐다.

```bash
# 프로젝트 생성
mkdir day02-web-scraper
cd day02-web-scraper
uv init

# 스크래핑 관련 패키지 설치
uv add requests beautifulsoup4 pandas lxml
uv add --dev pytest pytest-cov black ruff

# 디렉토리 구조 생성
mkdir -p src/web_scraper tests
```

**개선점:** Day 1 경험으로 패키지 선택이 확실해졌다.

### **2단계: 핵심 스크래퍼 엔진 구현 (25분)**

#### **WebScraper 클래스 설계**

객체지향으로 설계해서 재사용성을 높였다.

```python
class WebScraper:
    def __init__(self, delay: float = 1.0, timeout: int = 10):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.delay = delay
        self.timeout = timeout
        self.scraped_data: List[Dict[str, Any]] = []
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """웹 페이지를 가져와서 BeautifulSoup 객체로 반환"""
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        time.sleep(self.delay)  # 예의 바른 스크래핑
        return soup
```

**핵심 아이디어:**
- Session 재사용으로 성능 향상
- User-Agent 설정으로 봇 차단 회피
- 지연 시간으로 서버 부하 최소화

#### **뉴스 사이트 설정**

각 사이트별 CSS 선택자를 설정 파일로 분리했다.

```python
NEWS_SITES = [
    {
        'name': 'Hacker News',
        'url': 'https://news.ycombinator.com/',
        'selector': '.storylink, .titleline > a'
    },
    {
        'name': 'BBC News',
        'url': 'https://www.bbc.com/news',
        'selector': '[data-testid="card-headline"] h3'
    }
]
```

#### **데이터 수집 로직**

```python
def scrape_news_headlines(self, news_sites: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    all_headlines = []
    
    for site in news_sites:
        try:
            soup = self.fetch_page(site['url'])
            headlines = soup.select(site['selector'])
            
            for headline in headlines[:10]:  # 상위 10개만
                text = headline.get_text(strip=True)
                if text:
                    link = headline.get('href', '')
                    # 상대 URL을 절대 URL로 변환
                    if link and not link.startswith('http'):
                        link = urljoin(site['url'], link)
                    
                    news_data = {
                        'title': text,
                        'link': link,
                        'source': site['name'],
                        'scraped_at': datetime.now().isoformat()
                    }
                    all_headlines.append(news_data)
        except ScraperError as e:
            self.logger.error(f"Error scraping {site['name']}: {e}")
            continue  # 한 사이트 실패해도 다른 사이트는 계속
    
    return all_headlines
```

**배운 점:** 에러가 나도 전체가 멈추지 않게 예외 처리가 중요하다.

### **3단계: CLI 인터페이스 구현 (10분)**

Day 1 경험을 살려 간단하면서도 강력한 CLI를 만들었다.

```python
def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "news":
        scrape_news()
    elif command == "interactive":
        interactive_mode()
    elif command == "help":
        print_help()
```

#### **대화형 모드 구현**

```python
def interactive_mode():
    print("🤖 Web Scraper Interactive Mode")
    scraper = WebScraper(delay=1.0)
    
    while True:
        command = input("\nscraper> ").strip().lower()
        
        if command == "news":
            headlines = scraper.scrape_news_headlines(NEWS_SITES[:2])
            print(f"Collected {len(headlines)} headlines")
        elif command == "summary":
            summary = scraper.get_data_summary()
            print(f"Total items: {summary['total_items']}")
        elif command == "quit":
            break
```

### **4단계: 테스트 작성 (10분)**

Day 1보다 더 체계적으로 테스트를 작성했다.

```python
@patch('src.web_scraper.scraper.requests.Session.get')
def test_fetch_page_success(self, mock_get, scraper, mock_html):
    """페이지 가져오기 성공 테스트"""
    mock_response = Mock()
    mock_response.content = mock_html.encode('utf-8')
    mock_get.return_value = mock_response
    
    soup = scraper.fetch_page("https://example.com")
    
    assert isinstance(soup, BeautifulSoup)
    assert soup.find('h1').get_text() == "Test Headline 1"
```

**테스트 결과:** 11개 테스트 모두 통과! ✅

---

## 🐛 만난 문제들과 해결 과정

### **문제 1: CSS 선택자가 사이트마다 다름**

**원인:** 각 뉴스 사이트마다 HTML 구조가 완전히 다름

**해결:** 설정 파일로 사이트별 선택자를 분리하고, 여러 선택자를 시도하는 방식으로 구현

```python
'selector': '.storylink, .titleline > a'  # 여러 선택자를 쉼표로 구분
```

### **문제 2: 상대 URL vs 절대 URL**

**원인:** 어떤 사이트는 `/article/123` 형태, 어떤 사이트는 `https://...` 형태

**해결:** `urljoin()`으로 자동 변환

```python
if link and not link.startswith('http'):
    link = urljoin(site['url'], link)
```

### **문제 3: 사이트 접근 차단**

**원인:** 일부 사이트에서 봇으로 인식해서 차단

**해결:** 
- User-Agent 헤더 설정
- 요청 간 지연 시간 추가
- Session 재사용으로 자연스러운 브라우징 시뮬레이션

### **문제 4: 테스트에서 실제 HTTP 요청**

**원인:** 테스트 중 실제 웹사이트에 요청을 보내면 느리고 불안정

**해결:** `unittest.mock.patch`로 HTTP 요청을 모킹

---

## 🎉 완성된 결과물

### **뉴스 스크래핑**

```bash
$ uv run python -m src.web_scraper news

🔍 Scraping major news sites...

✅ Found 15 headlines
1. [Hacker News] Show HN: I built a Python web scraper
2. [BBC News] Tech industry shows strong growth
3. [Reuters] Market updates and analysis

💾 Data saved to: news_headlines_20240123_140530.csv

📊 Summary:
  Hacker News: 8 articles
  BBC News: 3 articles
  Reuters: 2 articles
  CNN: 2 articles
```

### **대화형 모드**

```
🤖 Web Scraper Interactive Mode
Commands: news, tech, summary, clear, quit

scraper> news
Collected 10 headlines
scraper> summary
Total items: 10
  Hacker News: 6
  BBC News: 4
scraper> save
Data saved to: interactive_scrape_20240123_141205.csv
```

### **CSV 출력 예시**

| title | link | source | scraped_at |
|-------|------|--------|------------|
| Show HN: I built a web scraper | https://news.ycombinator.com/item?id=123 | Hacker News | 2024-01-23T14:05:30 |
| Tech industry shows growth | https://www.bbc.com/news/technology-123 | BBC News | 2024-01-23T14:05:32 |

---

## 💡 배운 점들

### **기술적 측면**

1. **웹 스크래핑의 현실**: 각 사이트마다 구조가 다르고 계속 변경됨
2. **예의 바른 스크래핑**: 지연 시간, User-Agent, robots.txt 준수
3. **데이터 정규화**: 다양한 소스의 데이터를 일관된 형태로 변환
4. **에러 처리의 중요성**: 네트워크 문제, 사이트 변경 등에 대비
5. **테스트 전략**: 외부 의존성을 모킹하는 방법

### **개발 프로세스 측면**

1. **설정 분리**: 코드와 데이터(선택자)를 분리해서 유지보수성 향상
2. **점진적 개발**: 기본 기능부터 시작해서 단계적으로 확장
3. **사용자 경험**: CLI 인터페이스에서 피드백과 진행상황 표시
4. **데이터 중심 사고**: 수집-처리-저장-분석의 파이프라인 구축

### **윤리적 측면**

1. **합법적 스크래핑**: 공개된 뉴스 사이트만 대상
2. **서버 부하 최소화**: 적절한 지연 시간과 요청 제한
3. **저작권 존중**: 헤드라인과 링크만 수집, 전체 내용은 수집하지 않음

---

## 🏗️ 프로젝트 구조

최종 완성된 프로젝트 구조:

```
day02-web-scraper/
├── src/
│   └── web_scraper/
│       ├── __init__.py
│       ├── __main__.py         # 패키지 진입점
│       ├── main.py             # CLI 인터페이스
│       ├── scraper.py          # 핵심 스크래퍼 엔진
│       └── news_sites.py       # 뉴스 사이트 설정
├── tests/
│   ├── __init__.py
│   └── test_scraper.py         # 포괄적 테스트 스위트
├── pyproject.toml              # uv 프로젝트 설정
├── uv.lock                     # 의존성 잠금 파일
├── README.md                   # 프로젝트 문서
└── BLOG.md                     # 이 파일
```

---

## 🔥 앞으로의 계획

### **Day 3 예고: 작업 관리 시스템**
- SQLite 데이터베이스 연동
- CRUD 기능이 있는 TODO 앱
- Rich 라이브러리로 예쁜 터미널 UI
- 데이터 백업/복원 기능

### **웹 스크래퍼 향후 개선 사항**
- [ ] 더 많은 뉴스 소스 추가
- [ ] 키워드 필터링 기능
- [ ] 스케줄링으로 자동 수집
- [ ] 데이터 시각화 (matplotlib)
- [ ] 웹 인터페이스 (Flask)

---

## 📊 성과 측정

### **개발 시간 단축**
- **Day 1**: 프로젝트 셋업 10분
- **Day 2**: 프로젝트 셋업 15분 (더 복잡한 의존성)
- **향상**: uv 사용법에 익숙해져 전체적으로 더 빨라짐

### **코드 품질 향상**
- **테스트 커버리지**: 11개 테스트로 핵심 기능 모두 커버
- **에러 처리**: 네트워크 오류, 파싱 오류 등 다양한 시나리오 대응
- **모듈화**: 기능별로 파일을 분리해 유지보수성 향상

### **실용성**
- **실제 데이터**: 가짜 데이터가 아닌 실제 뉴스 사이트에서 데이터 수집
- **유연성**: 새로운 사이트를 쉽게 추가할 수 있는 구조
- **확장성**: 뉴스 외에 다른 콘텐츠도 스크래핑 가능

---

## 🎯 마무리

**60분 만에 실용적인 웹 스크래퍼를 완성**했다는 게 뿌듯하다.

특히 Day 1의 계산기와 달리 이번엔 **실제 인터넷의 데이터를 다루는** 프로젝트라 더 흥미로웠다. 각 사이트마다 다른 HTML 구조를 파악하고, 안정적으로 데이터를 수집하는 과정에서 웹 개발의 현실적인 어려움을 체험할 수 있었다.

무엇보다 **"내가 만든 도구로 실제 데이터를 수집할 수 있다"**는 성취감이 크다. 이제 뉴스 헤드라인을 자동으로 모아서 트렌드를 분석하거나, 특정 키워드를 추적할 수도 있다.

**Day 2에서 이 정도 실력이라면, 30일 후에는 정말 어떤 웹 애플리케이션도 만들 수 있을 것 같다!** 🚀

---

## 📝 소스코드

전체 소스코드는 GitHub에 올려뒀다: [30-day-uv-python-challenge](https://github.com/Reasonofmoon/30-day-uv-python-challenge)

```bash
# 직접 실행해보고 싶다면
git clone https://github.com/Reasonofmoon/30-day-uv-python-challenge.git
cd 30-day-uv-python-challenge/day02-web-scraper
uv sync
uv run python -m src.web_scraper interactive
```

---

**다음 포스팅은 Day 3 - 작업 관리 시스템 개발기로 찾아뵙겠습니다!**

**함께 성장하는 개발자가 되어요! 💪**

---

*#Python #uv #WebScraping #BeautifulSoup4 #pandas #개발일기 #30일챌린지 #뉴스스크래퍼*

---

**Created by [Reasonofmoon](https://v0-neobrutalist-ui-design-sigma-seven.vercel.app/) | uv Python Developer Journey**