# 🚀 30-Day uv Python Mastery Challenge

> **Building practical Python applications with modern tools**  
> Using the lightning-fast [uv](https://github.com/astral-sh/uv) package manager

A month-long journey to master Python development through hands-on projects, each built in 60 minutes or less.

## 🎯 Challenge Overview

**Goal**: Build 30 practical Python applications using modern development tools and best practices.

**Core Tools**:
- **[uv](https://github.com/astral-sh/uv)**: Next-generation Python package manager
- **pytest**: Testing framework
- **Modern libraries**: requests, pandas, FastAPI, SQLAlchemy, etc.

**Rules**:
- ⏰ Each project completed in ~60 minutes
- 🧪 Full test coverage with pytest
- 📚 Complete documentation for each project
- 🔄 Real-world, practical applications

---

## 📅 Progress Tracker

### Week 1: Foundation Tools
- ✅ **Day 1**: [Smart Calculator CLI](./day01-smart-calculator/) - Math operations with history
- ✅ **Day 2**: [Web Scraper CLI](./day02-web-scraper/) - News headline collector
- ⏳ **Day 3**: Task Manager with SQLite
- ⏳ **Day 4**: File Organizer CLI
- ⏳ **Day 5**: Password Generator & Manager
- ⏳ **Day 6**: Weather Dashboard CLI
- ⏳ **Day 7**: Week 1 Review & Integration

### Week 2: Web Applications
- ⏳ **Day 8**: FastAPI REST API
- ⏳ **Day 9**: Database Integration
- ⏳ **Day 10**: Authentication System
- ⏳ **Day 11**: File Upload Service
- ⏳ **Day 12**: Real-time Chat App
- ⏳ **Day 13**: API Testing Suite
- ⏳ **Day 14**: Week 2 Review

### Week 3: Data & Analysis
- ⏳ **Day 15**: Data Pipeline Builder
- ⏳ **Day 16**: Excel Report Generator
- ⏳ **Day 17**: Web Analytics Dashboard
- ⏳ **Day 18**: Email Automation
- ⏳ **Day 19**: PDF Report Generator
- ⏳ **Day 20**: Data Visualization Tool
- ⏳ **Day 21**: Week 3 Review

### Week 4: Advanced Projects
- ⏳ **Day 22**: Docker Deployment
- ⏳ **Day 23**: GitHub Actions CI/CD
- ⏳ **Day 24**: Monitoring & Logging
- ⏳ **Day 25**: Performance Testing
- ⏳ **Day 26**: Security Scanner
- ⏳ **Day 27**: Open Source Contribution
- ⏳ **Day 28-30**: Capstone Project

---

## 🛠️ Completed Projects

### 🧮 Day 1: Smart Calculator CLI
**Built**: Interactive calculator with history and math functions  
**Tech**: uv + pytest + argparse  
**Features**: REPL mode, history tracking, mathematical functions  
**Tests**: ✅ 5 tests passing  

```bash
cd day01-smart-calculator
uv run python src/smart_calculator/main.py interactive
```

[📖 Read Day 1 Blog](./day01-smart-calculator/BLOG.md) | [💻 View Code](./day01-smart-calculator/)

---

### 🕷️ Day 2: Web Scraper CLI
**Built**: Multi-site news headline scraper with data export  
**Tech**: uv + requests + BeautifulSoup4 + pandas  
**Features**: Multi-site scraping, CSV export, interactive mode  
**Tests**: ✅ 11 tests passing  

```bash
cd day02-web-scraper
uv run python -m src.web_scraper news
uv run python -m src.web_scraper interactive
```

[📖 Read Day 2 Blog](./day02-web-scraper/BLOG.md) | [💻 View Code](./day02-web-scraper/)

---

## 🚀 Quick Start

### Prerequisites
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Clone & Run Any Project
```bash
git clone https://github.com/Reasonofmoon/30-day-uv-python-challenge.git
cd 30-day-uv-python-challenge

# Day 1: Calculator
cd day01-smart-calculator && uv sync && uv run pytest tests/ -v

# Day 2: Web Scraper  
cd day02-web-scraper && uv sync && uv run pytest tests/ -v
```

---

## 📈 Key Metrics

- **Projects Completed**: 2/30
- **Total Test Coverage**: 16 tests passing
- **Lines of Code**: ~2,567 lines
- **Technologies Used**: 8+ libraries
- **Documentation**: 100% projects documented

---

## 🎓 Learning Outcomes

### Technical Skills Developed
- ✅ **uv Package Manager**: Project setup, dependency management
- ✅ **Testing**: pytest, mocking, test-driven development
- ✅ **CLI Development**: argparse, interactive modes, user experience
- ✅ **Web Scraping**: requests, BeautifulSoup4, ethical scraping
- ✅ **Data Processing**: pandas, CSV export, data analysis
- ✅ **Error Handling**: Exception management, graceful failures
- ✅ **Code Organization**: Module structure, separation of concerns

### Development Practices
- ✅ **TDD Approach**: Writing tests first
- ✅ **Documentation**: README, inline docs, usage examples
- ✅ **Git Workflow**: Proper commits, version control
- ✅ **Code Quality**: Clean, readable, maintainable code

---

## 🔧 Tech Stack

### Core Tools
- **[uv](https://github.com/astral-sh/uv)**: Package management & virtual environments
- **[pytest](https://pytest.org/)**: Testing framework
- **Python 3.8+**: Core language

### Libraries Used
- **requests**: HTTP client for web scraping
- **BeautifulSoup4**: HTML/XML parsing
- **pandas**: Data analysis and manipulation
- **lxml**: Fast XML and HTML parsing
- **rich**: Rich terminal UI (planned)
- **FastAPI**: Web framework (upcoming)
- **SQLAlchemy**: Database ORM (upcoming)

---

## 📚 Project Structure

Each project follows consistent structure:

```
dayXX-project-name/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       ├── core_module.py       # Main logic
│       └── utils.py            # Utilities
├── tests/
│   ├── __init__.py
│   └── test_*.py              # Test files
├── pyproject.toml             # uv configuration
├── uv.lock                    # Dependency lock file
├── README.md                  # Project documentation
├── BLOG.md                    # Development journey
└── .gitignore                # Git ignore rules
```

---

## 🎯 Next Steps

### Day 3 Preview: Task Manager CLI
- SQLite database integration
- CRUD operations for tasks
- Rich terminal UI with tables
- Priority and due date management
- Data export/import functionality

**Planned Features**:
- `task add "Learn Python" --priority high --due tomorrow`
- `task list --status pending --priority high`
- `task complete 5`
- Interactive dashboard with rich tables

---

## 🤝 Contributing

This is a learning challenge, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with improvements

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🌟 Acknowledgments

- **[uv team](https://github.com/astral-sh/uv)** for creating an amazing package manager
- **Python community** for excellent libraries and tools
- **Open source maintainers** whose tools make this possible

---

## 📬 Connect

- **GitHub**: [@Reasonofmoon](https://github.com/Reasonofmoon)
- **Blog**: Development journey and insights
- **Challenge**: Follow along with the 30-day progress

---

**⭐ If you find this challenge helpful, please give it a star!**

**💪 Join the challenge - fork this repository and start your own 30-day journey!**

---

*Last updated: Day 2 of 30 - Web Scraper CLI completed*