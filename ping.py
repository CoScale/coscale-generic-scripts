#!/usr/bin/python
import sys
import json
import subprocess

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
        "maxruntime": 50000,
        "metrics": metrics
    })

def data():
    datapoints = {}
    counter = 0;
    for host in hosts:
        pingtime = subprocess.check_output("ping -c %s %s | tail -1 | awk '{print $4}' | cut -d '/' -f 2" % (count, hosts[host]), shell=True)
        datapoints[counter] = pingtime.rstrip()
        counter += 1

    for line in datapoints:
        print "M%s %s" % (line, datapoints[line])

if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()

    if sys.argv[1] == '-d':
        data()
