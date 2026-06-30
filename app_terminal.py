from openai import OpenAI
from dotenv import load_dotenv
import os

from prompts import SYSTEM_PROMPT
from faq import faq_data

load_dotenv()

# Keeping this for future AI integration
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def search_faq(user_input):
    user_input = user_input.lower()

    for keyword, answer in faq_data.items():
        if keyword in user_input:
            return answer

    return None


print("Customer Support Chatbot")
print("Type 'exit' to quit\n")

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

while True:

    user_message = input("Customer: ")

    if user_message.lower() == "exit":
        print("Goodbye!")
        break

    faq_answer = search_faq(user_message)

    if faq_answer:
        print("\nBot:", faq_answer)
        continue

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Temporary response (no API needed)
    answer = """
Thank you for contacting customer support.

We have received your query and will help you resolve it.
Please provide additional details if needed.
"""

    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    print("\nBot:", answer)

    # Save chat log
    with open("chat_log.txt", "a", encoding="utf-8") as file:
        file.write(f"Customer: {user_message}\n")
        file.write(f"Bot: {answer}\n\n")