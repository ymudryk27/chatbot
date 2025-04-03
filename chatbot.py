import json
import random
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import tkinter as tk
from tkinter import scrolledtext

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

with open("intents.json") as file:
    intents = json.load(file)

def clean_text(text):
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

def predict_class(text):
    tokens = clean_text(text)
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = clean_text(pattern)
            if all(word in tokens for word in pattern_tokens):
                return intent
    return None

def get_response(user_input):
    intent = predict_class(user_input)
    if intent:
        return random.choice(intent["responses"])
    else:
        return "I'm not sure I understand. Can you try again?"

def send_message():
    msg = entry.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + msg + "\n")
    response = get_response(msg)
    chat_log.insert(tk.END, "Bot: " + response + "\n")
    chat_log.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

window = tk.Tk()
window.title("Chatbot (NLTK)")

chat_log = scrolledtext.ScrolledText(window, state='disabled', width=50, height=20, bg="black", fg="white")
chat_log.pack(padx=10, pady=10)

entry = tk.Entry(window, width=50)
entry.pack(padx=10, pady=5)

send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(pady=5)

window.mainloop()