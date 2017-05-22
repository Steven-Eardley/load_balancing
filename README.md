## load_balancing

Run app with:
```uwsgi --http-socket localhost:8080 --manage-script-name --mount /web=app:app --virtualenv ~/code/cl/load_balancing --plugin python3```
