import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox, QSpinBox, QFrame
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import openai
import boto3
import json
import tiktoken
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
BEDROCK_ACCESS_KEY = os.environ.get("BEDROCK_ACCESS_KEY")
BEDROCK_SECRET_KEY = os.environ.get("BEDROCK_SECRET_KEY")
BEDROCK_REGION_NAME = os.environ.get("BEDROCK_REGION_NAME")

openai.api_key = OPENAI_API_KEY

class ChatbotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.conversation_history = {}
        self.selected_models = []
        self.system_prompt = ""

        self.model_info = {
            "gpt-3.5-turbo": {
                "display_name": "GPT-3.5 Turbo",
                "full_name": "gpt-3.5-turbo",
                "provider": "openai"
            },
            "gpt-4": {
                "display_name": "GPT-4",
                "full_name": "gpt-4-turbo",
                "provider": "openai"
            },
            "gpt-4o": {
                "display_name": "GPT-4-Omni",
                "full_name": "gpt-4-o",
                "provider": "openai"
            },
            "sonnet": {
                "display_name": "Sonnet",
                "full_name": "anthropic.claude-3-sonnet-20240229-v1:0",
                "provider": "anthropic"
            },
            "haiku": {
                "display_name": "Haiku",
                "full_name": "anthropic.claude-3-haiku-20240307-v1:0",
                "provider": "anthropic"
            },
            "opus": {
                "display_name": "Opus",
                "full_name": "anthropic.claude-3-opus-20240229-v1:0",
                "provider": "anthropic"
            }
            # Add more models as needed
        }

        # Main Window Setup
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #F5F5F5; border-radius: 10px;")

        # Layouts
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        # Fonts
        title_font = QFont("Garamond", 16)
        label_font = QFont("Garamond", 12)
        input_font = QFont("Garamond", 11)

        # System Prompt
        system_prompt_label = QLabel("System Prompt:")
        system_prompt_label.setFont(title_font)
        self.system_prompt_entry = QLineEdit()
        self.system_prompt_entry.setFont(input_font)
        self.system_prompt_entry.setPlaceholderText("Enter system prompt here...")
        self.system_prompt_entry.setStyleSheet("border-radius: 5px; padding: 5px;")

        # Chat Area
        self.chat_area = QTextEdit()
        self.chat_area.setFont(label_font)
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("border-radius: 5px; padding: 10px;")
        self.chat_area.setAutoFillBackground(True)
        palette = self.chat_area.palette()
        palette.setColor(QPalette.Base, QColor(240, 240, 240))  # Light gray background color
        self.chat_area.setPalette(palette)

        # User Input
        self.user_input = QTextEdit()
        self.user_input.setFont(input_font)
        self.user_input.setPlaceholderText("Type your message here...")
        self.user_input.setFixedHeight(100)
        self.user_input.setStyleSheet("border-radius: 5px; padding: 10px; border: 1px solid #CCCCCC;")

        # Buttons
        send_button = QPushButton("Send")
        send_button.setFont(label_font)
        send_button.clicked.connect(self.send_message)
        send_button.setStyleSheet("QPushButton { background-color: #B0E0E6; color: #333333; border-radius: 5px; padding: 8px; }"
                                  "QPushButton:hover { background-color: #ADD8E6; }"
                                  "QPushButton:pressed { background-color: #87CEFA; }")
        clear_button = QPushButton("Clear Conversation")
        clear_button.setFont(label_font)
        clear_button.clicked.connect(self.clear_conversation)
        clear_button.setStyleSheet("QPushButton { background-color: #FFE4E1; color: #333333; border-radius: 5px; padding: 8px; }"
                                   "QPushButton:hover { background-color: #FFC0CB; }"
                                   "QPushButton:pressed { background-color: #FFB6C1; }")

        # Token Count and Limit
        token_layout = QHBoxLayout()
        self.token_label = QLabel("Token Count: 0")
        self.token_label.setFont(label_font)
        token_limit_label = QLabel("Token Limit:")
        token_limit_label.setFont(label_font)
        self.token_limit_entry = QSpinBox()
        self.token_limit_entry.setFont(input_font)
        self.token_limit_entry.setRange(1, 10000)
        self.token_limit_entry.setValue(4096)
        self.token_limit_entry.setStyleSheet("border-radius: 5px; padding: 5px;")
        token_layout.addWidget(self.token_label)
        token_layout.addWidget(token_limit_label)
        token_layout.addWidget(self.token_limit_entry)
        token_layout.addStretch()

        # Model Selection
        model_layout = QHBoxLayout()
        model_label = QLabel("Model Selection:")
        model_label.setFont(title_font)
        model_layout.addWidget(model_label)
        self.model_checkboxes = {}
        for model_key in self.model_info:
            model_checkbox = QCheckBox(self.model_info[model_key]["display_name"])
            model_checkbox.setFont(label_font)
            model_checkbox.stateChanged.connect(lambda state, model=model_key: self.update_selected_models(model, state))
            model_layout.addWidget(model_checkbox)
            self.model_checkboxes[model_key] = model_checkbox
        model_layout.addStretch()

        # Add Widgets to Layouts
        top_layout.addWidget(system_prompt_label)
        top_layout.addWidget(self.system_prompt_entry)
        top_layout.addStretch()

        bottom_layout.addWidget(send_button)
        bottom_layout.addWidget(clear_button)
        bottom_layout.addLayout(token_layout)
        bottom_layout.addLayout(model_layout)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.chat_area)
        main_layout.addWidget(self.user_input)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def send_message(self):
        user_message = self.user_input.toPlainText().strip()
        self.user_input.clear()

        for model in self.selected_models:
            if model not in self.conversation_history:
                self.conversation_history[model] = []

            self.conversation_history[model].append({"role": "user", "content": user_message})

        self.chat_area.setTextColor(QColor(0, 0, 0))  # Set text color to black
        self.chat_area.append(f"\nYou: {user_message}\n")
        self.chat_area.ensureCursorVisible()

        self.get_responses()

    def get_responses(self):
        for model in self.selected_models:
            if self.model_info[model]["provider"] == "anthropic":
                self.get_anthropic_response(model)
            else:
                self.get_chatbot_response(model)

    def update_selected_models(self, model, state):
        if state == Qt.Checked:
            self.selected_models.append(model)
        else:
            self.selected_models.remove(model)

    def get_chatbot_response(self, model):
        token_limit = self.token_limit_entry.value()
        self.limit_conversation_history(model, token_limit)

        system_prompt = self.system_prompt_entry.text()
        messages = [{"role": "system", "content": system_prompt}] + self.conversation_history[model] if system_prompt else self.conversation_history[model]

        response = openai.ChatCompletion.create(
            model=self.model_info[model]["full_name"],
            messages=messages,
            stream=True,
            max_tokens=token_limit,
        )

        assistant_response = ""
        self.chat_area.setTextColor(QColor(50, 50, 50))  # Set text color to dark gray
        self.chat_area.append(f"\n{self.model_info[model]['display_name']}: ")
        QApplication.processEvents()

        for chunk in response:
            if 'content' in chunk['choices'][0]['delta']:
                content = chunk['choices'][0]['delta']['content']
                assistant_response += content
                self.chat_area.insertPlainText(content)
                self.chat_area.ensureCursorVisible()
                QApplication.processEvents()

        self.conversation_history[model].append({"role": "assistant", "content": assistant_response})
        self.chat_area.append("\n")
        self.update_token_count()

    def get_anthropic_response(self, model):
        session = boto3.Session(
            aws_access_key_id=BEDROCK_ACCESS_KEY,
            aws_secret_access_key=BEDROCK_SECRET_KEY,
            region_name=BEDROCK_REGION_NAME
        )

        bedrock = session.client(service_name="bedrock-runtime")

        token_limit = self.token_limit_entry.value()
        self.limit_conversation_history(model, token_limit)
        messages = self.conversation_history[model]

        body = {
            "messages": messages,
            "max_tokens": token_limit,
            "anthropic_version": "bedrock-2023-05-31"
        }

        try:
            response = bedrock.invoke_model_with_response_stream(
                body=json.dumps(body),
                modelId=self.model_info[model]["full_name"],
            )

            self.chat_area.setTextColor(QColor(50, 50, 50))  # Set text color to dark gray
            self.chat_area.append(f"\n{self.model_info[model]['display_name']}: ")
            QApplication.processEvents()

            assistant_response = ""
            for event in response.get("body"):
                chunk = json.loads(event["chunk"]["bytes"])["content"][0]["text"]
                assistant_response += chunk
                self.chat_area.insertPlainText(chunk)
                self.chat_area.ensureCursorVisible()
                QApplication.processEvents()

            self.chat_area.append("\n")
            self.conversation_history[model].append({"role": "assistant", "content": assistant_response})
            self.update_token_count()

        except:
            print("Error occurred while calling Anthropic model")
            raise

    def limit_conversation_history(self, model, token_limit):
        token_count = self.count_tokens(model)
        while token_count > token_limit:
            self.conversation_history[model].pop(0)
            token_count = self.count_tokens(model)

    def count_tokens(self, model):
        num_tokens = 0
        try:
            self.conversation_history[model]
        except KeyError:
            return num_tokens
        
        for message in self.conversation_history[model]:
            num_tokens += 4  # Each message incurs a small overhead
            for key, value in message.items():
                num_tokens += len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(value))
                if key == "name":
                    num_tokens += -1  # Adjust for specific key names if necessary
        num_tokens += 2  # Account for additional overhead
        return num_tokens

    def update_token_count(self):
        if not self.selected_models:
            self.token_label.setText("Token Count: 0")
            return

        text_to_append = []
        for model in self.selected_models:
            token_count = self.count_tokens(model)
            text_to_append.append(f"Token Count ({self.model_info[model]['display_name']}): {token_count}")
                
        self.token_label.setText("\n".join(text_to_append))

    def clear_conversation(self):
        self.conversation_history = {}
        self.chat_area.clear()
        self.update_token_count()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatbot_gui = ChatbotGUI()
    chatbot_gui.show()
    sys.exit(app.exec_())
