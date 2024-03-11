# Client
Client side was built with **[Streamlit](https://streamlit.io/)**.

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
```

## 2. Docker deployment
Docker deployment here.
1. Pre-built image is located on **my Docker Hub** with tag `theanhtran/ems-client:v1.0.0`. You cal also re-build image with following command.
```
cd client
docker build -t <image-tag> .
```
2. Run image with following commands
```
docker run -p 80:80 -e HOST=<server-host> <image-tag>
```
3. After successfully running, the app will be available at `localhost:80`.