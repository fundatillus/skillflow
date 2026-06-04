bind = "unix:/run/skillflow/gunicorn.sock"
workers = 3
worker_class = "sync"
user = "skillflow"
group = "www-data"
umask = 0o007
timeout = 30
