import json
import openai
from dotenv import load_dotenv
import os
import re
import logging

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename="faq_debug.log", filemode="w", format="%(asctime)s - %(message)s")

def faq_lookup(question: str) -> str:
    """
    Use ChatGPT to find the most relevant FAQ entry.
    """
    # Load FAQ data from file
    with open("data/faq.json", "r") as file:
        faq_data = json.load(file)

    # Build the prompt
    faq_list = "\n".join([f"{i+1}. {faq['question']}" for i, faq in enumerate(faq_data)])
    prompt = (
        f"You are an intelligent assistant. Match the user question to the most relevant FAQ question from the list below. "
        f"Respond with the number of the best match or 'No match found' if there is no good match.\n\nFAQs:\n{faq_list}\n\n"
        f"User Question: {question}\n\nProvide only the number of the most relevant FAQ or 'No match found'."
    )

    logging.debug(f"Generated FAQ Prompt: {prompt}")

    try:
        # Call the ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )

        # Parse the response
        result = response['choices'][0]['message']['content'].strip()
        logging.debug(f"ChatGPT Response: {result}")

        # Extract the FAQ number from the response
        match = re.search(r"^\d+", result)  # Extract leading number from the response
        if match:
            match_index = int(match.group()) - 1  # Convert match number to index
            if 0 <= match_index < len(faq_data):
                return faq_data[match_index]["answer"]
            else:
                return "Sorry, the match number is out of range."
        elif "no match found" in result.lower():
            return "Sorry, I couldn’t find an answer to that question."
        else:
            return f"Unexpected response format from ChatGPT: {result}"

    except Exception as e:
        # Log and return errors gracefully
        logging.error(f"Error during ChatGPT API call: {str(e)}")
        return f"An error occurred while processing your question: {str(e)}"
