import os
import time
import yaml
import pprint
import pathlib
from loguru import logger

from .model import ConfiguredModel
from .trainer import Trainer


class Experiment:
    def __init__(self, exp_dir):
        
        self.exp_dir = exp_dir
        self.exp_id = os.path.basename(self.exp_dir)
        pathlib.Path(self.exp_dir).mkdir(parents=True, exist_ok=True)
        
        # Configs
        self.exp_config_path = os.path.join(self.exp_dir, 'configs.yaml')
        self.load_configs()
        logger.info('Experiment configs: \n{}'.format(pprint.pformat(self.configs)))
        
        # Build model
        logger.info('Building model...')
        start = time.time()
        self.model = ConfiguredModel(self.configs['model'])
        
        if not self.model.is_valid():
            raise Exception('Invalid model structure')
        logger.success('Done after {:.2f}s!'.format(time.time() - start))
        
        # Build trainer
        logger.info('Building trainer...')
        start = time.time()
        self.trainer = Trainer(
            self.model,
            self.configs['data'],
            self.configs['train'],
            self.exp_dir
        )
        logger.success('Done after {:.2f}s!'.format(time.time() - start))
    
    # Load configs
    def load_configs(self):
        with open(self.exp_config_path, 'r') as f:
            self.configs = yaml.full_load(f)
        
    # Start experiments
    def start(self):
        logger.info('Start experiment...')
        
        # Train model
        logger.info('Start training...')
        start = time.time()
        self.trainer.train()
        logger.success('Done after {:.2f}s!'.format(time.time() - start))
    
        # Evaluate model
        logger.info('Start evaluating on train set')
        start = time.time()
        self.trainer.eval(train=True)
        logger.success('Done after {:.2f}s!'.format(time.time() - start))
        
        logger.info('Start evaluating on valid set')
        start = time.time()
        self.trainer.eval(train=False)
        logger.success('Done after {:.2f}s!'.format(time.time() - start))
    
    # Try the whole training process
    def try_start(self):
        self.trainer.try_train()
        
if __name__ == '__main__':
    exp = Experiment(exp_dir='../save/exps/q0k5ozji3ro0')
    exp.start()