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
import re

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics-text': make_wsgi_app(REGISTRY)})

# Create a metric to track time spent and requests made.
host_status = Gauge('host_status', 'host_status_check')
min = Gauge('Ping_Minimum','minimum_ping_check')
max = Gauge('Ping_Maximum','maximum_ping_check')
ava = Gauge('Ping_Avarage','avarage_ping_check')
portStatus = Gauge('Port_status','port_status_check')

# Decorate function with metric.
def process_request():
        while(1):   
            # Container Environment Variable'ları çekmeye çalışıyor. Çekemez ise değerler = (hostName google.com, ping_type ping, port 80)
            try:
                hostName = os.environ['hostName']
                ping_type = os.environ['mission']
                port = os.environ['port']
                
                print("hostname= ", hostName)
                print("ping_type= ", ping_type)
            
            except:
                hostName = '8.8.8.8'
                ping_type = 'ping'
                port = '80'
            
                print("hostname= ", hostName)
                print("ping type seçmediğin için ping seçildi.",ping_type)
            
            hostname = hostName
            try:
                response = ping_at(hostname,ping_type,port)
                print(response)
                print("response[0]",response[0])
                print(type(response[0]))
                if response[0] == 100.0:
                    print(hostname, 'is down!')
                    print(response)
                    portStatus.set(0)
                    host_status.set(0)

                else:
                    print(hostname, 'is up!')
                    print(response)
                    host_status.set(1)
                    portStatus.set(1)
                    min.set(response[1])
                    max.set(response[2])
                    ava.set(response[3])
            except:
                print("response dönüş alamadı")
                min.set(0)
                max.set(0)
                ava.set(0)
                host_status.set(0)
                
                
    
def run_app():
    app.run(host='0.0.0.0',threaded=True,port = 8080, debug= False)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=process_request)
    first_thread.start()
    second_thread.start()

