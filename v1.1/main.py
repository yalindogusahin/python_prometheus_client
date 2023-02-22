from concurrent.futures import thread
from flask import Flask
from wsgiref.simple_server import make_server
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Summary, Gauge, Info
from pingat import ping_at
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY
import threading
import time
import os

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics-text': make_wsgi_app(REGISTRY)})

# Create a metric to track time spent and requests made.
g = Gauge('my_inprogress_requests', 'host is up')
y = Gauge('my_inprogress_requests2', 'host is down')
min = Gauge('Ping_Minimum','host is probably up')
max = Gauge('Ping_Maximum','host is probably up2')
ava = Gauge('Ping_Avarage','host is probably up3')

try:
    hostName = os.environ['hostName']
    print(hostName)
except:
    hostName = '8.8.8.8'
    print(hostName)

# Decorate function with metric.
def process_request():
        while(1):   
            print(hostName)
            hostname = hostName
            response = ping_at(hostname)
            print(response)

            #and then check the response...
            if response[0] == '100':
                print(hostname, 'is down!')
                print(response)
                y.inc()

            else:
                print(hostname, 'is up!')
                print(response)
                g.inc()
                min.set(response[1])
                max.set(response[2])
                ava.set(response[3])
    
def run_app():
    app.run(host='0.0.0.0',threaded=True,port = 8080, debug= False)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=process_request)
    first_thread.start()
    second_thread.start()

