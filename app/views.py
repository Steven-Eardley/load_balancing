from app import app
import socket, os, time

# Our behaviour sequence for broken machines - 5 quick responses then 5 very slow ones
seq = [1] * 5 + [20] * 5 + [1] * 5
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
    return "Hello, World! From {0} ".format(socket.gethostname()), 200

