#!/usr/bin/python
import sys
import json
import random
import time

# Configuration mode: return the custom metrics data should be defined
def config():
    settings = {
        "maxruntime": 5000,  # How long the script is allowed to run
        "period": 60,  # The period the script will run, in this case it will run every 60 seconds
        "metrics": [
            {
                "id": 0,
                "datatype": "DOUBLE",
                "name": "Random number",
                "description": "Random number from 1 to 100",
                "groups": "Statistics",
                "unit": "ms",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 1,
                "datatype": "DOUBLE",
                "name": "Server time",
                "description": "Current time in hours",
                "groups": "Time",
                "unit": "hours",
                "tags": "",
                "calctype": "Instant"
            },
            {
                "id": 2,
                "datatype": "DOUBLE",
                "name": "Server time",
                "description": "Current time in minutes",
                "groups": "Time",
                "unit": "minutes",
                "tags": "",
                "calctype": "Instant"
            }
        ]
    }

    print json.dumps(settings)

# Data retrieval mode: return the data for the custom metrics
def data():
    print "M1 %s" % random.randint(1, 100)
    print "M2 %s" % time.strftime("%H")
    print "M3 %s" % time.strftime("%M")

# Switch to check in which mode the script is running
if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()
    if sys.argv[1] == '-d':
        data()
