
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from tools.faq_tool import faq_lookup
from tools.tracking_tool import track_order
from tools.order_cancellation_tool import cancel_order
import openai
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def determine_intent(query):
    """Use GPT to determine the user's intent."""
    messages = [
        {"role": "system", "content": "You are an intent classifier. Classify the following query into one of the intents: 'faq', 'track_order', 'cancel_order', 'what can you do' or 'unknown'."},
        {"role": "user", "content": f"Query: {query}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=50
    )
    return response['choices'][0]['message']['content'].strip().lower()

@app.route("/")
def home():
    """Render the web UI."""
    return render_template("index.html")

CAPABILITIES = [
    "Answer FAQs about our services and policies.",
    "Help you track your orders.",
    "Recommend products based on your preferences.",
    "Assist with order cancellations."
]

@app.route("/chat", methods=["POST"])
def chat():
    """API endpoint to handle chatbot interactions."""
    data = request.get_json()
    query = " ".join(data.get("query", "").lower().split())  # Normalize spaces and case

    if not query:
        return jsonify({"error": "No query provided."}), 400
    # Handle "What can you do?" query directly
    elif "what can you do" in query:
        response = (
            "I can assist you with the following:\n"
            "- Answer FAQs about our services and policies.\n"
            "- Help you track your orders.\n"
            "- Recommend products based on your preferences.\n"
            "- Assist with order cancellations.\n"
            "Let me know how I can help!"
        )
    else:
        intent = determine_intent(query)

    if "faq" in intent:
        response = faq_lookup(query)
    elif "track_order" in intent:
        order_id = query.split()[-1]
        response = track_order(order_id)
    elif "cancel_order" in intent:
        order_id = query.split()[-1]  # Extract order ID from the query
        response = cancel_order(order_id)
    elif "what can you do" in intent:
        response = faq_lookup(query)
    else:
        response = "Sorry, I didn't understand your query. Can you rephrase it?"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
    