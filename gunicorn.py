bind = 'unix:/tmp/flask_app.sock'
backlog = 2048

worker_class = 'eventlet'
debug = False
spew = False

proc_name = 'antares'