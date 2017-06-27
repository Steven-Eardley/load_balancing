from app import app
from redis import Redis
import socket, os, time

# Create a connection to redis
r = Redis(host='redis')
r.set('count', 0)

# A sequence of 35 random numbers which will stay the same between tests (random.seed didn't work).
seq = [1, 6, 8, 9, 2, 8, 6, 5, 3, 9, 10, 12, 9, 2, 7, 11, 7, 8, 3, 7, 4, 7, 1, 4, 3, 8, 1, 6, 12, 10, 7, 4, 11, 5, 10]
slow_count = 0


# Serve a page which shows the hostname and increments visit counter
@app.route('/')
def index():
    if bool(os.getenv('SLOW_APP', False)):
        global slow_count
        rnd = seq[slow_count % len(seq)]                                                # treat sequence as circular
        print('Sleeping for {0} seconds before replying.'.format(rnd))
        time.sleep(rnd)
        slow_count += 1
    r.incr('count')
    return "Hello, World! From {0}\nVisit count {1}\n".format(socket.gethostname(), int(r.get("count")))
