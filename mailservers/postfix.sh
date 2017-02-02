#!/bin/bash

#
# Generic Script for parsing your postfix logs.
#

for i in "$@"
do
    case $i in
        -c)
        # Configuration mode: return the custom metrics data should be defined.

        echo -n '{';
        # First we define how long the script is allowed to run, because the CoScale agent checks it every minute it is advised to not set this higher then 1000
        echo -n '"maxruntime":1000,'

        # Next we define the metrics we want the CoScale agent to fetch every minute
        echo -n '"metrics":['
        echo -n '{"id":1,"datatype":"DOUBLE","name":"Received mail","description":"The amount of emails currently received by postfix.","groups":"Postfix","unit":"emails","tags":"","calctype":"Instant"},';
        echo -n '{"id":2,"datatype":"DOUBLE","name":"Sent mail","description":"The amount of emails with status=sent.","groups":"Postfix","unit":"emails","tags":"","calctype":"Instant"}',;
        echo -n '{"id":3,"datatype":"DOUBLE","name":"Deferred mail","description":"The amount of emails with status=deferred.","groups":"Postfix","unit":"emails","tags":"","calctype":"Instant"}',;
        echo -n '{"id":4,"datatype":"DOUBLE","name":"Bounced mail","description":"The amount of emails with status=bounced.","groups":"Postfix","unit":"emails","tags":"","calctype":"Instant"}',;
        echo ']}';
        ;;

        -d)
        # Data retrieval mode: return the data for the custom metrics

        # The latest logs can be fetched using logtail (apt get install logtail) or dategrep (https://github.com/mdom/dategrep)

        logs=`logtail -f /var/log/mail.log -o mail.log.offset | grep "status"`
        # logs=`/bin/dategrep --format "%b %e %H:%M:%S" --from "1 minute ago" /var/log/mail.log | grep "status"`

        # Count the number of occurences in the logs.
        echo "M1 $(echo $logs | grep -o "status" | wc -l)"
        echo "M2 $(echo $logs | grep -o "sent" | wc -l)"
        echo "M3 $(echo $logs | grep -o "deferred" | wc -l)"
        echo "M4 $(echo $logs | grep -o "bounced" | wc -l)"
        ;;
    esac
done
