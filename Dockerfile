FROM python:3.8

RUN apt-get update && apt-get install openssl 

COPY . ./scripts
WORKDIR /scripts
RUN python setup.py install
RUN pip install paramiko && openssl genrsa -out server.key 4096

ENTRYPOINT ["python"]
CMD ["/scripts/example/fake_ssh_server.py"]
