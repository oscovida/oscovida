  FROM ubuntu:20.04

  RUN apt update -y
  RUN apt install -y git python3-pip curl
  RUN python3 -m pip install --upgrade pip pytest-cov pycodestyle pandas matplotlib seaborn joblib

  RUN mkdir /io
  # COPY . /io
  WORKDIR /io
  RUN bash
