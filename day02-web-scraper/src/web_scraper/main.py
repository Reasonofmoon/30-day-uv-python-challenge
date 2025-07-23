"""
웹 스크래퍼 CLI 메인 진입점
"""
import sys
from .scraper import WebScraper, ScraperError
from .news_sites import NEWS_SITES, TECH_NEWS_SITES

def print_help():
    """도움말 출력"""
    print("Web Scraper CLI")
    print("Usage:")
    print("  python -m web_scraper news           - Scrape major news sites")
    print("  python -m web_scraper tech           - Scrape tech news sites")  
    print("  python -m web_scraper interactive    - Interactive mode")
    print("  python -m web_scraper help           - Show this help")

def scrape_news():
    """뉴스 스크래핑"""
    try:
        scraper = WebScraper(delay=2.0)  # 2초 지연
        print("🔍 Scraping major news sites...")
        
        headlines = scraper.scrape_news_headlines(NEWS_SITES)
        
        if headlines:
            print(f"\n✅ Found {len(headlines)} headlines")
            
            # 결과 출력
            for i, item in enumerate(headlines[:5], 1):
                print(f"{i}. [{item['source']}] {item['title']}")
            
            # CSV 저장
            filename = scraper.save_to_csv("news_headlines")
            print(f"\n💾 Data saved to: {filename}")
            
            # 요약 정보
            summary = scraper.get_data_summary()
            print(f"\n📊 Summary:")
            for source, count in summary['sources'].items():
                print(f"  {source}: {count} articles")
        else:
            print("❌ No headlines found")
            
    except ScraperError as e:
        print(f"❌ Error: {e}")

def scrape_tech():
    """기술 뉴스 스크래핑"""
    try:
        scraper = WebScraper(delay=2.0)
        print("🔍 Scraping tech news sites...")
        
        headlines = scraper.scrape_news_headlines(TECH_NEWS_SITES)
        
        if headlines:
            print(f"\n✅ Found {len(headlines)} tech headlines")
            
            for i, item in enumerate(headlines[:5], 1):
                print(f"{i}. [{item['source']}] {item['title']}")
            
            filename = scraper.save_to_csv("tech_news")
            print(f"\n💾 Data saved to: {filename}")
        else:
            print("❌ No headlines found")
            
    except ScraperError as e:
        print(f"❌ Error: {e}")

def interactive_mode():
    """대화형 모드"""
    print("🤖 Web Scraper Interactive Mode")
    print("Commands: news, tech, summary, clear, quit")
    
    scraper = WebScraper(delay=1.0)
    
    while True:
        try:
            command = input("\nscraper> ").strip().lower()
            
            if command == "quit":
                print("Goodbye!")
                break
            elif command == "help":
                print("Commands:")
                print("  news    - Scrape news headlines")
                print("  tech    - Scrape tech news")
                print("  summary - Show data summary")
                print("  clear   - Clear collected data")
                print("  quit    - Exit")
            elif command == "news":
                headlines = scraper.scrape_news_headlines(NEWS_SITES[:2])  # 처음 2개만
                print(f"Collected {len(headlines)} headlines")
            elif command == "tech":
                headlines = scraper.scrape_news_headlines(TECH_NEWS_SITES[:1])  # Hacker News만
                print(f"Collected {len(headlines)} tech headlines")
            elif command == "summary":
                summary = scraper.get_data_summary()
                print(f"Total items: {summary['total_items']}")
                for source, count in summary['sources'].items():
                    print(f"  {source}: {count}")
            elif command == "clear":
                scraper.clear_data()
                print("Data cleared")
            elif command == "save":
                if scraper.scraped_data:
                    filename = scraper.save_to_csv("interactive_scrape")
                    print(f"Data saved to: {filename}")
                else:
                    print("No data to save")
            else:
                print(f"Unknown command: {command}. Type 'help' for commands.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "news":
        scrape_news()
    elif command == "tech":
        scrape_tech()
    elif command == "interactive":
        interactive_mode()
    elif command == "help":
        print_help()
    else:
        print(f"Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    main()