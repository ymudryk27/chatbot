import json
import random
import nltk
from nltk.stem import WordNetLemmatizer

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

print("Bot: Hi! Type 'quit' to exit.")
while True:
    msg = input("You: ")
    if msg.lower() == "quit":
        break
    tag = predict_class(msg)
    print("Bot:", get_response(tag))