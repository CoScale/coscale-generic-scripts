# Check remote RDP connection

This directory contains a Dockerfile to build a container that checks a remote RDP connection.

To build the container

    docker build -t rdp-health .

To run the container in the background

    docker run -d --restart unless-stopped --name rdp-health \
        -e RDP_USERNAME="user" \
        -e RDP_PASSWORD="pass" \
        -e RDP_HOST="host" \
        -e RDP_PORT=3389 \
        rdp-health

Install a CoScale agent as a Docker container to start monitoring the health of the RDP connection. This will give you a metric 'RDP uptime', this metric can be visualised in a line graph or an uptime widget.
