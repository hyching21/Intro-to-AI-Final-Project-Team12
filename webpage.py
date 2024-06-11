import os
from flask import Flask, request, render_template
from pyngrok import ngrok
import tensorflow as tf
import numpy as np
import jieba
import re
from tensorflow.python.keras.models import load_model
from tensorflow.keras.layers import Bidirectional, LSTM
from tensorflow.keras.utils import pad_sequences
import pickle

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

from tensorflow.python.keras.engine import data_adapter

def _is_distributed_dataset(ds):
    return isinstance(ds, data_adapter.input_lib.DistributedDatasetSpec)

data_adapter._is_distributed_dataset = _is_distributed_dataset

jieba.set_dictionary('dict.txt.big')

# Load your BLSTM model

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

custom_objects = {'Bidirectional': Bidirectional, 'LSTM': LSTM}
model = load_model('40BLSTM_model.h5', compile=False, custom_objects=custom_objects)

emoji_raw = open('40_mapping_emojis.txt','r',encoding="utf-8")

emojis=[]
for sentence in emoji_raw:
    sentence = sentence.rstrip()
    emojis.append(sentence)

emoji_dict={}

for e in emojis:
    idx = int(e.split()[0])
    emoji = e.split()[1]
    emoji_dict[idx] = emoji

def get_stopwords(file):
    stopword_list = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            stopword_list.append(line)
    return stopword_list

def remove_stopwords(sentence, stopwords):
    return [word for word in sentence if word not in stopwords and word.strip()]

stopwords = get_stopwords('stopwords.txt')  

def preprocess_text(X):
    tokenized_sentences = []
    for sentence in X:
      words = list(jieba.cut(sentence))
      filtered_words = remove_stopwords(words, stopwords)
      tokenized_sentences.append(filtered_words)
    tokenized_texts = [" ".join(sentence) for sentence in tokenized_sentences]

    max_len=40
    X_seqs = tokenizer.texts_to_sequences(tokenized_texts)
    X_seqs_pd = pad_sequences(X_seqs, truncating="pre", padding="pre", maxlen=max_len)
    return X_seqs_pd

def predict_emoji(text):
    X_sequences = preprocess_text([text])
    predictions = np.argmax(model.predict(X_sequences), axis=1)
    emoji_idx = predictions[0]
    emoji = emoji_dict[emoji_idx]

    return emoji

def emojify_paragraph(paragraph):
    lines = re.split(r'[\n，。]', paragraph)
    emojified_lines = []

    for line in lines:
        if line.strip():
            emojified_line = line + predict_emoji(line)
            emojified_lines.append(emojified_line)
        else:
            emojified_lines.append(line)

    emojified_paragraph = '\n'.join(emojified_lines)
    return emojified_paragraph

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form["text"]
        result = emojify_paragraph(text)
        return render_template("index.html", result=result)
    return render_template("index.html", result="")

os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write('''<!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Emoji Transformer</title>
            <style>
                body {
                    background-image: url('/static/6.jpg'); /* Update this path */
                    background-size: cover;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    width: 90%;
                    max-width: 500px;
                    text-align: center;
                }
                h1 {
                    color: #333;
                }
                textarea {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 4px;
                    border: 1px solid #ccc;
                    font-size: 16px;
                }
                input[type="submit"] {
                    background-color: #000;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                h2 {
                    color: #333;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Emoji Transformer</h1>
                <p>歡迎使用 Emoji 轉換器。請輸入文本讓我們幫您加上表情符號吧～</p>
                <form method="post">
                    <textarea name="text" rows="4" placeholder="輸入文本..."></textarea>
                    <br><br>
                    <input type="submit" value="轉換">
                </form>
                <h2>结果: {{ result }}</h2>
            </div>
        </body>
        </html>
    ''')
# 启动 ngrok 隧道
public_url = ngrok.connect(5000, bind_tls=True)
print("Public URL:", public_url)

# 启动 Flask 应用
if __name__ == "__main__":
    app.run(port=5000)