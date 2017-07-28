from app import app
import socket, os, time

# A sequence of random numbers which will stay the same between tests (random.seed didn't work).
#seq = [1, 2, 3, 4, 6, 1, 1, 2, 7, 2, 7, 1, 7, 1, 10, 13]
seq = [2, 6, 1, 6, 6, 6, 6]
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
    return "Hello, World! From {0}\n".format(socket.gethostname()), 200

