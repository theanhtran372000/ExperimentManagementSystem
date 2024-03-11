FROM python:3.10-slim

COPY pages /workspace/pages
COPY utils /workspace/utils
COPY .streamlit /workspace/.streamlit
COPY 0-🏠-Home.py /workspace/0-🏠-Home.py
COPY requirements.txt /workspace/requirements.txt

WORKDIR /workspace

RUN python -m pip install -U pip setuptools
RUN pip install -r requirements.txt

EXPOSE 80 

ENTRYPOINT [ "streamlit", "run", "0-🏠-Home.py" ]