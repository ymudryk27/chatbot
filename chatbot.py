import json
import random
import nltk
import tkinter as tk
from tkinter import scrolledtext
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

with open("intents.json", "r") as file:
    intents = json.load(file)

words = []
classes = []
documents = []

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        documents.append((tokens, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w.isalpha()]
words = sorted(set(words))
classes = sorted(set(classes))

def clean_input(sentence):
    tokens = nltk.word_tokenize(sentence)
    tokens = [lemmatizer.lemmatize(w.lower()) for w in tokens if w.isalpha()]
    return tokens

def predict_class(sentence):
    tokens = clean_input(sentence)
    for doc in documents:
        pattern_words = [lemmatizer.lemmatize(w.lower()) for w in doc[0] if w.isalpha()]
        if set(tokens).intersection(pattern_words):
            return doc[1]
    return "unknown"

def get_response(tag):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "Sorry, I don't understand."


def send_message():
    user_input = entry.get()
    chat_log.insert(tk.END, "You: " + user_input + "\n")
    entry.delete(0, tk.END)

    tag = predict_class(user_input)
    response = get_response(tag)
    chat_log.insert(tk.END, "Bot: " + response + "\n")

root = tk.Tk()
root.title("Chatbot (NLTK)")

chat_log = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD, font=("Helvetica", 12))
chat_log.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40, font=("Helvetica", 12))
entry.pack(padx=10, pady=5)
entry.bind("<Return>", lambda event: send_message())

send_btn = tk.Button(root, text="Send", command=send_message, font=("Helvetica", 12))
send_btn.pack(pady=5)

root.mainloop()