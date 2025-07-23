"""
뉴스 사이트 설정
"""

# 주요 뉴스 사이트 설정 (안전하고 공개적인 사이트들)
NEWS_SITES = [
    {
        'name': 'Hacker News',
        'url': 'https://news.ycombinator.com/',
        'selector': '.storylink, .titleline > a'
    },
    {
        'name': 'BBC News',
        'url': 'https://www.bbc.com/news',
        'selector': '[data-testid="card-headline"] h3, .gs-c-promo-heading__title'
    },
    {
        'name': 'Reuters',
        'url': 'https://www.reuters.com/',
        'selector': '[data-testid="Heading"] a, .story-title a'
    },
    {
        'name': 'CNN',
        'url': 'https://www.cnn.com/',
        'selector': '.container__headline a, h3.cd__headline a'
    }
]

# 기술 뉴스 사이트
TECH_NEWS_SITES = [
    {
        'name': 'Hacker News',
        'url': 'https://news.ycombinator.com/',
        'selector': '.storylink, .titleline > a'
    },
    {
        'name': 'TechCrunch',
        'url': 'https://techcrunch.com/',
        'selector': '.post-block__title__link'
    },
    {
        'name': 'The Verge',
        'url': 'https://www.theverge.com/',
        'selector': 'h2 a, h3 a'
    }
]

# 예제용 간단한 사이트 (테스트용)
DEMO_SITES = [
    {
        'name': 'Example News',
        'url': 'https://example.com',
        'selector': 'h1, h2, h3'
    }
]