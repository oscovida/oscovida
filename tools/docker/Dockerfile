  FROM ubuntu:20.04
  RUN apt update -y
  RUN apt install -y git python3-pip curl
  RUN python3 -m pip install --upgrade pip
  COPY requirements.txt /tmp/requirements
  RUN python3 -m pip install -r /tmp/requirements
  RUN mkdir /io
  # COPY . /io
  WORKDIR /io
  RUN bash
