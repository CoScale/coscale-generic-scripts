#!/bin/bash
# Create events when a service is restarted (PID changed)

MATCH="/usr/sbin/apache2 -k start"
PID_FILE="/apache2.pid"

function getpid {
    ps --sort=pid auxf | grep "$MATCH" | grep -v grep | head -n 1 | awk '{ print $2; }'
}

case $1 in
    -c)
    # Configuration mode

    echo -n '{'
    echo -n '"maxruntime":1000,'
    echo -n '"period":60,'
    echo -n '"events":['
    echo -n '{"id":1,"name":"Apache restarts","description":"Restarts of the apache service","attributeDescriptions":[]}'
    echo ']}'
    ;;

    -d)

    PID=$(getpid)
    if [ -e $PID_FILE ]; then
        PREV=$(cat $PID_FILE)
        if [ "$PID" != "$PREV" ]; then
            echo 'E1 0 0 "Apache restarted" "{ }" S'
        fi
    fi

    echo $PID > $PID_FILE
    ;;
esac

