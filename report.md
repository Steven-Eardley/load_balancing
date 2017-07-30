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

Run ```docker-compose -f compose-nginx.yml up --build``` to bring up the pool 
fronted by nginx.

The command below will issue 50 requests with timestamps so we can check the 
response patterns.

    for i in {1..50}; do curl -s localhost:8080 | tee -a nginx_hiworld_sequence; echo `date +%T`; sleep 1s; done;

The results follow, annotated to more clearly mark which container it was:

```
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
Hello, World! From a79cb7bcaa8c 20:21:09    x
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
Hello, World! From a79cb7bcaa8c 20:21:37    x
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
Hello, World! From a79cb7bcaa8c 20:22:07    x
Hello, World! From c5341b534706 20:22:08    o
Hello, World! From a79cb7bcaa8c 20:22:09    x
Hello, World! From c5341b534706 20:22:10    o
Hello, World! From a79cb7bcaa8c 20:22:12    x
Hello, World! From c5341b534706 20:22:13    o
Hello, World! From a79cb7bcaa8c 20:22:14    x
Hello, World! From c5341b534706 20:22:15    o
Hello, World! From a79cb7bcaa8c 20:22:16    x
```

### HAPROXY

Run 
