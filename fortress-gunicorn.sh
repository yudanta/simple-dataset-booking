# gunicorn --name 'DB CMS WEB' --chdir /home/fortress/src --timeout 300 -b 0.0.0.0:$PORT app:app -k gevent --worker-connections 5 --workers 1 --reload
gunicorn --name 'DB CMS WEB' --chdir /home/fortress/src --timeout 300 -b 0.0.0.0:8000 app:app -k gevent --worker-connections 5 --workers 1 --reload