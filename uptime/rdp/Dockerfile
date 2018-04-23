FROM ubuntu:16.04

LABEL com.coscale.monitoring='[{"PluginType":"GENERICSCRIPT","Configuration":{"SCRIPT":["/rdp-check.sh"]}}]'

ENV DISPLAY=:0
COPY rdp-check.sh /rdp-check.sh

RUN apt-get update && apt-get install -y xvfb freerdp-x11

CMD [ "/usr/bin/Xvfb", ":0"]
