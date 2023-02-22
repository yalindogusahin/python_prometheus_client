#!/usr/bin/env python3

import os
import iperf3
import time

try:
    port = os.environ['port']
except:
    print('server port is not given!')
    print("you didn't specified port its port=888")
    port = 888

server = iperf3.Server()
server.port=port
#print('Running server: {0}:{1}'.format(server.bind_address, server.port))

while True:
    result = server.run()
    if result.error:
        print("Testte hata var!",result.error)
        result.error
    else:
        print('')
        print('Test results from {0}:{1}'.format(result.remote_host,
                                                result.remote_port))
        print('  started at         {0}'.format(result.time))
        print('  bytes received     {0}'.format(result.received_bytes))
        print('Average transmitted received in all sorts of networky formats:')
        print('  bits per second      (bps)   {0}'.format(result.received_bps))
        print('  Kilobits per second  (kbps)  {0}'.format(result.received_kbps))
        print('  Megabits per second  (Mbps)  {0}'.format(result.received_Mbps))
        print('  KiloBytes per second (kB/s)  {0}'.format(result.received_kB_s))
        print('  MegaBytes per second (MB/s)  {0}'.format(result.received_MB_s))
        print('')