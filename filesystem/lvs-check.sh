#!/bin/bash

if [ "$1" == "-c" ]; then
    echo '{"maxruntime":5000,"metrics":[{"name":"Logical Volume Size","groups":"LVS","tags":"","datatype":"DOUBLE","calctype":"Instant","id":0,"unit":"b","description":"The size of a LVS logical volume","dimensions":[{"id":1,"name":"Volume Group"},{"id":2,"name":"Logical Volume"}]},{"name":"Logical Volume Data%","groups":"LVS","tags":"","datatype":"DOUBLE","calctype":"Instant","id":1,"unit":"%","description":"The percentage of data the volume consumes","dimensions":[{"id":1,"name":"Volume Group"},{"id":2,"name":"Logical Volume"}]},{"name":"Logical Volume MetaData%","groups":"LVS","tags":"","datatype":"DOUBLE","calctype":"Instant","id":2,"unit":"%","description":"The percentage of metadata space the volume consumes","dimensions":[{"id":1,"name":"Volume Group"},{"id":2,"name":"Logical Volume"}]}],"period":60}'
else

    lvs -o lv_full_name,lv_size,data_percent,metadata_percent --units b --separator " " | tail -n+2 | while read -r LINE || [[ -n "$LINE" ]]; do
        VG=$(echo $LINE | awk '{ print $1; }' | awk -F/ '{ print $1; }')
        LV=$(echo $LINE | awk '{ print $1; }' | awk -F/ '{ print $2; }')
        SIZE=$(echo $LINE | awk '{ print $2; }' | sed 's/B//')
        DATA=$(echo $LINE | awk '{ print $3; }')
        METADATA=$(echo $LINE | awk '{ print $4; }')

        if [ "x$DATA" != "x" ]; then
            echo "M0 \"1:$VG,2:$LV\" $SIZE"
            echo "M1 \"1:$VG,2:$LV\" $DATA"
            echo "M2 \"1:$VG,2:$LV\" $METADATA"
        fi
    done

fi
