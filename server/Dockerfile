FROM python:3.8-slim-bullseye

COPY aicore /workspace/aicore
COPY configs /workspace/configs
COPY routes /workspace/routes
COPY utils /workspace/utils
COPY app.py /workspace/app.py

RUN apt update
RUN apt upgrade

WORKDIR /workspace

RUN python -m pip install -U pip setuptools
RUN pip install -r requirements.txt

EXPOSE 3720 

ENTRYPOINT [ "python", "app.py" ]