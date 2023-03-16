FROM ubuntu:latest

ARG NODE

RUN apt-get update && apt-get install -y --no-install-recommends \
    mc \
    python3-pip

COPY ./requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt
RUN rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/*

VOLUME /home/ubuntu/
WORKDIR /home/ubuntu/

ENTRYPOINT ["entrypoint.sh"]
