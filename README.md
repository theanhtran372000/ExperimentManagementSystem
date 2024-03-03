# ExperimentManagementSystem
System for manage ML/DL processes as a blackbox.

```
# Create environments
python -m venv venv
source venv/bin/activate
python -m pip install -U pip setuptools

# Install Pytorch
pip install torch===1.11.0+cu115 torchvision===0.12.0 torchaudio===0.11.0 -f https://download.pytorch.org/whl/torch_stable.html

# Install requirements
pip install -r requirements.txt
```