FROM python:3.8-slim-bullseye

COPY pages /workspace/pages
COPY utils /workspace/utils
COPY routes /workspace/routes
COPY 0-🏠-Home.py /workspace/0-🏠-Home.py
COPY configs.yaml /workspace/configs.yaml
COPY requirements.txt /workspace/requirements.txt

RUN apt update
RUN apt upgrade

WORKDIR /workspace

RUN python -m pip install -U pip setuptools
RUN pip install -r requirements.txt

EXPOSE 80 

ENTRYPOINT [ "streamlit", "run", "0-🏠-Home.py" ]