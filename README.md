## load_balancing

**Experiments with load balancing a flask app using *nginx* or *haproxy***

### Run nginx version:

    todo

### Run haproxy version:

From project root, for 3 web-servers:

    docker-compose -f docker-compose-haproxy.yml scale web=3
    docker-compose -f docker-compose-haproxy.yml up

