#!/usr/bin/python
import sys
import json
import subprocess
from threading import Thread
import datetime


# Group
group = "HTTPS check"

# Description of metrics
description = "Check remote service availability"

# Hosts to check
hosts = {
    # "{{Name of host}}": {{host}},
    # ex "HTTPS days left - google.be": "google.be",
    "HTTPS days left - google.be": "google.be",
    "HTTPS days left - coscale": "coscale.com",
    "HTTPS days left - microsoft": "microsoft.com",
}

#
# DONT CHANGE ANYTHING BELOW THIS LINE
#

def execute(metricId, host):
    try:
        output = subprocess.check_output("echo | openssl s_client -showcerts -servername %s -connect %s:443 2>/dev/null | openssl x509 -noout -dates 2>/dev/null" % (host, host), shell=True)
        notAfter = output.split("\n")[1].split("=")[1]
        days = (datetime.datetime.strptime(notAfter, "%b %d %H:%M:%S %Y %Z") - datetime.datetime.today()).days
    except subprocess.CalledProcessError as e:
        days = -1

    sys.stdout.write("M%s %s\n" % (metricId, days))

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
            "unit": "days",
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
        threads[counter] = Thread(target = execute, args = (counter, hosts[host], ))
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
