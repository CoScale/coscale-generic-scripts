#!/usr/bin/python

# 
# Generic script to pull the busy box image, run it, stop it and delete it to check Docker functionality
# For each of the steps an exitcode + latency is sent back, as well as a total latency.
#

import sys
import json
import random
import time
import subprocess

# Configuration mode: return the custom metrics data should be defined
def config():
    settings = {
        "maxruntime": 30000,  # How long the script is allowed to run
        "period": 60,  # The period the script will run, in this case it will run every 60 seconds
        "metrics": [
            {
                "id": 0,
                "datatype": "DOUBLE",
                "name": "Uptime total",
                "description": "100% if commands succeed",
                "groups": "Docker Test",
                "unit": "",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 1,
                "datatype": "DOUBLE",
                "name": "Runtime total",
                "description": "Total runtime of Docker test",
                "groups": "Docker Test",
                "unit": "ms",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 2,
                "datatype": "DOUBLE",
                "name": "Uptime pull",
                "description": "100% if pull command succeeds",
                "groups": "Docker Test",
                "unit": "",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 3,
                "datatype": "DOUBLE",
                "name": "Runtime pull",
                "description": "Pull runtime of Docker test",
                "groups": "Docker Test",
                "unit": "ms",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 4,
                "datatype": "DOUBLE",
                "name": "Uptime run",
                "description": "100% if run command succeeds",
                "groups": "Docker Test",
                "unit": "",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 5,
                "datatype": "DOUBLE",
                "name": "Runtime run",
                "description": "Run runtime of Docker test",
                "groups": "Docker Test",
                "unit": "ms",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 6,
                "datatype": "DOUBLE",
                "name": "Uptime stop",
                "description": "100% if stop command succeeds",
                "groups": "Docker Test",
                "unit": "",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 7,
                "datatype": "DOUBLE",
                "name": "Runtime stop",
                "description": "Stop runtime of Docker test",
                "groups": "Docker Test",
                "unit": "ms",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 8,
                "datatype": "DOUBLE",
                "name": "Uptime remove",
                "description": "100% if remove command succeeds",
                "groups": "Docker Test",
                "unit": "",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 9,
                "datatype": "DOUBLE",
                "name": "Runtime remove",
                "description": "Remove runtime of Docker test",
                "groups": "Docker Test",
                "unit": "ms",
                "tags": "",
                "calctype": "Instant"
            }
        ]
    }

    print json.dumps(settings)

# Data retrieval mode: return the data for the custom metrics
def data():
    # Success value
    result = 0

    # Total time spent
    total = 0

    (success, time) = run(["docker pull busybox"])
    result += success - 100
    total += time
    print "M2 %s" % success
    print "M3 %s" % time
    (success, time) = run(["docker run --name coscale-test -d busybox"])
    result += success - 100
    total += time
    print "M4 %s" % success
    print "M5 %s" % time
    (success, time) = run(["docker stop coscale-test"])
    result += success - 100
    total += time
    print "M6 %s" % success
    print "M7 %s" % time
    (success, time) = run(["docker rm coscale-test"])
    result += success - 100
    total += time
    print "M8 %s" % success
    print "M9 %s" % time

    # Convert result to meaningfull value
    if result < 0:
        result = 0
    else:
        result = 100


    print "M0 %s" % result
    print "M1 %s" % total

def run(command):
    success = 100
    start = time.time()
    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as grepexc:
        success = 0
    end = (time.time() - start) * 1000

    return [success, end]

# Switch to check in which mode the script is running
if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()
    if sys.argv[1] == '-d':
        data()
