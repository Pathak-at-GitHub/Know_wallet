from flask_socketio import SocketIO, send
from flask import Flask, render_template



app = Flask(__name__, template_folder='./HTML_CSS_Req/')
app.config['SECRET'] = "secret!123"

socketio = SocketIO(app, cors_allowed_origins = "*")

@socketio.on('message')
def handle_message(message):
    print("Received messages: "+message)
    if message != "User connected!":
        send(message, broadcast=True)
    else:
        print('connected')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host="localhost",allow_unsafe_werkzeug=True)