#!/usr/bin/env python

import argparse
import json
import random
import time
#------------------------------------------------------------------------------
# Configuration mode: return the custom metrics data should be defined
def config():
    settings = {
        'maxruntime': 5000,  # How long the script is allowed to run
        'period': 60,  # The period the script will run, in this case it will run every 60 seconds
        'metrics': [
            {
                'id': 1,
                'datatype': 'DOUBLE',
                'name': 'Random number',
                'description': 'Random number from 1 to 100',
                'groups': 'Statistics',
                'unit': 'ms',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 2,
                'datatype': 'DOUBLE',
                'name': 'Server time',
                'description': 'Current time in hours',
                'groups': 'Time',
                'unit': 'hours',
                'tags': '',
                'calctype': 'Instant'
            },
            {
                'id': 3,
                'datatype': 'DOUBLE',
                'name': 'Server time',
                'description': 'Current time in minutes',
                'groups': 'Time',
                'unit': 'minutes',
                'tags': '',
                'calctype': 'Instant'
            }
        ]
    }

    print json.dumps(settings, indent=4)

# Data retrieval mode: return the data for the custom metrics
def data():
    print 'M1 {0}'.format(random.randint(1, 100))
    print 'M2 {0}'.format(time.strftime('%H'))
    print 'M3 {0}'.format(time.strftime('%M'))
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
