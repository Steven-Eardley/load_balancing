## load_balancing

**Experiments with load balancing a flask app using *nginx* or *haproxy***

### Run nginx version:

    todo

### Run haproxy version:

From project root, for 3 web-servers:

    docker-compose -f docker-compose-haproxy.yml up             # Builds initial containers and creates network
    docker-compose -f docker-compose-haproxy.yml scale web=3    # Creates 3 web apps
    docker-compose -f docker-compose-haproxy.yml up             # Run the whole service
    
Connect to port ```localhost:8080``` to see the load balancing effect.

#### Optional - give it a better name
Because the project directory is called ```src```, you'll get containers named like ```src_redis_1```. If you want a
better name, add the argument ```-p, --project-name``` to ```docker-compose```:

    docker-compose -f docker-compose-haproxy.yml -p hi-hiproxy up

#### To scale down

I find (Docker for Mac 17.03.1-ce, compose 1.11.2) simply re-running ```docker-compose scale``` with a lower count
doesn't reduce the count on the next ```docker-compose up```, you must first run ```docker-compose down```, re-scale,
then back ```up``` to get the reduction.

