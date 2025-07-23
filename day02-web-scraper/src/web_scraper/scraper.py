"""
웹 스크래퍼 엔진
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import time
import logging
from urllib.parse import urljoin, urlparse

class ScraperError(Exception):
    """스크래퍼 예외"""
    pass

class WebScraper:
    def __init__(self, delay: float = 1.0, timeout: int = 10):
        """
        웹 스크래퍼 초기화
        
        Args:
            delay: 요청 간 지연 시간 (초)
            timeout: 요청 타임아웃 (초)
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.delay = delay
        self.timeout = timeout
        self.scraped_data: List[Dict[str, Any]] = []
        
        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """
        웹 페이지를 가져와서 BeautifulSoup 객체로 반환
        
        Args:
            url: 스크래핑할 URL
            
        Returns:
            BeautifulSoup 객체
        """
        try:
            self.logger.info(f"Fetching: {url}")
            
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 요청 간 지연
            time.sleep(self.delay)
            
            return soup
            
        except requests.exceptions.RequestException as e:
            raise ScraperError(f"페이지 요청 실패: {url} - {str(e)}")
        except Exception as e:
            if "Network error" in str(e):
                raise ScraperError(f"페이지 요청 실패: {url} - {str(e)}")
            raise ScraperError(f"페이지 파싱 실패: {url} - {str(e)}")
    
    def scrape_news_headlines(self, news_sites: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        뉴스 사이트에서 헤드라인 수집
        
        Args:
            news_sites: [{'name': '사이트명', 'url': 'URL', 'selector': 'CSS선택자'}] 형태의 리스트
            
        Returns:
            수집된 뉴스 데이터 리스트
        """
        all_headlines = []
        
        for site in news_sites:
            try:
                self.logger.info(f"Scraping {site['name']}...")
                
                soup = self.fetch_page(site['url'])
                headlines = soup.select(site['selector'])
                
                for headline in headlines[:10]:  # 상위 10개만
                    text = headline.get_text(strip=True)
                    if text:
                        link = headline.get('href', '')
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
                continue
        
        self.scraped_data.extend(all_headlines)
        return all_headlines
    
    def scrape_generic_content(self, url: str, selectors: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        일반적인 콘텐츠 스크래핑
        
        Args:
            url: 스크래핑할 URL
            selectors: {'field_name': 'CSS선택자'} 형태의 딕셔너리
            
        Returns:
            스크래핑된 데이터 리스트
        """
        try:
            soup = self.fetch_page(url)
            results = []
            
            # 각 선택자로 요소 찾기
            first_selector = list(selectors.keys())[0]
            main_elements = soup.select(selectors[first_selector])
            
            for element in main_elements:
                data = {'scraped_at': datetime.now().isoformat()}
                
                for field, selector in selectors.items():
                    if field == first_selector:
                        data[field] = element.get_text(strip=True)
                    else:
                        # 현재 요소 내에서 찾기
                        sub_element = element.select_one(selector)
                        if sub_element:
                            if selector.endswith('[href]') or selector.endswith('[src]'):
                                data[field] = sub_element.get('href') or sub_element.get('src')
                            else:
                                data[field] = sub_element.get_text(strip=True)
                        else:
                            data[field] = None
                
                results.append(data)
            
            self.scraped_data.extend(results)
            return results
            
        except ScraperError as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return []
    
    def save_to_csv(self, filename: str, data: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        데이터를 CSV 파일로 저장
        
        Args:
            filename: 파일명
            data: 저장할 데이터 (None이면 전체 scraped_data 사용)
            
        Returns:
            저장된 파일 경로
        """
        if data is None:
            data = self.scraped_data
        
        if not data:
            raise ScraperError("저장할 데이터가 없습니다")
        
        try:
            df = pd.DataFrame(data)
            filepath = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            self.logger.info(f"Data saved to {filepath}")
            return filepath
            
        except Exception as e:
            raise ScraperError(f"CSV 저장 실패: {str(e)}")
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        수집된 데이터 요약 정보
        
        Returns:
            요약 정보 딕셔너리
        """
        if not self.scraped_data:
            return {"total_items": 0, "sources": [], "latest_scrape": None}
        
        df = pd.DataFrame(self.scraped_data)
        
        summary = {
            "total_items": len(self.scraped_data),
            "sources": df.get('source', pd.Series()).value_counts().to_dict() if 'source' in df.columns else {},
            "latest_scrape": max([item.get('scraped_at', '') for item in self.scraped_data]),
            "columns": list(df.columns)
        }
        
        return summary
    
    def clear_data(self):
        """수집된 데이터 초기화"""
        self.scraped_data.clear()
        self.logger.info("Data cleared")