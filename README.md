**Code Analyzer with AI Chatbot**
=====================================

**Table of Contents**

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuring the AI Model](#configuring-the-ai-model)
6. [Contributing](#contributing)

## Overview
--------

This project combines a code analyzer with an AI chatbot to provide an interactive way of analyzing and understanding codebases. The code analyzer uses recursion to collect all files within a specified directory, excluding those in the IGNORE_LIST, while the AI chatbot uses the LLaMA model to generate responses based on user input.

## Requirements
------------

* Python 3.x
* `ollama` library for interacting with the LLaMA model (`pip install ollama`)
* `dotenv` library for loading environment variables (`pip install python-dotenv`)
* `json` library for working with JSON files (comes bundled with Python)

## Installation
--------------

To run this project, you'll need to install the required libraries. Run the following commands in your terminal:

```bash
git clone https://github.com/RandyjCrowley/LearnMyCode.git
cd LearnMyCode
pip install -r requirements.txt
```

## Usage
----

### Initializing the Payload

Before starting the interactive session, the payload must be initialized by calling the `initialize_payload()` method in `main.py`. This will create a JSON file containing an empty payload.

### Starting the Interactive Session

To start the interactive session, run the script using Python:

```python main.py```

This will prompt you to enter your message. You can ask questions about the codebase, and the AI chatbot will respond accordingly. To exit the session, type `exit` or `quit`.

## Configuring the AI Model
-------------------------

To use a different AI model, update the `MODEL_NAME` variable in `main.py`. Currently, it's set to "llama3.1".

## Contributing
------------

Feel free to contribute by submitting pull requests or issues. Please make sure to follow the standard Python coding style (PEP 8) and include relevant tests for your code changes.
