import json
from typing import List, Dict, Optional
from ollama import AsyncClient
import os

class AIChatbot:
    def __init__(self, model_name: str, json_filename: str):
        self.model_name = model_name
        self.json_filename = json_filename
        self.payload = self.load_or_initialize_payload()

    def load_or_initialize_payload(self) -> List[Dict[str, str]]:
        """
        Loads the payload from a JSON file or initializes it if the file does not exist.
        """
        try:
            if not os.path.exists(self.json_filename):
                return []
            with open(self.json_filename, "r") as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.json_filename}")
            return []
        except Exception as e:
            print(f"Unexpected error loading or initializing payload: {e}")
            return []

    def save_payload_to_file(self) -> None:
        """
        Saves the current payload to a JSON file.
        """
        try:
            with open(self.json_filename, "w") as json_file:
                json.dump(self.payload, json_file)
        except IOError as e:
            print(f"Error saving payload to {self.json_filename}: {e}")

    async def generate_ai_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """
        Generates a response from the AI model based on the provided messages.
        """
        response: str = ""
        try:
            async for part in await AsyncClient().chat(model=self.model_name, messages=messages, stream=True):
                content = part['message']['content']
                response += content
                print(content, end='', flush=True)
            return response
        except asyncio.CancelledError:
            print("Async operation was cancelled.")
            return None
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return None

    def add_message_to_payload(self, role: str, content: str) -> None:
        """
        Adds a new message to the payload.
        """
        self.payload.append({'role': role, 'content': content})
        self.save_payload_to_file()
