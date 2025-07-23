# 🧮 Smart Calculator CLI

> **Day 1 of 30-day Python mastery challenge**  
> Built with modern Python tools: uv + pytest

A feature-rich command-line calculator with history tracking, interactive mode, and comprehensive testing.

## ✨ Features

- **🔢 Advanced calculations**: Basic arithmetic + square root, pi, e constants
- **📊 History management**: Track and review calculation history
- **⚡ Interactive mode**: REPL-style calculator experience
- **🧪 Fully tested**: Complete test coverage with pytest
- **⚡ Lightning fast**: Built with uv package manager

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Reasonofmoon/30-day-uv-python-challenge.git
cd 30-day-uv-python-challenge/day01-smart-calculator

# Install dependencies
uv sync
```

### Usage

#### Single Calculation Mode
```bash
# Basic arithmetic
uv run python src/smart_calculator/main.py calculate "2 + 3 * 4"
# Output: Result: 2 + 3 * 4 = 14

# Square root
uv run python src/smart_calculator/main.py calculate "sqrt(16)"
# Output: Result: sqrt(16) = 4.0

# Using constants
uv run python src/smart_calculator/main.py calculate "pi * 2"
# Output: Result: pi * 2 = 6.283185307179586
```

#### Interactive Mode
```bash
uv run python src/smart_calculator/main.py interactive
```

```
Interactive Calculator Mode
Type 'quit' to exit.

calc> 2 + 3 * 4
= 14
calc> sqrt(25)
= 5.0
calc> history
Calculation History:
  1. 2 + 3 * 4 = 14
  2. sqrt(25) = 5.0
calc> help
Smart Calculator Help
────────────────────────
Basic operations: +, -, *, /, **
Functions: sqrt(x)
Constants: pi, e
Commands:
  history - Show calculation history
  clear   - Clear history  
  help    - Show help
  quit    - Exit
calc> quit
Goodbye!
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

## 🏗️ Project Structure

```
day01-smart-calculator/
├── src/
│   └── smart_calculator/
│       ├── __init__.py
│       ├── main.py          # CLI entry point
│       ├── calculator.py    # Core calculation engine
│       └── cli.py          # Additional CLI utilities
├── tests/
│   ├── __init__.py
│   └── test_calculator.py  # Comprehensive test suite
├── pyproject.toml          # Project configuration
├── uv.lock                # Lock file for reproducible builds
├── BLOG.md                # Development blog post
└── README.md               # This file
```

## 💻 Technical Details

### Built With
- **[uv](https://github.com/astral-sh/uv)**: Next-generation Python package manager
- **[pytest](https://pytest.org/)**: Testing framework
- **Python 3.8+**: Core language features

### Key Components

#### `SmartCalculator` Class
- Expression evaluation with safety checks
- History management with timestamps
- Support for mathematical functions and constants
- Comprehensive error handling

#### CLI Interface
- Single command mode for quick calculations  
- Interactive REPL mode for extended sessions
- Help system and history commands
- Graceful error handling with user-friendly messages

### Supported Operations
- **Basic arithmetic**: `+`, `-`, `*`, `/`, `**` (exponentiation)
- **Mathematical functions**: `sqrt(x)`
- **Constants**: `pi`, `e`
- **Parentheses**: For operation precedence

### Safety Features
- Input validation with regex patterns
- Safe expression evaluation
- Division by zero protection
- Comprehensive error messages

## 📈 Test Results

```bash
$ uv run pytest tests/ -v

===== test session starts =====
collected 5 items

tests/test_calculator.py::test_basic_arithmetic PASSED      [ 20%]
tests/test_calculator.py::test_complex_expressions PASSED   [ 40%]  
tests/test_calculator.py::test_functions PASSED             [ 60%]
tests/test_calculator.py::test_history PASSED               [ 80%]
tests/test_calculator.py::test_error_handling PASSED        [100%]

===== 5 passed in 0.05s =====
```

### Test Coverage
- **Basic arithmetic**: Addition, subtraction, multiplication, division
- **Complex expressions**: Parentheses, operator precedence
- **Mathematical functions**: Square root, constants (pi, e)  
- **History management**: Storage, retrieval, timestamps
- **Error handling**: Division by zero, invalid expressions

## 📊 Development Journey

This project was completed in **60 minutes** as part of a 30-day Python mastery challenge:

- **⏰ 10 min**: Project setup with uv
- **⏰ 30 min**: Core functionality implementation  
- **⏰ 15 min**: Test suite development
- **⏰ 5 min**: CLI integration and debugging

### Challenges Overcome
1. **Unicode/Emoji encoding**: Fixed Windows terminal compatibility
2. **Regex validation**: Resolved function name validation in expressions
3. **Import path issues**: Fixed relative import problems
4. **CLI output**: Debugged silent execution issues

## 🎯 Future Enhancements

- [ ] Add more mathematical functions (sin, cos, tan, log)
- [ ] Implement variable storage and recall
- [ ] Add expression parsing for complex nested functions
- [ ] Create configuration file for custom settings
- [ ] Add expression history export/import
- [ ] Implement plugin system for custom functions

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
- Inspired by modern Python development practices
- Thanks to the creators of uv and pytest for amazing tools!

---

**⭐ If you found this project helpful, please give it a star!**

**📝 Read the full development story**: [BLOG.md - Building a Smart Calculator with uv](./BLOG.md)

---

**Created with ❤️ by [Reasonofmoon](https://github.com/Reasonofmoon)**  
**Part of the 30-day Python mastery challenge** 🚀