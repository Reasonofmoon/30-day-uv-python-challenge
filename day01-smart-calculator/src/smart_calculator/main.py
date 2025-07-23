"""
Smart Calculator Main Entry Point
"""
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.smart_calculator.calculator import SmartCalculator, CalculatorError

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Smart Calculator")
        print("Usage:")
        print("  python main.py calculate '2 + 3'")
        print("  python main.py interactive")
        return
    
    command = sys.argv[1]
    calc = SmartCalculator()
    
    if command == "calculate" and len(sys.argv) >= 3:
        expression = sys.argv[2]
        try:
            result = calc.evaluate(expression)
            print(f"Result: {expression} = {result}")
        except CalculatorError as e:
            print(f"Error: {e}")
    
    elif command == "interactive":
        print("Interactive Calculator Mode")
        print("Type 'quit' to exit.")
        print("")
        
        while True:
            try:
                user_input = input("calc> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'history':
                    history = calc.get_history()
                    if history:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"  {i}. {entry['expression']} = {entry['result']}")
                        print("")
                    else:
                        print("No calculation history.")
                    continue
                
                if user_input.lower() == 'clear':
                    calc.clear_history()
                    print("History cleared.")
                    continue
                
                if user_input.lower() == 'help':
                    print("""
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
""")
                    continue
                
                result = calc.evaluate(user_input)
                print(f"= {result}")
                
            except CalculatorError as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
    
    else:
        print("Unknown command.")
        print("Available commands: calculate, interactive")

if __name__ == "__main__":
    main()