#!/usr/bin/env python

# Generic script to check if certain directories exist, are accessable and not empty.

import argparse
import json
import random
import subprocess
import time
#------------------------------------------------------------------------------
directories = [
    '/test-unexisting/',
    '/tmp/'
]
#------------------------------------------------------------------------------
# Configuration mode: return the custom metrics data should be defined
def config():
    settings = {
        'maxruntime': 20000,  # How long the script is allowed to run
        'period': 60,  # The period the script will run, in this case it will run every 60 seconds
        'metrics': []
    }

    counter = 0
    for directory in directories:
        settings['metrics'].append({
            'id': counter,
            'datatype': 'DOUBLE',
            'name': 'NFS Available - {0}'.format(directory),
            'description': '100% if the directory exists and has files',
            'groups': 'NFS Availability',
            'unit': '',
            'tags': '',
            'calctype': 'Instant'
        })

        counter += 1

    print json.dumps(settings, indent=4)

# Data retrieval mode: return the data for the custom metrics
def data():
    counter = 0

    for directory in directories:
        (success, time) = run(['ls {0}'.format(directory)])
        print 'M{0} {1}'.format(counter, success)

        counter += 1

def run(command):
    success = 100
    result = ''
    start = time.time()
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as grepexc:
        success = 0
    end = (time.time() - start) * 1000

    # Check output
    if result == '':
        success = 0

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
