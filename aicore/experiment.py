import time
import yaml
import pprint
from loguru import logger

from model import ConfiguredModel
from trainer import Trainer


class Experiment:
    def __init__(self, exp_config_path):
        # Configs
        self.exp_config_path = exp_config_path
        self.load_configs()
        logger.info('Experiment configs: \n{}'.format(pprint.pformat(self.configs)))
        
        # Build model
        logger.info('Building model...')
        start = time.time()
        self.model = ConfiguredModel(self.configs['model'])
        logger.success('Done after {:.2f}s!'.format(time.time() - start))
        
        # Build trainer
        logger.info('Building trainer...')
        start = time.time()
        self.trainer = Trainer(
            self.model,
            self.configs['data'],
            self.configs['train']
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
        logger.info('Start evaluating...')
        start = time.time()
        self.trainer.eval()
        logger.success('Done after {:.2f}s!'.format(time.time() - start))
        
        # TODO: Log and save process
        
        
if __name__ == '__main__':
    exp = Experiment(exp_config_path='../configs/experiments/linear_configs.default.yaml')
    exp.start()