from concurrent.futures import thread
from flask import Flask
from wsgiref.simple_server import make_server
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Summary, Gauge, Info, Histogram
from iperf_client import client_start
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY
import threading
import sched, time
import os

try:
    hostName = os.environ['hostName']
    port = os.environ['port']
    schedule_time = os.environ['schedule_time']
except:
    print('hostName, port, schedule_time is not given!')
    print('hostName = serverIP, port=5201, you need to specify the scheduled_time for how many seconds wait for the between each iperf test!')
    while(1):
        time.sleep(1)

# Flask settings for /metrics-text path
app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics-text': make_wsgi_app(REGISTRY)})

# Create a metric to track time spent and requests made.
b = Gauge('bandwidth_requests_sent_bytes', 'sent_bytes')
c = Gauge('bandwidth_requests_retransmits', 'retransmits')
d = Gauge('bandwidth_requests_local_cpu_system', 'local_cpu_system')
e = Gauge('bandwidth_requests_sent_bps', 'sent_bps')
f = Gauge('bandwidth_requests_sent_kbps', 'sent_kbps')
g = Gauge('bandwidth_requests_sent_Mbps', 'sent_Mbps')
h = Gauge('bandwidth_requests_sent_kB_s', 'sent_kB_s')
j = Gauge('bandwidth_requests_sent_MB_s', 'sent_MB_s')

# Thread for pushing metrics to flask
def process_request():

    print('inside of the process_request function')

    # iperf_clint function returns those variables
    # return result.error, result.time, result.sent_bytes, result.retransmits, result.local_cpu_system, result.sent_bps, result.sent_kbps, result.sent_Mbps, result.sent_kB_s, result.sent_MB_s
    
    def shceduled_function(scheduler):

        print('inside of the scheduled_function')
        scheduler.enter(schedule_time, 1, shceduled_function, (scheduler,))
        response = client_start(hostName,port)

        if response[0] == 'unable to send control message:':
            print('There is an error on iperf3! Message = ', response[0])
            print('Response = ', response)
        else:
            print('response =', response)
            b.set(int(response[2]))
            c.set(int(response[3]))
            d.set(int(response[4]))
            e.set(int(response[5]))
            f.set(int(response[6]))
            g.set(int(response[7]))
            h.set(int(response[8]))
            j.set(int(response[9]))


    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(5, 1, shceduled_function, (my_scheduler,))
    my_scheduler.run()
           
    
def run_app():
    app.run(host='0.0.0.0',threaded=True,port = 8080, debug= False)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=process_request)
    first_thread.start()
    second_thread.start()

