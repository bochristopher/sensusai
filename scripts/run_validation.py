# CLI script to run validation
from agent.validator_agent import suggest_next_tests

def main():
    test_data = {'camera': {'sharpness': 'low'}}
    result = suggest_next_tests(test_data)
    print(f"AI Agent Suggestion: {result}")

if __name__ == "__main__":
    main()
