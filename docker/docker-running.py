#!/usr/bin/python

# 
# Generic script to check how many containers are running for a certain image
#
import sys
import json
import subprocess

#
# Image list - Add any image you want to monitor to the array below
#
images = [
    "nginx",
    "busybox"
]

# Configuration mode: return the custom metrics data should be defined
def config():
    metrics = []
    for key, image in enumerate(images):   
        metrics.append({
            "id": key,
            "datatype": "DOUBLE",
            "name": "Containers running for {}".format(image),
            "description": "Number of running container for {}".format(image),
            "groups": "Docker running",
            "unit": "",
            "tags": "",
            "calctype": "Instant"
        })

    settings = {
        "maxruntime": 30000,  # How long the script is allowed to run
        "period": 60,  # The period the script will run, in this case it will run every 60 seconds
        "metrics": metrics
    }

    print json.dumps(settings)

# Data retrieval mode: return the data for the custom metrics
def data():
    # Get running container images
    running = subprocess.check_output('docker ps --format "{{.Image}}"', shell=True, stderr=subprocess.STDOUT)
    
    # Prepare dict from images array
    data = {}
    for key, image in enumerate(images):
        data[image] = {
            'id': key,
            'count': 0
        }

    # Parse information from running command and match it with images we need to monitor
    for image in running.split():
        if image in data:
            data[image]['count'] += 1

    # Print output information
    for image in data:
        print "M{} {}".format(data[image]['id'], data[image]['count'])

# Switch to check in which mode the script is running
if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()
    if sys.argv[1] == '-d':
        data()
