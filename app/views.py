from app import app
from redis import Redis
import socket

# Create a connection to redis
r = Redis(host='redis')
r.set('count', 0)


# Serve a page which shows the hostname and increments visit counter
@app.route('/')
def index():
    r.incr('count')
    return "Hello, World! From {0}\nVisit count {1}\n".format(socket.gethostname(), int(r.get("count")))
