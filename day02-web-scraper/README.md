# =w Web Scraper CLI

> **Day 2 of 30-day Python mastery challenge**  
> Built with modern Python tools: uv + requests + BeautifulSoup4 + pandas

A powerful command-line web scraper for collecting news headlines and web content with data analysis and CSV export capabilities.

## ( Features

- **= Multi-site scraping**: Scrape multiple news sites simultaneously
- **=� News headlines**: Automatic collection from major news sources
- **=' Generic scraper**: Flexible content extraction with custom selectors
- **=� Data analysis**: Built-in pandas integration for data processing
- **=� Export functionality**: Save results to CSV with timestamps
- **� Interactive mode**: REPL-style scraper interface
- **>� Fully tested**: Comprehensive test coverage with pytest
- **� Lightning fast**: Built with uv package manager

## =� Quick Start

### Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Reasonofmoon/30-day-uv-python-challenge.git
cd 30-day-uv-python-challenge/day02-web-scraper

# Install dependencies
uv sync
```

### Usage

#### News Scraping Mode
```bash
# Scrape major news sites
uv run python -m src.web_scraper news

# Scrape tech news sites  
uv run python -m src.web_scraper tech
```

Example output:
```
= Scraping major news sites...

 Found 15 headlines
1. [Hacker News] Show HN: I built a Python web scraper
2. [BBC News] Tech industry shows strong growth
3. [Reuters] Market updates and analysis
4. [CNN] Breaking technology news
5. [Hacker News] Ask HN: Best practices for web scraping

=� Data saved to: news_headlines_20240123_140530.csv

=� Summary:
  Hacker News: 8 articles
  BBC News: 3 articles
  Reuters: 2 articles
  CNN: 2 articles
```

#### Interactive Mode
```bash
uv run python -m src.web_scraper interactive
```

```
> Web Scraper Interactive Mode
Commands: news, tech, summary, clear, quit

scraper> news
Collected 10 headlines
scraper> tech
Collected 8 tech headlines
scraper> summary
Total items: 18
  Hacker News: 12
  BBC News: 3
  Reuters: 2
  CNN: 1
scraper> save
Data saved to: interactive_scrape_20240123_141205.csv
scraper> quit
Goodbye!
```

## >� Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

## <� Project Structure

```
day02-web-scraper/
   src/
      web_scraper/
          __init__.py
          __main__.py         # Package entry point
          main.py             # CLI interface
          scraper.py          # Core scraper engine
          news_sites.py       # News site configurations
   tests/
      __init__.py
      test_scraper.py         # Comprehensive test suite
   pyproject.toml              # Project configuration
   uv.lock                     # Lock file for reproducible builds
   README.md                   # This file
```

## =� Technical Details

### Built With
- **[requests](https://requests.readthedocs.io/)**: HTTP library for web requests
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)**: HTML/XML parsing
- **[pandas](https://pandas.pydata.org/)**: Data analysis and CSV export
- **[lxml](https://lxml.de/)**: Fast XML and HTML parsing
- **[pytest](https://pytest.org/)**: Testing framework
- **[uv](https://github.com/astral-sh/uv)**: Next-generation Python package manager

### Key Components

#### `WebScraper` Class
- Multi-site content extraction with BeautifulSoup4
- Session management with proper headers
- Rate limiting and request timeout handling
- Data storage and history management
- Pandas integration for data analysis

#### News Site Support
- **Major News**: BBC, Reuters, CNN
- **Tech News**: Hacker News, TechCrunch, The Verge
- **Configurable**: Easy to add new sites via `news_sites.py`

#### CLI Interface
- Single command mode for quick scraping
- Interactive REPL mode for exploratory scraping
- Help system and data summary commands
- Automatic CSV export with timestamps

### Supported Features
- **Request handling**: Session reuse, timeout, error handling
- **Content parsing**: CSS selectors, link resolution, text extraction
- **Data export**: CSV format with UTF-8 encoding
- **Rate limiting**: Configurable delays between requests
- **Error handling**: Graceful failure with detailed logging

### Safety Features
- Respectful scraping with delays
- User-Agent headers to identify requests
- Timeout protection against hanging requests
- Exception handling for network issues
- Selective site targeting (public news sites only)

## =� Test Results

```bash
$ uv run pytest tests/ -v

===== test session starts =====
collected 11 items

tests/test_scraper.py::TestWebScraper::test_fetch_page_success PASSED        [  9%]
tests/test_scraper.py::TestWebScraper::test_fetch_page_request_error PASSED  [ 18%]
tests/test_scraper.py::TestWebScraper::test_scrape_news_headlines_success PASSED [ 27%]
tests/test_scraper.py::TestWebScraper::test_scrape_generic_content PASSED    [ 36%]
tests/test_scraper.py::TestWebScraper::test_save_to_csv_success PASSED       [ 45%]
tests/test_scraper.py::TestWebScraper::test_save_to_csv_no_data PASSED       [ 54%]
tests/test_scraper.py::TestWebScraper::test_get_data_summary_empty PASSED    [ 63%]
tests/test_scraper.py::TestWebScraper::test_get_data_summary_with_data PASSED [ 72%]
tests/test_scraper.py::TestWebScraper::test_clear_data PASSED                [ 81%]
tests/test_scraper.py::TestWebScraper::test_scrape_with_error_handling PASSED [ 90%]
tests/test_scraper.py::TestWebScraper::test_session_headers PASSED           [100%]

===== 11 passed in 1.28s =====
```

### Test Coverage
- **HTTP requests**: Success and error scenarios
- **HTML parsing**: BeautifulSoup4 integration
- **News scraping**: Multi-site headline collection
- **Data export**: CSV generation with pandas
- **Error handling**: Network failures and parsing errors
- **Data management**: Storage, summaries, and cleanup

## =� Development Journey

This project was completed as part of a 60-minute development challenge:

- **� 15 min**: Project setup with uv and dependencies
- **� 25 min**: Core scraper engine implementation
- **� 10 min**: CLI interface and interactive mode
- **� 10 min**: Test suite development

### Challenges Overcome
1. **Rate limiting**: Implemented respectful delays between requests
2. **Link resolution**: Proper handling of relative vs absolute URLs
3. **Error handling**: Graceful degradation when sites are unavailable
4. **Data structure**: Consistent format across different news sources
5. **CSV encoding**: UTF-8 support for international content

## <� Future Enhancements

- [ ] Add more news sources and categories
- [ ] Implement content filtering and keyword search
- [ ] Add data visualization with matplotlib
- [ ] Create scheduling system for automated scraping
- [ ] Implement database storage (SQLite/PostgreSQL)
- [ ] Add web interface with Flask/FastAPI
- [ ] Support for RSS feeds and APIs
- [ ] Advanced text analysis with NLP

## � Ethical Usage

This scraper is designed for educational purposes and should be used responsibly:

- **Respect robots.txt**: Always check site scraping policies
- **Rate limiting**: Don't overwhelm servers with requests
- **Attribution**: Give credit to original content sources
- **Terms of service**: Comply with website terms and conditions
- **Data usage**: Use scraped data ethically and legally

## > Contributing

This is a learning project, but contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## =� License

This project is open source and available under the [MIT License](LICENSE).

## < Acknowledgments

- Built as part of the **30-day Python mastery challenge**
- Inspired by modern web scraping best practices
- Thanks to the creators of requests, BeautifulSoup4, and pandas!

---

**P If you found this project helpful, please give it a star!**

---

**Created with d by [Reasonofmoon](https://github.com/Reasonofmoon)**  
**Part of the 30-day Python mastery challenge** =�