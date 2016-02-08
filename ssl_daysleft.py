#!/usr/bin/python
import sys
import json
import subprocess
from dateutil.parser import parse
from datetime import date
from threading import Thread

# Group
group = "SSL check"

# Description of metrics
description = "Checks how many days are left for HTTPS/SSL certs"

# Hosts to check
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
def execute(metricId, host):
    output = subprocess.check_output("echo | openssl s_client -connect %s:443 2>/dev/null | openssl x509 -noout -dates | grep notAfter" % host, shell=True)

    # Extract exp date from output
    expdate = parse(output.rstrip().split("=")[1]).date()

    # Calculate amount of days left
    today = date.today()
    difference = expdate - today

    sys.stdout.write("M%s %s\n" % (metricId, difference.days))

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
    for host in hosts:
        Thread(target = execute, args = (counter, hosts[host], )).start()

        counter += 1

if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()

    if sys.argv[1] == '-d':
        data()
