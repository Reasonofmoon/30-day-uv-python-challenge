"""
웹 스크래퍼 테스트
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

from src.web_scraper.scraper import WebScraper, ScraperError

class TestWebScraper:
    
    @pytest.fixture
    def scraper(self):
        """테스트용 스크래퍼 인스턴스"""
        return WebScraper(delay=0.1, timeout=5)
    
    @pytest.fixture
    def mock_html(self):
        """테스트용 HTML"""
        return """
        <html>
            <body>
                <h1><a href="/article1">Test Headline 1</a></h1>
                <h2><a href="/article2">Test Headline 2</a></h2>
                <div class="news-item">
                    <a href="/article3">Test Headline 3</a>
                </div>
            </body>
        </html>
        """
    
    @patch('src.web_scraper.scraper.requests.Session.get')
    def test_fetch_page_success(self, mock_get, scraper, mock_html):
        """페이지 가져오기 성공 테스트"""
        # Mock response
        mock_response = Mock()
        mock_response.content = mock_html.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test
        soup = scraper.fetch_page("https://example.com")
        
        # Assertions
        assert isinstance(soup, BeautifulSoup)
        assert soup.find('h1').get_text() == "Test Headline 1"
        mock_get.assert_called_once()
    
    @patch('src.web_scraper.scraper.requests.Session.get')
    def test_fetch_page_request_error(self, mock_get, scraper):
        """페이지 요청 실패 테스트"""
        mock_get.side_effect = Exception("Network error")
        
        with pytest.raises(ScraperError) as exc_info:
            scraper.fetch_page("https://example.com")
        
        assert "페이지 요청 실패" in str(exc_info.value)
    
    @patch('src.web_scraper.scraper.WebScraper.fetch_page')
    def test_scrape_news_headlines_success(self, mock_fetch, scraper, mock_html):
        """뉴스 헤드라인 스크래핑 성공 테스트"""
        # Mock BeautifulSoup
        soup = BeautifulSoup(mock_html, 'html.parser')
        mock_fetch.return_value = soup
        
        # Test data
        news_sites = [
            {
                'name': 'Test News',
                'url': 'https://test-news.com',
                'selector': 'h1 a, h2 a'
            }
        ]
        
        # Test
        headlines = scraper.scrape_news_headlines(news_sites)
        
        # Assertions
        assert len(headlines) == 2
        assert headlines[0]['title'] == "Test Headline 1"
        assert headlines[0]['source'] == "Test News"
        assert headlines[0]['link'] == "https://test-news.com/article1"
        assert 'scraped_at' in headlines[0]
    
    @patch('src.web_scraper.scraper.WebScraper.fetch_page')
    def test_scrape_generic_content(self, mock_fetch, scraper, mock_html):
        """일반 콘텐츠 스크래핑 테스트"""
        soup = BeautifulSoup(mock_html, 'html.parser')
        mock_fetch.return_value = soup
        
        selectors = {
            'title': 'h1 a, h2 a',
            'link': 'a'
        }
        
        results = scraper.scrape_generic_content("https://example.com", selectors)
        
        assert len(results) == 2
        assert results[0]['title'] == "Test Headline 1"
        assert 'scraped_at' in results[0]
    
    def test_save_to_csv_success(self, scraper, tmp_path):
        """CSV 저장 성공 테스트"""
        # Test data
        test_data = [
            {'title': 'Test 1', 'source': 'Site A', 'scraped_at': '2024-01-01T10:00:00'},
            {'title': 'Test 2', 'source': 'Site B', 'scraped_at': '2024-01-01T10:01:00'}
        ]
        scraper.scraped_data = test_data
        
        # Change to temp directory
        os.chdir(tmp_path)
        
        # Test
        filename = scraper.save_to_csv("test_output")
        
        # Assertions
        assert filename.startswith("test_output_")
        assert filename.endswith(".csv")
        assert os.path.exists(filename)
        
        # Verify CSV content
        df = pd.read_csv(filename)
        assert len(df) == 2
        assert list(df.columns) == ['title', 'source', 'scraped_at']
    
    def test_save_to_csv_no_data(self, scraper):
        """데이터 없을 때 CSV 저장 실패 테스트"""
        with pytest.raises(ScraperError) as exc_info:
            scraper.save_to_csv("test")
        
        assert "저장할 데이터가 없습니다" in str(exc_info.value)
    
    def test_get_data_summary_empty(self, scraper):
        """빈 데이터 요약 테스트"""
        summary = scraper.get_data_summary()
        
        assert summary['total_items'] == 0
        assert summary['sources'] == []
        assert summary['latest_scrape'] is None
    
    def test_get_data_summary_with_data(self, scraper):
        """데이터 있을 때 요약 테스트"""
        test_data = [
            {'title': 'Test 1', 'source': 'Site A', 'scraped_at': '2024-01-01T10:00:00'},
            {'title': 'Test 2', 'source': 'Site A', 'scraped_at': '2024-01-01T10:01:00'},
            {'title': 'Test 3', 'source': 'Site B', 'scraped_at': '2024-01-01T10:02:00'}
        ]
        scraper.scraped_data = test_data
        
        summary = scraper.get_data_summary()
        
        assert summary['total_items'] == 3
        assert summary['sources']['Site A'] == 2
        assert summary['sources']['Site B'] == 1
        assert summary['latest_scrape'] == '2024-01-01T10:02:00'
    
    def test_clear_data(self, scraper):
        """데이터 초기화 테스트"""
        scraper.scraped_data = [{'test': 'data'}]
        scraper.clear_data()
        
        assert len(scraper.scraped_data) == 0
    
    @patch('src.web_scraper.scraper.WebScraper.fetch_page')
    def test_scrape_with_error_handling(self, mock_fetch, scraper):
        """에러 처리 테스트"""
        mock_fetch.side_effect = ScraperError("Test error")
        
        news_sites = [
            {'name': 'Test Site', 'url': 'https://test.com', 'selector': 'h1'}
        ]
        
        # Should not raise exception, just log error
        headlines = scraper.scrape_news_headlines(news_sites)
        
        assert headlines == []
    
    def test_session_headers(self, scraper):
        """세션 헤더 설정 테스트"""
        assert 'User-Agent' in scraper.session.headers
        assert 'Mozilla' in scraper.session.headers['User-Agent']