FROM ubuntu:20.10
RUN apt update -y
RUN apt install -y git python3-pip curl
RUN python3 -m pip install --upgrade pip
RUN mkdir /io
COPY . /io
RUN python3 -m pip install /io[test]
WORKDIR /io
RUN bash
