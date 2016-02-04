#!/usr/bin/python
import sys
import json
import subprocess

# Group
group = "Server availability"

# Description of metrics
description = "Check remote service availability"

# Hosts to check
hosts = {
    # "{{name of the host}}": { "host": "{{hostname/ip address}}", "port": {{port}} },
    # ex "google dns": { "host": "8.8.8.8", "port": 53 },
    "google dns": { "host": "8.8.8.8", "port": 53 },
    "coscale api": { "host": "37.187.86.75", "port": 80 },
    "coscale dns": { "host": "37.187.86.75", "port": 53 }, # No service is running here
}

#
# DONT CHANGE ANYTHING BELOW THIS LINE
#
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
            "unit": "",
            "tags": "",
            "calctype": "Instant"
        })
        counter += 1

    print json.dumps({
        "maxruntime": 50000,
        "metrics": metrics
    })

def data():
    datapoints = {}
    counter = 0;
    for host in hosts:
        pingtime = subprocess.check_output("nc -w 1 %s %s && echo $? || echo $?" % (hosts[host]["host"], hosts[host]["port"]), shell=True)
        datapoints[counter] = pingtime.rstrip()
        counter += 1

    for line in datapoints:
        print "M%s %s" % (line, datapoints[line])

if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()

    if sys.argv[1] == '-d':
        data()
