import os

def exp_exists(exp_id, exp_dir):
    if os.path.exists(exp_dir):
        return exp_id in os.listdir(exp_dir)
    else:
        return False