import openai
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def track_order(query: str) -> str:
    """
    Use ChatGPT to identify and process an order tracking request.
    """
    # Example mock data for tracking orders
    mock_data = {
        "12345": "Your order is in transit and will arrive on Dec 15th.",
        "67890": "Your order has been delivered.",
        "54321": "Your order is being prepared for shipment."
    }

    # Build the prompt
    prompt = (
        "You are an intelligent assistant. The user wants to track an order. Identify the order ID from the query "
        "and return only the order ID. If there is no valid order ID, respond with 'No valid order ID found.'\n\n"
        f"Query: {query}\n\n"
        "Provide only the order ID or 'No valid order ID found'."
    )

    try:
        # Call the ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-4 for better accuracy if needed
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )

        # Parse the response
        result = response['choices'][0]['message']['content'].strip()

        # Handle the result
        if "no valid order id found" in result.lower():
            return "Sorry, I couldn’t find a valid order ID in your query."
        else:
            # Lookup the order ID in the mock data
            order_id = result
            if order_id in mock_data:
                return mock_data[order_id]
            else:
                return f"Sorry, I couldn’t find any information for order ID {order_id}."

    except Exception as e:
        # Handle errors gracefully
        return f"An error occurred while processing your request: {str(e)}"
