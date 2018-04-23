#!/bin/bash

if [ "$1" == "-c" ]; then
    echo -n '{'
    echo -n '"maxruntime":10000,'
    echo -n '"period":60,'
    echo -n '"metrics":['
    echo -n '{"id":1,"datatype":"DOUBLE","name":"RDP uptime","description":"RDP uptime","groups":"RDP","unit":"%","tags":"","calctype":"Instant"}';
    echo ']}';
else
    if timeout 5 xfreerdp /cert-ignore /authonly /u:$RDP_USERNAME /p:$RDP_PASSWORD /v:$RDP_HOST:$RDP_PORT 1>/dev/null 2>&1; then
        echo "M1 100"
    else
        echo "M1 0"
    fi
fi
