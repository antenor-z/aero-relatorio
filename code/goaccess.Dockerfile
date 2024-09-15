FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y goaccess && \
    rm -rf /var/lib/apt/lists/*

RUN echo '#!/bin/bash\n\
while true; do\n\
  goaccess /var/log/nginx/nginx-access.log -o /var/log/goaccess/report.html --log-format=COMBINED\n\
  sleep 180\n\
done' > /usr/local/bin/run-goaccess.sh

RUN chmod +x /usr/local/bin/run-goaccess.sh

CMD ["/usr/local/bin/run-goaccess.sh"]