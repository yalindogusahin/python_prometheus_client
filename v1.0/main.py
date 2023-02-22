#!/bin/sh

from prometheus_client import start_http_server, Summary, Gauge, Info
import random

import time
import os
import json
from pingat import ping_at


# Create a metric to track time spent and requests made.
g = Gauge('my_inprogress_requests', 'host is up')
y = Gauge('my_inprogress_requests2', 'host is down')
min = Gauge('Ping_Minimum','host is probably up')
max = Gauge('Ping_Maximum','host is probably up2')
ava = Gauge('Ping_Avarage','host is probably up3')

# Decorate function with metric.

def process_request():
    hostname = "8.8.8.8"
    response = ping_at('8.8.8.8')
    print(response)
    
    #and then check the response...
    if response[0] == '100%':
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

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8080)
    # Generate some requests.
    while True:
        process_request()

        