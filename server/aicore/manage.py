import os
import yaml
import pathlib

from utils.common import *


class StatusManager:
    def __init__(self, exp_dir):
        self.exp_dir = exp_dir
        self.status_path = os.path.join(self.exp_dir, 'status.yaml')
        
        pathlib.Path(self.exp_dir).mkdir(parents=True, exist_ok=True)
    
    
    def __call__(self):
        data = self.read()
        return data['run']['status']
    
    
    def read(self):
        with open(self.status_path, 'r') as f:
            data = yaml.full_load(f)
        return data
    
    
    def write(self, data):
        with open(self.status_path, 'w') as f:
            yaml.dump(data, f)        
    
     
    def create(self):
        
        data = {}
        data['run'] = {}
        data['run']['status'] = 'create'
        data['run']['create'] = get_current_timestring()
        
        self.write(data)
    
        
    def train(self):
        
        data = self.read()
        
        data['run']['status'] = 'train'
        data['run']['start'] = get_current_timestring()
        
        self.write(data)
    
        
    def update(self, epoch, loss):
        
        data = self.read()
        
        data['run']['curr_epoch'] = epoch
        data['run']['best_lost'] = loss
        
        self.write(data)
        
    
    def eval(self):
        
        data = self.read()
        
        data['run']['status'] = 'eval'
        data['run']['end'] = get_current_timestring()
        data['run']['dur'] = calculate_duration(
            data['run']['start'],
            data['run']['end']
        ).total_seconds()
        
        self.write(data)
    
     
    def done(self, train_result, valid_result):
        
        data = self.read()
        
        data['run']['status'] = 'done'

        data['result'] = {}
        data['result']['train'] = train_result
        data['result']['valid'] = valid_result
        
        self.write(data)
        