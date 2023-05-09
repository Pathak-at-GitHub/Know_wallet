from flask_socketio import SocketIO, send
from flask import Flask, render_template,request
import os
import openai
import re

openai.api_key = os.getenv("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")## Put openai key here

app = Flask(__name__)
app.config['SECRET'] = "secret!123"

socketio = SocketIO(app, cors_allowed_origins = "*")

@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

@app.route('/',methods = ['POST'])
def predict():
    data = request.get_data()

    text = data.decode('utf-8')
    text = text[90:]
    text = text[::-1]
    text = text[42:]
    text = text[::-1]

    ##### This is OpenAI API response generator

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=0.7,
            max_tokens=1100,
            top_p=1,
            best_of=2,
            frequency_penalty=0.17,
            presence_penalty=0.15
        )
        # Extract the generated text from the response
        text = response.choices[0].text
        # Remove any unwanted characters from the text
        text = re.sub('[^0-9a-zA-Z\n\.\?,!]+', ' ', text)
        # Print the generated text
        print(text)
    except Exception as e:
        print("An error occurred: {}".format(e))

    return render_template('index.html', prediction = text)

if __name__ == '__main__':
    socketio.run(app, host="localhost",allow_unsafe_werkzeug=True)

