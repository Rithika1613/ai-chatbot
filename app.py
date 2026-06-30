from flask import Flask, render_template, request, jsonify
from faq import faq_data
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

negative_words = [
    "angry",
    "bad",
    "worst",
    "frustrated",
    "upset",
    "hate",
    "issue",
    "problem",
    "complaint"
]

def search_faq(user_input):
    user_input = user_input.lower()

    for keyword, answer in faq_data.items():
        if keyword in user_input:
            return answer

    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    faq_answer = search_faq(user_message)

    # FAQ Response
    if faq_answer:

        with open("chat_log.txt", "a", encoding="utf-8") as file:
            file.write(f"Customer: {user_message}\n")
            file.write(f"Bot: {faq_answer}\n\n")

        return jsonify({"response": faq_answer})

    # Sentiment Analysis
    if any(word in user_message.lower() for word in negative_words):

        response = """
We are sorry for the inconvenience.

Your concern is important to us and our support team will work to resolve it as soon as possible.
"""

    else:

        response = """
Thank you for contacting customer support.

We have received your query and will assist you shortly.
"""

    # Chat Logging
    with open("chat_log.txt", "a", encoding="utf-8") as file:
        file.write(f"Customer: {user_message}\n")
        file.write(f"Bot: {response}\n\n")

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)