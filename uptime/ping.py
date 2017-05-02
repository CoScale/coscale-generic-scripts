#!/usr/bin/env python

# 
# Generic script to get the latency to remote hosts
#

import argparse
import json
import subprocess
import sys

from threading import Thread
#------------------------------------------------------------------------------
# Group
group = 'Remote latency'

# Description of metrics
description = 'Latency of remote hosts'

# Amount of times to ping each host
count = 3

# Hosts to ping
hosts = {
    # '{{name of the host}}': '{{hostname/ip}}',
    # ex 'coscale': 'coscale.com',
    'google': 'google.com',
    'pingdom': 'pingdom.com',
    'coscale': 'app.coscale.com'
}
#------------------------------------------------------------------------------
#
# DONT CHANGE ANYTHING BELOW THIS LINE
#
#------------------------------------------------------------------------------
def execute(metricId, host, count):
    pingtime = subprocess.check_output('ping -c {0} {1} | tail -1 | awk "{{print $4}}" | cut -d "/" -f 6'.format(count, host), shell=True).rstrip()

    if pingtime == '':
        pingtime = 0

    sys.stdout.write('M{0} {1}\n'.format(metricId, pingtime))

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
            'unit': 'ms',
            'tags': '',
            'calctype': 'Instant'
        })
        counter += 1

    print json.dumps({
        'maxruntime': 5000,
        'metrics': metrics
    }, indent=4)

def data():
    datapoints = {}
    counter = 0;
    threads = [None] * len(hosts)
    for host in hosts:
        threads[counter] = Thread(target = execute, args = (counter, hosts[host], count, ))
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
