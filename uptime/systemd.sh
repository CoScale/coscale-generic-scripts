#!/bin/bash

# Script to push status of enabled SystemD services to CoScale

for i in "$@"
do
    case $i in
        -c)
        # Configuration mode: return the custom metrics data should be defined

        echo -n '{';
        echo -n '"maxruntime":20000,'
        echo -n '"period": 60,'

        echo -n '"metrics":['

        echo -n '{ "id": 0, "name": "Disabled state", "description": "Service is in disabled state", "groups": "SystemD/State", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 1, "name": "Enabled state", "description": "Service is in enabled state", "groups": "SystemD/State", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 2, "name": "Indirect state", "description": "Service is in indirect state", "groups": "SystemD/State", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 3, "name": "Masked state", "description": "Service is in masked state", "groups": "SystemD/State", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 4, "name": "Static state", "description": "Services in in static state", "groups": "SystemD/State", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'

        echo -n '{ "id": 5, "name": "Active substate", "description": "Service is in active substate", "groups": "SystemD/Substate", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 6, "name": "Elapsed substate", "description": "Service is in elapsed substate", "groups": "SystemD/Substate", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 7, "name": "Exited substate", "description": "Service is in exited substate", "groups": "SystemD/Substate", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 8, "name": "Listening substate", "description": "Service is in listening substate", "groups": "SystemD/Substate", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 9, "name": "Mounted substate", "description": "Services in in mounted substate", "groups": "SystemD/Substate", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 10, "name": "Running substate", "description": "Services in in running substate", "groups": "SystemD/Substate", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] },'
        echo -n '{ "id": 11, "name": "Waiting substate", "description": "Services in in waiting substate", "groups": "SystemD/Substate", "unit": "", "tags": "", "calctype": "Instant", "dimensions": [ {"id": 1, "name":"Service"} ] }'


        echo ']}';
        ;;

        -d)
        # Data retrieval mode: return the data for the custom metrics

        systemctl list-unit-files  --no-legend | while read line ; do
            SERVICE=$(echo $line | awk '{print $1}')
            STATE=$(echo $line | awk '{print $2}')
            SUBSTATE=$(systemctl | grep "$SERVICE" 2> /dev/null | awk '{print $4}')

            echo "M0 \"1:$SERVICE\" $(echo $STATE | grep disabled | wc -l)"
            echo "M1 \"1:$SERVICE\" $(echo $STATE | grep enabled | wc -l)"
            echo "M2 \"1:$SERVICE\" $(echo $STATE | grep indirect | wc -l)"
            echo "M3 \"1:$SERVICE\" $(echo $STATE | grep masked | wc -l)"
            echo "M4 \"1:$SERVICE\" $(echo $STATE | grep static | wc -l)"

            echo "M5 \"1:$SERVICE\" $(echo $SUBSTATE | grep active | wc -l)"
            echo "M6 \"1:$SERVICE\" $(echo $SUBSTATE | grep elapsed | wc -l)"
            echo "M7 \"1:$SERVICE\" $(echo $SUBSTATE | grep exited | wc -l)"
            echo "M8 \"1:$SERVICE\" $(echo $SUBSTATE | grep listening | wc -l)"
            echo "M9 \"1:$SERVICE\" $(echo $SUBSTATE | grep mounted | wc -l)"
            echo "M10 \"1:$SERVICE\" $(echo $SUBSTATE | grep running | wc -l)"
            echo "M11 \"1:$SERVICE\" $(echo $SUBSTATE | grep waiting | wc -l)"
        done

    esac
done
