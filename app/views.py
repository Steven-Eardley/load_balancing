from app import app
from redis import Redis
import socket, os, time, random

# Create a connection to redis
r = Redis(host='redis')
r.set('count', 0)


# Serve a page which shows the hostname and increments visit counter
@app.route('/')
def index():
    if bool(os.getenv('SLOW_APP', False)):
        rnd = random.randint(0, 33)
        print('Sleeping for {0} seconds before replying.'.format(rnd))
        time.sleep(rnd)
    r.incr('count')
    return "Hello, World! From {0}\nVisit count {1}\n".format(socket.gethostname(), int(r.get("count")))
