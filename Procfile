gunicorn --worker-class gevent --timeout 30 --graceful-timeout 20 --max-requests-jitter 2000 --max-requests 1500 -w 50 --log-level DEBUG --capture-output --bind 0.0.0.0:5000 run:app
