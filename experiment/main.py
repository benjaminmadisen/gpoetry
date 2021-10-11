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

app = Flask(__name__)
app.secret_key = os.urandom(50)

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/get_poems')
def get_poems():
    poem_response = []
    sample_authors = random.sample(authors,25)
    ix = 0
    for author in sample_authors:
        ix += 1
        real_key = random.choice(list(poems[author]['real'].keys()))
        real = poems[author]['real'][real_key]
        real_info = {'type':'real', 'text':real.strip(), 'chosen':False, 'ix':ix,
                     'name':real_key[:65],
                     'author':" ".join([n.capitalize() for n in author.split("-")])}
        fake_key = random.choice(list(poems[author]['fake'].keys()))
        fake = poems[author]['fake'][fake_key]
        fake_info = {'type':'fake', 'text':fake.strip(), 'chosen':False, 'ix':ix,
                     'name':fake_key[:65],
                     'author':" ".join([n.capitalize() for n in author.split("-")])}
        if random.random() > .5:
            real_info['option'] = 0
            fake_info['option'] = 1
            poem_response.append([real_info, fake_info])
        else:
            real_info['option'] = 1
            fake_info['option'] = 0
            poem_response.append([fake_info, real_info])
    return {'poem_pairs':poem_response}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)