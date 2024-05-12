import requests
import json
import os
from requests.exceptions import ConnectionError
from pytgpt.phind import PHIND
from threading import Thread
from speech import text_to_speech  # Importing the text_to_speech function

# Define the path to the cache file
CACHE_FILE = "cache.json"

# Initialize cache dictionary
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as file:
        response_cache = json.load(file)
else:
    response_cache = {}

# Now response_cache contains either the loaded cache from cache.json or an empty dictionary


# Initialize conversation history list
history = []

# Function to check internet connectivity
def is_online():
    try:
        requests.get("https://www.google.com", timeout=10)
        return True
    except ConnectionError:
        return False

# Function to send request to Ollama
def send_ollama_request(prompt):
    url = "http://localhost:11434/api/chat"

    # Append the user prompt to the conversation history
    history.append({"role": "user", "content": prompt})

    payload = {
        "model": "openchat",
        "messages": history,
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
            # Append the assistant prompt to the conversation history
            history.append({"role": "assistant", "content": total_response})

            return total_response
        return "Error: Empty response from OpenChat"
    except ConnectionError:
        return "Error: Connection error occurred while connecting to OpenChat"
    except Exception as e:
        return f"Error: {e}"


default_prompt = "You are an assistant running on PRETTY_NAME='Ubuntu 23.10'. Keep the answers brief and short unless asked by the user to explain more. Here's what the user asked {}"

# Function to save the cache to cache.json
def save_cache():
    with open("cache.json", "w") as file:
        json.dump(response_cache, file)

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
        save_cache() # Save the cache
        return response

# Function to generate text response using OpenChat
def generate_offline_response(prompt):
    # Check if prompt is in cache
    if prompt in response_cache:
        return response_cache[prompt]
    else:
        response = send_ollama_request(prompt)
        
        # Append the assistant response to the conversation history
        history.append({"role": "assistant", "content": response})
        
        response_cache[prompt] = response  # Cache the response
        save_cache() # Save the cache
        return response

# Function to generate response based on online/offline status
def generate_text_response(prompt):
    if is_online():
        response = generate_online_response(prompt)
        Thread(target=text_to_speech, args=(response,)).start()
        return response
    else:
        response = generate_offline_response(prompt)
        Thread(target=text_to_speech, args=(response,)).start()
        return response

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
