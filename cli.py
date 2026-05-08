import os
from dotenv import load_dotenv
from agent.agent import ask

load_dotenv()

def main():
    print("\n" + "="*50)
    print("🤖 GitHub AI Agent — powered by Gemini + MCP")
    print("="*50)
    print("Ask me anything about your GitHub!")
    print("Examples:")
    print("  → What repos do I have?")
    print("  → Show open issues in <repo-name>")
    print("  → Summarize my profile")
    print("  → List PRs in <repo-name>")
    print("\nType 'exit' or 'quit' to stop.")
    print("="*50 + "\n")

    chat_history = []

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nAgent: Bye bro! Happy coding! 👋")
                break

            print("\nAgent: thinking...\n")
            response = ask(user_input, chat_history)
            print(f"Agent: {response}\n")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\n\nAgent: Bye bro! Happy coding! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()