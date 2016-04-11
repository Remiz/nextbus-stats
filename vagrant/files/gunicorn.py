import multiprocessing


bind = "127.0.0.1:8888"
workers = multiprocessing.cpu_count() * 2
user = '{{project_user}}'
logfile = "/home/{{project_user}}/logs/gunicorn.log"
loglevel = "info"
pidfile = '/tmp/{{project_user}}.pid'
daemon = False
debug = False
timeout = 300
