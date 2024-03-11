# Server
Server side was built with **Flask** and **Pytorch**.

## 1. Configuration
*1. Create environment*
```
# Create environments
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