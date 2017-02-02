#!/usr/bin/python

# 
# Generic script to check the response of a web request
#

import sys
import json
import subprocess
from threading import Thread
import datetime
import httplib
from urlparse import urlparse

# Group
group = "HTTP check"

# Description of metrics
description = "Check remote webservice availability"

# Hosts to check
hosts = {
    # "{{Name of host}}": {{host}},
    # ex "HTTPS days left - google.be": "google.be",
    "HTTP status - google.be": "http://www.google.be",
    "HTTP status - coscale": "http://www.coscale.com/contact",
    "HTTP status - microsoft": "https://www.microsoft.com/en-us/about",
}

#
# DONT CHANGE ANYTHING BELOW THIS LINE
#

def execute(metricId, url):
    parse = urlparse(url)
    host = parse.hostname
    path = parse.path

    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        status = conn.getresponse().status
    except StandardError:
        status = -1

    sys.stdout.write("M%s %s\n" % (metricId, status))

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
        "maxruntime": 5000,
        "period": 3600, # Check every hour
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
