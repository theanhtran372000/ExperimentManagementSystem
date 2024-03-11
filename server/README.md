# Server
Server side was built with **[Flask](https://flask.palletsprojects.com/en/3.0.x/)** and **[Pytorch](https://pytorch.org/)**.

## 1. Configuration
*1. Create environment*
```
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate in Window
```

*2. Install requirements*
```
python -m pip install -U pip setuptools
pip install -r requirements.txt
pip install torch==1.9.0+cpu torchvision==0.10.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

## 2. Docker deployment
Docker deployment here.
1. Pre-built image is located on **my Docker Hub** with tag `theanhtran/ems-server:v1.0.0`. You cal also re-build image with following command.
```
cd client
docker build -t <image-tag> .
```
2. Run image with following commands
```
docker run -p 3720:3720 <image-tag>
```
That's it. Now you can import [server.json](./postman/server.json) into Postman and explore it.