from flask import Flask, render_template, session, redirect
from google import auth
from google.cloud import storage
import pickle
import random
import os

storage_client = storage.Client()
bucket = storage_client.bucket(os.getenv("GPOETRY_BUCKET"))
blob = bucket.blob(os.getenv("GPOETRY_FILE"))
poems = pickle.loads(blob.download_as_bytes())
authors = list(poems.keys())
poem_info = {}
poem_ix = {}
ix = 0
for author in authors:
    for type in ['real', 'fake']:
        for poem_key in list(poems[author][type].keys()):
            poem_info[ix] = {'type':type, 'text':poems[author][type][poem_key]}
            poem_ix[poem_key] = ix
            ix += 1

app = Flask(__name__)
app.secret_key = os.urandom(50)

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/get_poems')
def get_poems():
    author = random.choice(authors)
    real = random.choice(list(poems[author]['real'].keys()))
    real_ix = poem_ix[real]
    real_info = {'id':real_ix, 'text':poem_info[real_ix]['text']}
    fake = random.choice(list(poems[author]['fake'].keys()))
    fake_ix = poem_ix[fake]
    fake_info = {'id':fake_ix, 'text':poem_info[fake_ix]['text']}
    if random.random() > .5:
        return {'poem_pair':[real_info, fake_info]}
    else:
        return {'poem_pair':[fake_info, real_info]}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)