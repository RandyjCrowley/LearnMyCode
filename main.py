import os
import json
import sys
from time import sleep
import asyncio
from ollama import Client
from dotenv import load_dotenv
import os

load_dotenv()







PATH_TO_LEARN = os.getenv("PATH_TO_LEARN")
IGNORE_LIST = [".git","vendor"]
JSON_FILENAME = "output.json"
MODEL_NAME = "llama3.1"


def read_file(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return format_string(content=f.read(), file_name=file_name)
    except UnicodeDecodeError:
        print(f"Error reading {file_name}: UnicodeDecodeError")
        return ''
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        return ''


def format_string(content, file_name):
    return f"=========\nFileName: {file_name}\nContent:\n{content}\n========="


def recursive_walk(path):
    new_files = []
    for root, _, files in os.walk(path):
        if not any(ignored in root for ignored in IGNORE_LIST):
            for file in files:
                file = os.path.join(root, file)
                new_files.append(file)
    return new_files


def get_initial_payload():
    if not os.path.exists(JSON_FILENAME):
        files = recursive_walk(PATH_TO_LEARN)
        payload = [{'role': 'user', 'content': read_file(file)} for file in files if read_file(file)]
        payload[:0] = [{'role': 'user', 'content': 'You will act as a Code Analyzer and understand that I can ask comments about my entire code base. You must respond to questions and statements related to my code and nothing else. Here is my code base:'}]
        with open(JSON_FILENAME, "w") as f:
            json.dump(payload, f)
    else:
        with open(JSON_FILENAME, "r") as f:
            payload = json.load(f)
    return payload


def save_payload(payload):
    with open(JSON_FILENAME, "w") as f:
        json.dump(payload, f)


async def initialize_ai(messages):
    response = ""
    Client.chat(model=MODEL_NAME, messages=messages)
    for part in :
        content = part['message']['content']
        response += content
        print(content, end='', flush=True)  # Print the content as it's received
    return response


async def main():
    payload = get_initial_payload()
    while True:
        user_input = input("Enter your message: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        # Append user input to payload with 'user' role
        payload.append({'role': 'user', 'content': user_input})

        # Prepare messages for the AI
        messages = [{'role': message['role'], 'content': message['content']} for message in payload]

        # Get AI response
        response = await initialize_ai(messages)

        # Append AI response to payload with 'assistant' role
        payload.append({'role': 'assistant', 'content': response})

        # Save updated payload
        save_payload(payload)

        # Print a newline after the complete response is printed
        print()

if __name__ == "__main__":
    asyncio.run(main())
