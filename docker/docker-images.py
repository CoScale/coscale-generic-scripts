#!/usr/bin/python

# 
# Generic script to check how many images exist on the host
#
import sys
import json
import subprocess

# Configuration mode: return the custom metrics data should be defined
def config():
    settings = {
        "maxruntime": 30000,  # How long the script is allowed to run
        "period": 60,  # The period the script will run, in this case it will run every 60 seconds
        "metrics": {
            "id": 0,
            "datatype": "DOUBLE",
            "name": "Number of Docker images",
            "description": "Number of Docker images available on host",
            "groups": "Docker images",
            "unit": "",
            "tags": "",
            "calctype": "Instant"
        }
    }

    print json.dumps(settings)

# Data retrieval mode: return the data for the custom metrics
def data():
    # Get running container images
    running = int(subprocess.check_output('docker images | wc -l', shell=True, stderr=subprocess.STDOUT)) - 1
    
    print "M0 {}".format(running)

# Switch to check in which mode the script is running
if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()
    if sys.argv[1] == '-d':
        data()
