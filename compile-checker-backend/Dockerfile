FROM ubuntu:18.04

RUN rm -rf /var/lib/apt/lists/*
RUN apt-get -yq update && apt-get -yq install apt-transport-https software-properties-common wget curl build-essential
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -yq update && apt-get -yq install python3.8 python3.8-dev python3.8-distutils
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py

COPY requirements.txt /root/requirements.txt
RUN python3.8 -m pip install -r /root/requirements.txt
RUN python3.8 -m pip install awslambdaric

RUN mkdir /usr/src/app
COPY handler.py /usr/src/app/handler.py
WORKDIR /usr/src/app

COPY secret.py /usr/src/app/secret.py

# RUN chmod +x /python3.8/bin/python3.8
ENTRYPOINT [ "python3.8", "-m", "awslambdaric" ]
CMD ["handler.hello"]