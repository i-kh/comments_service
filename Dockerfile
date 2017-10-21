FROM python:3.6
ADD ./ /app
RUN apt-get update && apt-get install -y supervisor vim && \
    mkdir -p /var/log/comments/ && \
    mkdir -p /app/comments_service/logs  && \
    mkdir -p /app/comments_service/media  && \
    cp /app/docker/supervisor_comments.conf /etc/supervisor/conf.d/ && \
    cp /app/docker-entrypoint.sh /docker-entrypoint.sh && \
    pip3 install -r /app/requirements.txt

RUN chmod +x /docker-entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/docker-entrypoint.sh"]
