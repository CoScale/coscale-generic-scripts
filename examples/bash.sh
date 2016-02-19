#!/bin/bash
# Custom metrics script

for i in "$@"
do
    case $i in
        -c)
        # Configuration mode: return the custom metrics data should be defined

        echo -n '{';
        # First we define how long the script is allowed to run, because the CoScale agent checks it every minute it is advised to not set this higher then 1000
        echo -n '"maxruntime":1000,'

        # Next we define the metrics we want the CoScale agent to fetch every minute
        echo -n '"metrics":['
        echo -n '{"id":1,"datatype":"DOUBLE","name":"Server response time","description":"","groups":"Statistics","unit":"ms","tags":"","calctype":"Instant"},';
        echo -n '{"id":2,"datatype":"DOUBLE","name":"Internet status","description":"","groups":"Network","unit":"","tags":"","calctype":"Instant"}',;
        echo -n '{"id":3,"datatype":"DOUBLE","name":"Server time","description":"","groups":"Network","unit":"minutes","tags":"","calctype":"Instant"}';
        echo ']}';
        ;;

        -d)
        # Data retrieval mode: return the data for the custom metrics

        # Example for getting average response time to external service
        echo "M1 $(ping -c 1 google.com | tail -1 | awk '{print $4}' | cut -d '/' -f 2)"

        # Example for checking if service is running with netcat
        echo "M2 $(nc -w 1 8.8.8.8 53 && echo $? || echo $?)"

        # Example for getting a value out of MySQL
        echo "M3 $(mysql -ss mysql -uroot -proot -e "SELECT MINUTE(NOW());")"
        ;;
    esac
done
