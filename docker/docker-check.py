#!/usr/bin/env python


# Generic script to pull the busy box image, run it, stop it and delete it to check Docker functionality
# For each of the steps an exitcode + latency is sent back, as well as a total latency.

import argparse
import json
import random
import subprocess
import time
#------------------------------------------------------------------------------
# Configuration mode: return the custom metrics data should be defined
def config():
    settings = {
        'maxruntime': 30000,  # How long the script is allowed to run
        'period': 60,  # The period the script will run, in this case it will run every 60 seconds
        'metrics': [
            {
                'id': 0,
                'datatype': 'DOUBLE',
                'name': 'Uptime total',
                'description': '100% if commands succeed',
                'groups': 'Docker Test',
                'unit': '',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 1,
                'datatype': 'DOUBLE',
                'name': 'Runtime total',
                'description': 'Total runtime of Docker test',
                'groups': 'Docker Test',
                'unit': 'ms',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 2,
                'datatype': 'DOUBLE',
                'name': 'Uptime pull',
                'description': '100% if pull command succeeds',
                'groups': 'Docker Test',
                'unit': '',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 3,
                'datatype': 'DOUBLE',
                'name': 'Runtime pull',
                'description': 'Pull runtime of Docker test',
                'groups': 'Docker Test',
                'unit': 'ms',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 4,
                'datatype': 'DOUBLE',
                'name': 'Uptime run',
                'description': '100% if run command succeeds',
                'groups': 'Docker Test',
                'unit': '',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 5,
                'datatype': 'DOUBLE',
                'name': 'Runtime run',
                'description': 'Run runtime of Docker test',
                'groups': 'Docker Test',
                'unit': 'ms',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 6,
                'datatype': 'DOUBLE',
                'name': 'Uptime stop',
                'description': '100% if stop command succeeds',
                'groups': 'Docker Test',
                'unit': '',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 7,
                'datatype': 'DOUBLE',
                'name': 'Runtime stop',
                'description': 'Stop runtime of Docker test',
                'groups': 'Docker Test',
                'unit': 'ms',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 8,
                'datatype': 'DOUBLE',
                'name': 'Uptime remove',
                'description': '100% if remove command succeeds',
                'groups': 'Docker Test',
                'unit': '',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 9,
                'datatype': 'DOUBLE',
                'name': 'Runtime remove',
                'description': 'Remove runtime of Docker test',
                'groups': 'Docker Test',
                'unit': 'ms',
                'tags': '',
                'calctype': 'Instant'
            }
        ]
    }

    print json.dumps(settings, indent=4)

# Data retrieval mode: return the data for the custom metrics
def data():
    # Success value
    result = 0

    # Total time spent
    total = 0

    metrics = [None] * 10

    # pull busybox
    (success, time) = run(['docker pull busybox'])
    result += success - 100
    total += time
    metrics[2] = 'M2 {0}'.format(success)
    metrics[3] = 'M3 {0:.2f}'.format(time)

    # run coscale-test container
    (success, time) = run(['docker run --name coscale-test -d busybox'])
    result += success - 100
    total += time
    metrics[4] = 'M4 {0}'.format(success)
    metrics[5] = 'M5 {0:.2f}'.format(time)

    # stop coscale-test container
    (success, time) = run(['docker stop coscale-test'])
    result += success - 100
    total += time
    metrics[6] = 'M6 {0}'.format(success)
    metrics[7] = 'M7 {0:.2f}'.format(time)

    # remove coscale-test
    (success, time) = run(['docker rm coscale-test'])
    result += success - 100
    total += time
    metrics[8] = 'M8 {0}'.format(success)
    metrics[9] = 'M9 {0:.2f}'.format(time)

    # Convert result to meaningfull value
    if result < 0:
        result = 0
    else:
        result = 100


    metrics[0] = 'M0 {0}'.format(result)
    metrics[1] = 'M1 {0:.2f}'.format(total)

    for metric in metrics:
        print metric

def run(command):
    success = 100
    start = time.time()
    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as grepexc:
        success = 0
    end = (time.time() - start) * 1000

    return [success, end]
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
