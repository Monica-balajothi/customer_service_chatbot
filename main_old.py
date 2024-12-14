import os
from dotenv import load_dotenv
from tools.faq_tool import faq_lookup
from tools.tracking_tool import track_order
from tools.order_cancellation_tool import cancel_order
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def determine_intent(query):
    """Use GPT to determine the user's intent."""
    messages = [
        {"role": "system", "content": "You are an intent classifier. Classify the following query into one of the intents: 'faq', 'track_order', 'recommend_product', 'cancel_order', or 'unknown'."},
        {"role": "user", "content": f"Query: {query}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=50
    )
    return response['choices'][0]['message']['content'].strip().lower()


def main():
    print("Welcome to the Enhanced Customer Service Chatbot!")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        intent = determine_intent(query)

        if "faq" in intent:
            response = faq_lookup(query)
        elif "track_order" in intent:
            order_id = query.split()[-1]  # Extract order ID
            response = track_order(order_id)
        elif "cancel_order" in intent:
            order_id = query.split()[-1]  # Extract order ID from the query
            response = cancel_order(order_id)
        else:
            response = "Sorry, I didn't understand your query. Can you rephrase it?"

        print(f"Bot: {response}")

if __name__ == "__main__":
    main()