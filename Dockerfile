FROM registry.access.redhat.com/ubi8/ubi-minimal:8.6-751.1655117800

LABEL maintainer="Manoj Jahgirdar <manoj.jahgirdar@in.ibm.com>"

RUN microdnf update
RUN microdnf install python3.9 -y
RUN microdnf install gcc gcc-c++ make -y

WORKDIR /app

ADD . /app

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install wheel

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install torch==1.8.0 --no-cache-dir

EXPOSE 8080

CMD ["python3", "-u", "app.py"]
