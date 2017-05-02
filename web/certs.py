#!/usr/bin/env python

# 
# Generic script to get the days left to expire for https certs
#

import argparse
import datetime
import json
import subprocess
import sys

from threading import Thread
#------------------------------------------------------------------------------
# Group
group = 'HTTPS check'

# Description of metrics
description = 'Check validity of HTTPS certificates'

# Hosts to check
hosts = {
    # '{{Name of host}}': {{host}},
    # ex 'HTTPS days left - google.be': 'google.be',
    'HTTPS days left - google.be': 'google.be',
    'HTTPS days left - coscale': 'coscale.com',
    'HTTPS days left - microsoft': 'microsoft.com',
}
#------------------------------------------------------------------------------
#
# DONT CHANGE ANYTHING BELOW THIS LINE
#
#------------------------------------------------------------------------------
def execute(metricId, host):
    try:
        output = subprocess.check_output('echo | openssl s_client -showcerts -servername {0} -connect {1}:443 2>/dev/null | openssl x509 -noout -dates 2>/dev/null'.format(host, host), shell=True)
        notAfter = output.split('\n')[1].split('=')[1]
        days = (datetime.datetime.strptime(notAfter, '%b %d %H:%M:%S %Y %Z') - datetime.datetime.today()).days
    except subprocess.CalledProcessError as e:
        days = -1

    sys.stdout.write('M{0} {1}\n'.format(metricId, days))

def config():
    metrics = []
    counter = 0;
    for host in hosts:
        metrics.append({
            'id': counter,
            'datatype': 'DOUBLE',
            'name': host,
            'description': description,
            'groups': group,
            'unit': '',
            'tags': '',
            'calctype': 'Instant'
        })
        counter += 1

    print json.dumps({
        'maxruntime': 5000,
        'period': 3600, # Check every hour
        'metrics': metrics
    }, indent=4)

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
#------------------------------------------------------------------------------
# Switch to check in which mode the script is running
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='output a JSON object detailing the metrics this script collects')
    parser.add_argument('-d', action='store_true', help='output the metrics this script collects')
    args = parser.parse_args()

    if args.c:
        config()
    elif args.d:
        data()
