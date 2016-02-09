#!/usr/bin/python
import sys
import json
import subprocess
from threading import Thread


# Group
group = "Remote latency"

# Description of metrics
description = "Latency of remote hosts"

# Amount of times to ping each host
count = 3

# Hosts to ping
hosts = {
    # "{{name of the host}}": "{{hostname/ip}}",
    # ex "coscale": "coscale.com",
    "google": "google.com",
    "pingdom": "pingdom.com",
    "coscale": "app.coscale.com"
}

#
# DONT CHANGE ANYTHING BELOW THIS LINE
#
def execute(metricId, host, count):
    pingtime = subprocess.check_output("ping -c %s %s | tail -1 | awk '{print $4}' | cut -d '/' -f 2" % (count, host), shell=True)
    sys.stdout.write("M%s %s\n" % (metricId, pingtime.rstrip()))

def config():
    metrics = []
    counter = 0;
    for host in hosts:
        metrics.append({
            "id": counter,
            "datatype": "DOUBLE",
            "name": host,
            "description": description,
            "groups": group,
            "unit": "ms",
            "tags": "",
            "calctype": "Instant"
        })
        counter += 1

    print json.dumps({
        "maxruntime": 5000,
        "metrics": metrics
    })

def data():
    datapoints = {}
    counter = 0;
    threads = [None] * len(hosts)
    for host in hosts:
        threads[counter] = Thread(target = execute, args = (counter, hosts[host], count, ))
        threads[counter].start()

        counter += 1

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()

    if sys.argv[1] == '-d':
        data()
