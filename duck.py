from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QIcon
import random
import sys
import os

class RubberDuckChatApp(QWidget):
    def __init__(self):
        super().__init__()

        self.is_pinned = False

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle("Rubber Duck")
        self.setGeometry(100, 100, 400, 500)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.title_bar = QWidget(self)
        self.title_bar.setStyleSheet("background-color: #444444;")
        self.title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout()
        title_label = QLabel("🦆 Rubber Duck", self.title_bar)
        title_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold; padding-left: 10px;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        self.pin_button = QPushButton("📌", self.title_bar)
        self.pin_button.setFixedSize(30, 30)
        self.pin_button.setCheckable(True)
        self.pin_button.setStyleSheet("background-color: #555555; border: none; color: white;")
        self.pin_button.clicked.connect(self.toggle_pin)
        title_layout.addWidget(self.pin_button)

        close_button = QPushButton("X", self.title_bar)
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("background-color: #ff5f5f; border: none; color: white;")
        close_button.clicked.connect(self.close)
        title_layout.addWidget(close_button)
        
        self.title_bar.setLayout(title_layout)
        layout.addWidget(self.title_bar)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            background-color: #1e1e2e;
            color: white;
            font-family: Arial;
            font-size: 20px;
            border: none;
            padding: 10px;
        """)
        layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()
        self.user_input = QLineEdit(self)
        self.user_input.setStyleSheet("""
            background-color: #404040;
            color: white;
            font-family: Arial;
            font-size: 20px;
            border-radius: 15px;
            padding: 10px;
        """)
        self.user_input.returnPressed.connect(self.send_message)  # Bind Enter key to send message
        input_layout.addWidget(self.user_input)

        self.send_button = QPushButton(self)
        self.send_button.setIcon(QIcon("icon.svg"))  # Replace with your paper airplane icon
        self.send_button.setIconSize(self.send_button.size())
        self.send_button.setStyleSheet("""
            background-color: #ffbf00;
            border: none;
            border-radius: 15px;
            padding: 10px;
            width: 50px;
            height: 50px;
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

        self.duck_image_path = os.path.abspath("RubberDuck.png")
        self.user_image_path = os.path.abspath("user.png")

        self.quack_phrases = [
            "Quack! Quack quack.", "Quack. 😎", "Quaaack. 😠",
            "QuaCK qUacK!", "Qu-qu-qu-quack!", "Quaaaack... qu-quack.",
            "Qu-quack. 💨", "Quack!", "Quack Quack", "Quack!", 
            "Quack!!!", "Quaaaack", "Quack Quack Quack", "QUACK!!!!",
            "Quackity quack!", "Quack Quack... Quack?", "Quack! Quack! Quack!",
            "Quaaaack Quack.", "Quack-a-doodle-doo!", "Quack-a-lackin'!",
            "Quaaaack, quack-quack.", "QUA-QUACK!", "Quack attack!", 
            "Quack quack quack, quack quack.", "QUACK!! Quack quack quack!",
            "QUAAAACK!!!", "Quack... 🦆", "Quack-a-lot!", "Quack quack. 😏",
            "Quack-quack-quack-quack!", "Quack? Quack! Quack.", "Quack... Quack?"
        ]
        self.emoji_responses = {
            "love": "Quack Quack! 💖",
            "cute": "Quack! 😊",
            "sad": "Quack... 😢",
            "angry": "QUACK! 😠",
            "thanks": "Quack Quack! 🙏",
            "excited": "Quaaaack! 🎉",
            "happy": "Quack Quack! 😁",
            "surprised": "Quack?! 😲",
            "confused": "Quack? 🤔",
            "tired": "Quaaack... 😴",
            "cool": "Quack. 😎",
            "funny": "Quack Quack! 😂",
            "thinking": "Quack... 💭",
            "celebrate": "Quack Quack! 🎊",
            "thumbsup": "Quack Quack! 👍",
            "thumbsdown": "Quack... 👎",
            "clap": "Quack Quack! 👏",
            "smile": "Quack Quack! 😊",
            "wink": "Quack! 😉",
            "bored": "Quack... 😐"
        }

        self.oldPos = self.pos()

    def quack(self):
        return random.choice(self.quack_phrases)

    def respond(self, message):
        for keyword in self.emoji_responses:
            if keyword in message.lower():
                return self.emoji_responses[keyword]
        return self.quack()

    def send_message(self):
        user_message = self.user_input.text()
        if user_message:
            self.display_message("You", user_message, self.user_image_path)
            duck_response = self.respond(user_message)
            self.display_message("RubberDuck", duck_response, self.duck_image_path)
            self.user_input.clear()

    def display_message(self, sender, message, image_path):
        if os.path.exists(image_path):
            img_tag = f"<img src='{image_path}' width='32' height='32'>"
        else:
            img_tag = ""  

        self.chat_display.append(f"{img_tag} {sender}: {message}")

    def toggle_pin(self):
        if self.is_pinned:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.is_pinned = False
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.is_pinned = True

        self.show()  


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

app = QApplication(sys.argv)
chat_app = RubberDuckChatApp()
chat_app.show()
sys.exit(app.exec_())
