#!/bin/sh

DIR=/mnt/nfs

if [ "$1" == "-c" ]; then
    echo '{"maxruntime": 5000, "metrics": [{"name": "NFS Available - '"$DIR"'", "groups": "NFS Availability", "tags": "", "datatype": "DOUBLE", "calctype": "Instant", "id": 0, "unit": "%", "description": "100% if the directory exists and has files"}], "period": 60}'
else

    AV=0
    if [ -e $DIR ]; then
        LINES=`ls $DIR 2>/dev/null | wc -l`
        if [ "$LINES" != "0" ]; then
            AV=100
        fi
    fi
    
    echo "M1 $AV"

fi
