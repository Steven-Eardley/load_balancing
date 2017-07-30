## Load Balancing Test

**Aim**: Investigate and resolve issue with DOAJ index servers, which cause the 
app to fail when they are slow to respond. NGINX doesn't remove the servers 
from the pool, so the gunicorn workers experience a timeout when accessing the
index.


### Testing infrastructure

Running on Docker:

* Flask web app
    * Optionally 'misbehaving', which sleeps before replying.
    * Run 2 copies of normal, ```hiworld``` ```1``` & ```2```, one misbehaving; ```brokenworld```
* Load balancer, accessible via port ```8080```, nginx or haproxy.

The broken app responds quickly (1s sleep) for 5 requests, then slowly (20s sleep) for 5 requests.

### NGINX

```nginx``` has been configured for a 15s timeout when connecting to the upstream
servers, the 3 web app machines, with the setting ```proxy_read_timeout 15s;```.

Run ```docker-compose -f compose-nginx.yml up --build``` to bring up the pool 
fronted by nginx.

The command below will issue 50 requests with timestamps so we can check the 
response patterns.

    for i in {1..50}; do curl -s localhost:8080 | tee -a nginx_hiworld_sequence; echo `date +%T`; sleep 1s; done;

The results follow, annotated to more clearly mark which container has replied:

```
hostname       container    label
a79cb7bcaa8c   hiworld1     x
c5341b534706   hiworld2     o
187b0a4de190   brokenworld  #

<- shows a large gap where timeouts occured

Hello, World! From a79cb7bcaa8c 20:20:30    x
Hello, World! From c5341b534706 20:20:31    o
Hello, World! From 187b0a4de190 20:20:34    #
Hello, World! From a79cb7bcaa8c 20:20:35    x
Hello, World! From c5341b534706 20:20:36    o
Hello, World! From 187b0a4de190 20:20:38    #
Hello, World! From a79cb7bcaa8c 20:20:39    x
Hello, World! From c5341b534706 20:20:40    o
Hello, World! From 187b0a4de190 20:20:42    #
Hello, World! From a79cb7bcaa8c 20:20:43    x
Hello, World! From c5341b534706 20:20:44    o
Hello, World! From 187b0a4de190 20:20:46    #
Hello, World! From a79cb7bcaa8c 20:20:48    x
Hello, World! From c5341b534706 20:20:49    o
Hello, World! From 187b0a4de190 20:20:51    #
Hello, World! From a79cb7bcaa8c 20:20:52    x
Hello, World! From c5341b534706 20:20:53    o
Hello, World! From a79cb7bcaa8c 20:21:09    x   <-
Hello, World! From c5341b534706 20:21:10    o
Hello, World! From a79cb7bcaa8c 20:21:11    x
Hello, World! From c5341b534706 20:21:12    o
Hello, World! From a79cb7bcaa8c 20:21:13    x
Hello, World! From c5341b534706 20:21:15    o
Hello, World! From a79cb7bcaa8c 20:21:16    x
Hello, World! From c5341b534706 20:21:17    o
Hello, World! From a79cb7bcaa8c 20:21:18    x
Hello, World! From c5341b534706 20:21:19    o
Hello, World! From a79cb7bcaa8c 20:21:20    x
Hello, World! From c5341b534706 20:21:21    o
Hello, World! From a79cb7bcaa8c 20:21:37    x   <-
Hello, World! From c5341b534706 20:21:39    o
Hello, World! From a79cb7bcaa8c 20:21:40    x
Hello, World! From c5341b534706 20:21:41    o
Hello, World! From a79cb7bcaa8c 20:21:42    x
Hello, World! From c5341b534706 20:21:43    o
Hello, World! From a79cb7bcaa8c 20:21:45    x
Hello, World! From c5341b534706 20:21:46    o
Hello, World! From a79cb7bcaa8c 20:21:47    x
Hello, World! From c5341b534706 20:21:48    o
Hello, World! From a79cb7bcaa8c 20:21:49    x
Hello, World! From c5341b534706 20:21:51    o
Hello, World! From a79cb7bcaa8c 20:22:07    x   <-
Hello, World! From c5341b534706 20:22:08    o
Hello, World! From a79cb7bcaa8c 20:22:09    x
Hello, World! From c5341b534706 20:22:10    o
Hello, World! From a79cb7bcaa8c 20:22:12    x
Hello, World! From c5341b534706 20:22:13    o
Hello, World! From a79cb7bcaa8c 20:22:14    x
Hello, World! From c5341b534706 20:22:15    o
Hello, World! From a79cb7bcaa8c 20:22:16    x
```

We can see our load balancer round-robining the connections between all three
machines while ```brokenworld``` is replying quickly, then once the timeout is
exceeded we see only the speedy servers for a spell. However, nginx will still
periodically reinstate ```brokenworld``` into the pool, send it requests, and 
allow a new timeout to occur. That's where we see ```<-``` in the output above - 
there is a delay before ```hiworld1``` takes up the request.

Of course, without any explicit health checks (a feature of 
[nginx plus](https://www.nginx.com/products/application-load-balancing/) for lots 
of money) that's all nginx can do - it infers by the performance that a proxied
machine is down or slow, gives is a break, and tries again later. The only 
communication is has are the actual user requests, so that's what it sends to
determine whether a machine is up or not. The timeout delays are a necessary 
effect of this approach.

This means that when using nginx as a load balancer, the ```proxy_read_timeout```
setting should be as low as possible (as with all timeouts, really). However, 
because in the DOAJ we are proxying ElasticSearch servers, we had it set fairly
high to allow for how long a particularly tricky query may take. 

### \#fixme: how to express what's really killing the app

### HAPROXY

The command to run this version is ```docker-compose -f compose-haproxy-custom.yml up --build```.
```haproxy``` has also been configured to use a 15s timeout when connecting to 
upstream servers with the directive ```timeout server  15000```.

Haproxy allows us to configure health checks; here we have a check for the
```brokenworld``` server. It's simply making a ```GET``` to the webapp root. In
actuality for web servers we'd have a bespoke lightweight endpoint, for ElasticSearch
we would use a simple query or count. The health check interval is 5 seconds; 
it takes 2 successful checks to bring the server back into the pool, one to
consider it down.
     
    option httpchk GET /
    server brokenworld brokenworld:80 check inter 5s rise 2 fall 1

The other app servers aren't checked because they'll always succeed and
that'd just introduce noise in the logs. 

As above, we can test the system with the following command:

    for i in {1..50}; do curl -s localhost:8080 | tee -a haproxy_hiworld_sequence; echo `date +%T`; sleep 1s; done;


