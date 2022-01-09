FROM python:3.9-alpine
ARG USER=gateway

RUN \
    adduser -D $USER && \
    mkdir /opt/graylog-alert-gateway \

COPY . /opt/graylog-alert-gateway/
RUN chown -R $USER:$USER /opt/graylog-alert-gateway

USER $USER
WORKDIR /opt/graylog-alert-gateway
RUN \
    pip3 install --no-cache-dir --upgrade pip --user && \
    pip3 install -r requirements.txt --user
CMD python3 launch.py




