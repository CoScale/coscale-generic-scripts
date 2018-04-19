#!/bin/bash

# Script to push status of enabled SystemD services to CoScale
# Service value running 1, other 0

for i in "$@"
do
    case $i in
        -c)
        # Configuration mode: return the custom metrics data should be defined

        echo -n '{';
        echo -n '"maxruntime":1000,'
        echo -n '"period": 60,'

        echo -n '"metrics":['

        # Add services metrics definition
        COUNTER=1
        for SERVICE in `systemctl list-unit-files | grep enabled | awk '{print $1}'`; do
            echo -n "{\"id\": ${COUNTER}, \"datatype\":\"DOUBLE\", \"name\":\"${SERVICE}\", \"description\":\"Status of ${SERVICE}\", \"groups\":\"SystemD\", \"unit\":\"\", \"tags\":\"\", \"calctype\":\"Instant\"},";
            COUNTER=$((COUNTER+1))
        done

        # Push metric with total number of services enabled
        echo -n '{"id":0, "datatype":"DOUBLE", "name":"Total number of enabled SystemD services", "description":"", "groups":"SystemD", "unit":"", "tags":"", "calctype":"Instant"}';

        echo ']}';
        ;;

        -d)
        # Data retrieval mode: return the data for the custom metrics

        # Total number of services enabled
        echo "M0 $(systemctl list-unit-files | grep enabled | wc -l)"

        # Status per service
        COUNTER=1
        SERVICES=$(systemctl list-unit-files | grep enabled | awk '{print $1}')
        for SERVICE in `systemctl list-unit-files | grep enabled | awk '{print $1}'`; do
            echo "M${COUNTER} $(systemctl | grep ${SERVICE} | grep "running\|listening" | wc -l)"
            COUNTER=$((COUNTER+1))
        done
        ;;
    esac
done
