#!/usr/bin/env python

# 
# Generic script to import metrics from Dropwizard
#

import argparse
import json
import socket
import sys
import time
import urllib2

from threading import Thread
#------------------------------------------------------------------------------
DROPWIZARD_ADMIN_URL='http://localhost:8001'
TENACITY_URL='http://localhost:8000/tenacity'

TENACITY_METRICS = ['countBadRequests', 'countCollapsedRequests', 'countEmit', 'countExceptionsThrown', 'countFailure', 'countFallbackEmit', 'countFallbackFailure', 'countFallbackMissing', 'countFallbackRejection', 'countFallbackSuccess', 'countResponsesFromCache', 'countSemaphoreRejected', 'countShortCircuited', 'countSuccess', 'countThreadPoolRejected', 'countTimeout', 'latencyTotal_mean']
#------------------------------------------------------------------------------
def config():
	global TENACITY_METRICS

	metrics = [
		create_metric(1, 'Ping uptime', unit='%'),
		create_metric(2, 'Ping latency', unit='ms'),
		create_metric(3, 'Healthcheck uptime', unit='%', dimensions=['Healthcheck']),
		create_metric(4, 'Circuitbreaker uptime', unit='%', dimensions=['Key']),
		create_metric(5, 'JVM Heap committed', unit='b'),
		create_metric(6, 'JVM Heap init', unit='b'),
		create_metric(7, 'JVM Heap max', unit='b'),
		create_metric(8, 'JVM Heap used', unit='b'),
		create_metric(9, 'JVM Thread count', unit=''),
		create_metric(10, 'JVM Daemon thread count', unit=''),
	]

	for tmetric in TENACITY_METRICS:
		metrics.append(create_metric(len(metrics) + 1, 'Hystrix ' + tmetric, unit='', dimensions=['Key']))

	print json.dumps({
		'maxruntime': 1000,
		'period': 60,
		'metrics' : metrics
	}, indent=4)


def create_metric(metric_id, name, unit='', description='', datatype='DOUBLE', groups='Dropwizard', tags='', calctype='Instant', dimensions=[]):
	return {
		'id': metric_id,
		'name': 'Dropwizard ' + name,
		'description': description,
		'datatype': datatype,
		'unit': unit,
		'groups': groups,
		'tags': tags,
		'calctype': calctype,
		'dimensions': [{'id':i+1, 'name':dimensions[i]} for i in range(len(dimensions))]
	}


def data():
	global DROPWIZARD_ADMIN_URL, TENACITY_URL, TENACITY_METRICS

	responses = {}
	threads = []

	threads.append(do_request(DROPWIZARD_ADMIN_URL + '/ping', responses, 'ping', json_response=False))
	threads.append(do_request(DROPWIZARD_ADMIN_URL + '/healthcheck', responses, 'healthcheck'))
	threads.append(do_request(TENACITY_URL + '/circuitbreakers', responses, 'circuitbreakers'))
	threads.append(do_request(DROPWIZARD_ADMIN_URL + '/metrics', responses, 'metrics'))

	[t.join() for t in threads]

	print_metric(1, [], 100 if responses['ping'] is not None else 0)
	print_metric(2, [], responses['ping-latency'])

	if responses['healthcheck'] is not None:
		for healthcheck in responses['healthcheck'].keys():
			print_metric(3, [healthcheck], 100 if responses['healthcheck'][healthcheck]['healthy'] is True else 0)

	if responses['circuitbreakers'] is not None:
		for cb in responses['circuitbreakers']:
			print_metric(4, [cb['id']], 100 if cb['open'] is True else 0)

	if responses['metrics'] is not None:
		if 'gauges' in responses['metrics']:
			gauges = responses['metrics']['gauges']
			print_gauge(5, [], gauges, 'jvm.memory.heap.committed')
			print_gauge(6, [], gauges, 'jvm.memory.heap.init')
			print_gauge(7, [], gauges, 'jvm.memory.heap.max')
			print_gauge(8, [], gauges, 'jvm.memory.heap.used')
			print_gauge(9, [], gauges, 'jvm.threads.count')
			print_gauge(10, [], gauges, 'jvm.threads.daemon.count')

			for gauge in gauges.keys():
				if gauge.startswith('TENACITY'):
					parts = gauge.split('.')
					if len(parts) == 3:
						(key, metric_name) = (parts[1], parts[2])

						if metric_name in TENACITY_METRICS:
							index = TENACITY_METRICS.index(metric_name)
							print_gauge(11 + index, [key], gauges, gauge)


def print_metric(metric_id, dimension_values, value):
	dims = ','.join(['%d:%s' % (i+1, dimension_values[i]) for i in range(len(dimension_values))])
	print 'M{0} "{1}" {2}' % (metric_id, dims, value)

def print_gauge(metric_id, dimension_values, dict, key):
	if key in dict:
		print_metric(metric_id, dimension_values, dict[key]['value'])


def do_request(url, response_dict, response_key, json_response=True, timeout=2):
	socket.setdefaulttimeout(timeout)

	def request():
		try:
			start = time.time()
			response = urllib2.urlopen(url, timeout=timeout)
			content = response.read()
			stop = time.time()
			value = json.loads(content) if json_response else content
			latency = (stop - start) * 1000
		except urllib2.HTTPError as e:
			# Circuitbreaker returns 500 when circuit is closed. Still process the data.
			content = e.read()
			stop = time.time()
			value = json.loads(content) if json_response else content
			latency = (stop - start) * 1000
		except:
			(value, latency) = (None, 0)
		finally:
			response_dict[response_key] = value
			response_dict[response_key + '-latency'] = latency

	thread = Thread(target=request)
	thread.start()
	return thread
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
