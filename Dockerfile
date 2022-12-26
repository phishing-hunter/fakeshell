FROM python:3.8

RUN apt-get update && apt-get install openssl && \
    openssl genrsa -out /tmp/server.key 4096

COPY . ./scripts
WORKDIR /scripts
RUN python setup.py install
RUN pip install paramiko 

ENTRYPOINT ["python"]
CMD ["/scripts/example/fake_ssh_server.py"]
