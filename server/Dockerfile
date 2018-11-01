# pull base image
FROM ubuntu:16.04

WORKDIR /root
RUN mkdir dstat_logs

# install
RUN \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get -y install python3 python3-dev virtualenv gcc dstat

# Add bootstrap executable
ADD files/dstat_server /root/dstat_server

WORKDIR /root
RUN \
  virtualenv -ppython3 venv && \
  venv/bin/pip install -r dstat_server/requirements.txt

# expose ports
EXPOSE 80

# start the cluster
WORKDIR /root
ENTRYPOINT ["/root/venv/bin/python3", "/root/dstat_server/dstat_starter.py"]
CMD []

