FROM python:3.10-slim

COPY aicore /workspace/aicore
COPY configs /workspace/configs
COPY routes /workspace/routes
COPY utils /workspace/utils
COPY app.py /workspace/app.py
COPY requirements.txt /workspace/requirements.txt

WORKDIR /workspace

RUN python -m pip install -U pip setuptools
RUN pip install -r requirements.txt
RUN pip install torch===1.11.0+cpu torchvision===0.12.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

EXPOSE 3720 

ENTRYPOINT [ "python", "app.py" ]