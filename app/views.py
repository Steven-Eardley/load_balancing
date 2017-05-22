from app import app
import socket


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World! From {0}".format(socket.gethostname())
