import random
import numpy as np
import torch

from .experiment import *

def seed(random_seed):
    # Fix the random seed for the random module
    random.seed(random_seed)

    # Fix the random seed for NumPy
    np.random.seed(random_seed)

    # Fix the random seed for PyTorch
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed(random_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False