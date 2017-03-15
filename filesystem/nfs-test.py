#!/usr/bin/python

# 
# Generic script to check if certain directories exist, are accessable and not empty.
#

import sys
import json
import random
import time
import subprocess

directories = [
    "/test-unexisting/",
    "/tmp/"
]

# Configuration mode: return the custom metrics data should be defined
def config():
    settings = {
        "maxruntime": 20000,  # How long the script is allowed to run
        "period": 60,  # The period the script will run, in this case it will run every 60 seconds
        "metrics": []
    }

    counter = 0
    for directory in directories:
        settings['metrics'].append({
            "id": counter,
            "datatype": "DOUBLE",
            "name": "NFS Available - %s" % directory,
            "description": "Value of 1 if NFS is unavailable, 0 if available",
            "groups": "NFS Availability",
            "unit": "",
            "tags": "",
            "calctype": "Instant"
        })

        counter += 1

    print json.dumps(settings)

# Data retrieval mode: return the data for the custom metrics
def data():
    counter = 0

    for directory in directories:
        (success, time) = run(["ls %s" % directory])
        print "M%s %s" % (counter, success)

        counter += 1

def run(command):
    success = 0
    result = ''
    start = time.time()
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as grepexc:
        success = grepexc.returncode
    end = (time.time() - start) * 1000

    # Check output
    if result == '':
        success = 1

    return [success, end]

# Switch to check in which mode the script is running
if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()
    if sys.argv[1] == '-d':
        data()
