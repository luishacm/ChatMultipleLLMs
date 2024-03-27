# Local LLM Multiple Chats

## Description

Local LLM Multiple Chats is an inference interface for Language Models (LLMs) that allows you to simultaneously converse with four different models using the same prompt. It provides a user-friendly interface for interacting with powerful language models and comparing their responses side by side.

## Features

- Simultaneously chat with multiple language models
- Support for OpenAI's GPT-3.5 Turbo and GPT-4 models
- Integration with Anthropic's Claude 3 Sonnet and Claude 3 Haiku models
- Customizable system prompts for each model
- Real-time token count tracking and adjustable token limit
- Clear and intuitive user interface

## Upcoming Features

- Integration with Bedrock's Opus model once it becomes available on AWS


## Getting Started

### Prerequisites

To run the Local LLM Multiple Chats application, you need to have the following:

- Python 3.x installed
- PyQt5 library
- OpenAI API key
- Bedrock Access Key
- Bedrock Secret Key
- Bedrock Region Name

### Installation

1. Clone the repository:

```git clone https://github.com/luishacm/local-llm-multiple-chats.git```

2. Install the required dependencies:

```pip install -r requirements.txt```

3. Create a `.env` file in the project root directory and add the following variables:

```
OPENAI_API_KEY=your-openai-api-key
BEDROCK_ACCESS_KEY=your-bedrock-access-key
BEDROCK_SECRET_KEY=your-bedrock-secret-key
BEDROCK_REGION_NAME=your-bedrock-region-name
```

Replace `your-openai-api-key`, `your-bedrock-access-key`, `your-bedrock-secret-key`, and `your-bedrock-region-name` with your actual API keys and region name.

### Usage

1. Run the application:

```python app.py```

2. The application window will open, presenting you with the chat interface.

3. Select the desired language models you want to converse with by checking the corresponding checkboxes.

4. Enter your system prompt (optional) in the designated input field.

5. Type your message in the user input area and click the "Send" button or press Enter to send the message.

6. The selected models will generate responses, which will be displayed in the chat area.

7. Continue the conversation by entering new messages and observing the models' responses.

8. You can adjust the token limit using the provided input field to control the maximum number of tokens allowed in the conversation history.

9. To clear the conversation history, click the "Clear Conversation" button.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request. Make sure to follow the project's code of conduct.

## License

This project is licensed under the [MIT License](license).

## Source

- [OpenAI](https://openai.com): GPT-3.5 Turbo and GPT-4 models.
- [Anthropic](https://www.anthropic.com): Claude 3 Sonnet and Claude 3 Haiku models.
- [PyQt5](https://pypi.org/project/PyQt5/): User interface framework.

## Contact

For any questions or inquiries, please contact [luishacmartins@gmail.com](mailto:luishacmartins@gmail.com).
