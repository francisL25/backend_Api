import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import tensorflow as tf
import json
import random
import openai
from ..config import Config

lemmatizer = WordNetLemmatizer()
model = tf.keras.models.load_model('app/config/datos.h5')
with open('app/config/intents.json', encoding='utf-8') as fh:
    intents = json.load(fh)
words = pickle.load(open('app/config/palabras.pkl', 'rb'))
classes = pickle.load(open('app/config/clases.pkl', 'rb'))

openai.api_key = Config.OPENAI_API_KEY

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"found in bag: {w}")
    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    if np.all(p == 0):
        return []
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "Introduzca su texto"

def model_response(msg):
    ints = predict_class(msg, model)
    return getResponse(ints, intents) if ints else "Introduzca su texto"

def get_completion(prompt, model="gpt-3.5-turbo-1106"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content