import requests
import json
from requests.exceptions import ConnectionError
from pytgpt.phind import PHIND
from speech import text_to_speech  # Importing the text_to_speech function

# Initialize cache dictionary
response_cache = {}

# Function to check internet connectivity
def is_online():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except ConnectionError:
        return False

# Function to send request to Ollama API
def send_ollama_request(prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "openchat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    total_response = ""
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        for data in response.iter_lines():
            json_data = json.loads(data.decode())
            if "message" in json_data and json_data["message"]:
                total_response += json_data["message"]["content"]
            if json_data['done'] == True:
                break
        if total_response:
            return total_response
        return "Error: Empty response from OpenChat"
    except ConnectionError:
        return "Error: Connection error occurred while connecting to OpenChat"
    except Exception as e:
        return f"Error: {e}"


default_prompt = "You are an assistant running on PRETTY_NAME='Ubuntu 23.10'. Keep the answers brief and short unless asked by the user to explain more. Here's what the user asked {}"

# Initialize PHIND chatbot
bot = PHIND()

# Function to generate text response using PHIND
def generate_online_response(prompt):
    # Check if prompt is in cache
    if prompt in response_cache:
        return response_cache[prompt]
    else:
        response = bot.chat(prompt)
        response_cache[prompt] = response  # Cache the response
        return response

# Function to generate text response using ollama
def generate_offline_response(prompt):
    # Check if prompt is in cache
    if prompt in response_cache:
        return response_cache[prompt]
    else:
        response = send_ollama_request(prompt)
        response_cache[prompt] = response  # Cache the response
        return response

# Function to generate response based on online/offline status
def generate_text_response(prompt):
    if is_online():
        response = generate_online_response(prompt)
        text_to_speech(response)  # Convert the assistant's response to speech (online only)
        return response
    else:
        return generate_offline_response(prompt)

# Main function for interaction
def main():
    print("Welcome to Your Virtual Assistant!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        else:
            response = generate_text_response(default_prompt.format(user_input))
            print("Assistant:", response)


if __name__ == "__main__":
    main()
