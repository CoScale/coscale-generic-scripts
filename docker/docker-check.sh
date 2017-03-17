#!/bin/sh

if [ "$1" == "-c" ]; then
    echo '{"maxruntime": 30000, "metrics": [{"name": "Uptime total", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 0, "unit": "", "description": "100% if commands succeed"}, {"name": "Runtime total", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 1, "unit": "ms", "description": "Total runtime of Docker test"}, {"name": "Uptime pull", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 2, "unit": "", "description": "100% if pull command succeeds"}, {"name": "Runtime pull", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 3, "unit": "ms", "description": "Pull runtime of Docker test"}, {"name": "Uptime run", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 4, "unit": "", "description": "100% if run command succeeds"}, {"name": "Runtime run", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 5, "unit": "ms", "description": "Run runtime of Docker test"}, {"name": "Uptime stop", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 6, "unit": "", "description": "100% if stop command succeeds"}, {"name": "Runtime stop", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 7, "unit": "ms", "description": "Stop runtime of Docker test"}, {"name": "Uptime remove", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 8, "unit": "", "description": "100% if remove command succeeds"}, {"name": "Runtime remove", "groups": "Docker Test", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 9, "unit": "ms", "description": "Remove runtime of Docker test"}], "period": 60}'
else

    TOTAL_TIME=0
    TOTAL_EXIT=0
    
    # Pull
    COMMAND_START=$(date +%s)
    docker pull busybox > /dev/null 2> /dev/null
    EXIT=$?
    TOTAL_EXIT=$(($TOTAL_EXIT + $EXIT))
    COMMAND_STOP=$(date +%s)
    COMMAND_TOTAL=$(($COMMAND_STOP-$COMMAND_START))
    TOTAL_TIME=$(($TOTAL_TIME + $COMMAND_TOTAL))
    if [ "$EXIT" == "0" ]; then
        EXIT=100
    else
        EXIT=0
    fi
    echo "M2 $COMMAND_TOTAL"
    echo "M3 $EXIT"

    # Pull
    COMMAND_START=$(date +%s)
    docker run --name coscale-test -d busybox > /dev/null 2> /dev/null
    EXIT=$?
    TOTAL_EXIT=$(($TOTAL_EXIT + $EXIT))
    COMMAND_STOP=$(date +%s)
    COMMAND_TOTAL=$(($COMMAND_STOP-$COMMAND_START))
    TOTAL_TIME=$(($TOTAL_TIME + $COMMAND_TOTAL))
    if [ "$EXIT" == "0" ]; then
        EXIT=100
    else
        EXIT=0
    fi
    echo "M4 $COMMAND_TOTAL"
    echo "M5 $EXIT"

    # Pull
    COMMAND_START=$(date +%s)
    docker stop coscale-test > /dev/null 2> /dev/null
    EXIT=$?
    TOTAL_EXIT=$(($TOTAL_EXIT + $EXIT))
    COMMAND_STOP=$(date +%s)
    COMMAND_TOTAL=$(($COMMAND_STOP-$COMMAND_START))
    TOTAL_TIME=$(($TOTAL_TIME + $COMMAND_TOTAL))
    if [ "$EXIT" == "0" ]; then
        EXIT=100
    else
        EXIT=0
    fi
    echo "M6 $COMMAND_TOTAL"
    echo "M7 $EXIT"

    # Pull
    COMMAND_START=$(date +%s)
    docker rm coscale-test > /dev/null 2> /dev/null
    EXIT=$?
    TOTAL_EXIT=$(($TOTAL_EXIT + $EXIT))
    COMMAND_STOP=$(date +%s)
    COMMAND_TOTAL=$(($COMMAND_STOP-$COMMAND_START))
    TOTAL_TIME=$(($TOTAL_TIME + $COMMAND_TOTAL))
    if [ "$EXIT" == "0" ]; then
        EXIT=100
    else
        EXIT=0
    fi
    echo "M8 $COMMAND_TOTAL"
    echo "M9 $EXIT"


    if [ "$TOTAL_EXIT" == "0" ]; then
        TOTAL_EXIT=100
    else
        TOTAL_EXIT=0
    fi
    echo "M0 $TOTAL_TIME"
    echo "M1 $TOTAL_EXIT"
fi
