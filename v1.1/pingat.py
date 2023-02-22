from sys import platform
import subprocess
import re

def ping_at(hostname):
    self_IP = hostname

    if platform == "linux" or platform == "darwin" or platform == "ubuntu":
        command=['ping', '-c', '4', self_IP]
        timeout=10
        proc=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        proc.wait()

    else:
        command=["ping", "-n", "4", self_IP]
        timeout=10
        proc=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    try:
        [out, err]=proc.communicate(timeout=timeout)
        if proc.returncode == 0:
            if platform == "linux" or platform == "darwin" or platform == "ubuntu":
                # rtt min/avg/max/mdev = 578.263/917.875/1013.707/132.095 ms
                print("içerideyim")
                print("out",out)
                try:
                    minimum=re.search("rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)", str(out)).group(1)
                    maximum=re.search("rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)", str(out)).group(2)
                    avarage=re.search("rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)", str(out)).group(3)
                    packetlost= re.search("(\d*[\.|\,]?\d+)%",str(out)).group(1)
                except AttributeError:
                    print('Ping atılamadı')
                    minimum="Null"
                    maximum="Null"
                    avarage="Null"
                    packetlost=100
            else:
                print("Windowstaki output", out)
                try:
                    # Approximate round trip times in milli-seconds: Minimum = 63ms, Maximum = 64ms, Average = 63ms
                    avgRTT=re.search("Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)", str(out))
                    minimum=re.search("Minimum = (\d+)",str(out))
                    maximum=re.search("Maximum = (\d+)",str(out))
                    avarage=re.search("Average = (\d+)",str(out))
                    packetlost= re.search("(\d*[\.|\,]?\d+)%",str(out))

                    # Organized for only number outputs
                    minimum = minimum.group().split("=")[1]
                    maximum = maximum.group().split("=")[1]
                    avarage = avarage.group().split("=")[1]
                    packetlost = packetlost.group().replace('%','')
                except:
                    print("Windows ping bir sorun var")
                    minimum="Null"
                    maximum="Null"
                    avarage="Null"
                    packetlost=100
    except subprocess.TimeoutExpired:
        proc.kill()
    return(packetlost,minimum,maximum,avarage)
