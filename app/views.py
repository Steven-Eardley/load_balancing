from app import app
from redis import Redis
import socket, os, time

# Create a connection to redis
r = Redis(host='redis')
r.set('count', 0)

# A sequence of random numbers which will stay the same between tests (random.seed didn't work).
seq = [1, 6, 8, 9, 2, 10, 12, 11, 9, 2, 7, 11, 7, 8, 3]
slow_count = 0


# Serve a page which shows the hostname and increments visit counter
@app.route('/')
def index():
    if bool(os.getenv('SLOW_APP', False)):
        global slow_count
        rnd = seq[slow_count % len(seq)]                                                    # treat sequence as circular
        print('Sleeping for {0} seconds before replying.'.format(rnd))
        time.sleep(rnd)
        slow_count += 1
    r.incr('count')
    return "Hello, World! From {0}\nVisit count {1}\n".format(socket.gethostname(), int(r.get("count")))
