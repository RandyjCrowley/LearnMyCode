import os
import asyncio
from ai_chatbot import AIChatbot
from utils import read_file_content, read_directory
from dotenv import load_dotenv

load_dotenv()

class CodeAnalyzer:
    def __init__(self, path_to_learn: str, model_name: str, json_filename: str):
        self.path_to_learn = path_to_learn
        self.ai_chatbot = AIChatbot(model_name=model_name, json_filename=json_filename)

    def initialize_payload(self) -> None:
        """
        Initializes the payload with the code base and initial instructions.
        """
        files = read_directory(self.path_to_learn)
        initial_payload = [{'role': 'user', 'content': read_file_content(file)} for file in files if read_file_content(file)]
        initial_instruction = {
            'role': 'user',
            'content': 'You will act as a Code Analyzer and understand that I can ask comments about my entire code base. You must respond to questions and statements related to my code and nothing else. Here is my code base:'
        }
        self.ai_chatbot.payload.insert(0, initial_instruction)
        self.ai_chatbot.payload.extend(initial_payload)
        self.ai_chatbot.save_payload_to_file()

    async def start_interaction(self) -> None:
        """
        Main loop for interacting with the AI model.
        """
        print("type 'exit' or 'quit' to leave")
        while True:
            try:
                user_input = input("Enter your message: ")
                if user_input.lower() in ['exit', 'quit']:
                    print("bye bye o/")
                    break

                # Append user input to the payload with 'user' role
                self.ai_chatbot.add_message_to_payload(role='user', content=user_input)

                # Prepare messages for the AI
                messages = [{'role': message['role'], 'content': message['content']} for message in self.ai_chatbot.payload]

                # Get AI response
                response = await self.ai_chatbot.generate_ai_response(messages)
                if response is None:
                    print("Failed to generate a response. Please try again.")
                    continue

                # Append AI response to the payload with 'assistant' role
                self.ai_chatbot.add_message_to_payload(role='assistant', content=response)

                # Print a newline after the complete response is printed
                print()

            except KeyboardInterrupt:
                print("\nOperation interrupted by user. Exiting...")
                break
            except Exception as e:
                print(f"Unexpected error in main loop: {e}")
                break

if __name__ == "__main__":
    PATH_TO_LEARN = os.getenv("PATH_TO_LEARN", "")
    MODEL_NAME = "llama3.1"
    JSON_FILENAME = "output.json"

    if PATH_TO_LEARN:
        code_analyzer = CodeAnalyzer(path_to_learn=PATH_TO_LEARN, model_name=MODEL_NAME, json_filename=JSON_FILENAME)

        # Initialize the payload if it hasn't been done yet
        if not os.path.exists(JSON_FILENAME):
            code_analyzer.initialize_payload()

        asyncio.run(code_analyzer.start_interaction())

    print("Please set your path to PATH_TO_LEARN in the .env :)")
