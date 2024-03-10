import os
import yaml
import shutil
import pathlib
import threading
from loguru import logger
from flask import Blueprint, request

from .utils import *
from aicore import Experiment
from utils.request import generate_response
from utils.random import generate_random_string

module = Blueprint('exp', __name__)

# Configs
configs = None

def configure(_configs):
    global configs
    configs = _configs


# Create an experiment from JSON configs
@module.route('/create', methods=['POST'])
def experiment_create():
    
    # Extract configs from request
    if not request.is_json:
        return generate_response(
            data=None,
            success=False,
            message='Data format must be JSON!'
        ), 400
    
    exp_configs = request.get_json()
    exp_configs['data']['dir'] = configs['data']['dir']
    logger.info('[Experiment][Create] Recieve request')
    
    # Verify duplication
    for exist_id in os.listdir(configs['exp']['dir']):

        with open(os.path.join(configs['exp']['dir'], exist_id, 'configs.yaml'), 'r') as f:
            exist_configs = yaml.full_load(f)
            
            if exp_configs == exist_configs:
                
                logger.error('[Experiment][Create] Experiment exists: {}'.format(exist_id))
                
                return generate_response(
                    data=None,
                    success=False,
                    message='Experiment exists: {}'.format(exist_id)
                ), 400
    
    # Save experiment configs to local
    exp_id = generate_random_string(configs['exp']['name_len'])
    exp_dir = os.path.join(configs['exp']['dir'], exp_id)
    pathlib.Path(exp_dir).mkdir(parents=True, exist_ok=True)
    
    yaml_configs = yaml.dump(exp_configs)
    config_path = os.path.join(exp_dir, 'configs.yaml')
    with open(config_path, 'w') as f:
        f.write(yaml_configs)
    logger.info('[Experiment][Create] Experiment config save at {}'.format(config_path))
    
    # Verify configuration
    try:
        _ = Experiment(exp_dir)
        logger.success('[Experiment][Create] Experiment {} is valid'.format(exp_id))
        
        return generate_response(
            data={
                'id': exp_id
            },
            success=True,
            message='Create experiment success!'
        ), 200
    
    except Exception as e: 
        logger.exception('[Experiment][Create] Experiment {} is invalid'.format(exp_id))
        shutil.rmtree(exp_dir) # Delete that experiment
        
        return generate_response(
            data=None,
            success=False,
            message='Config format is invalid: {}'.format(repr(e))
        ), 400
        

# List all available experiment
@module.route('/list', methods=['GET'])
def experiment_list():
    
    logger.info('[Experiment][List] Recieve request')
    if os.path.exists(configs['exp']['dir']):
        exp_ids = os.listdir(configs['exp']['dir'])
    else:
        pathlib.Path(configs['exp']['dir']).mkdir(parents=True, exist_ok=True)
        exp_ids = []
    logger.success('[Experiment][List] List: {}'.format(exp_ids))
    
    return generate_response(
        data={
            "ids": exp_ids
        },
        success=True,
        message='List experiment success!'
    ), 200
    

# Delete an experiment
@module.route('/delete', methods=['DELETE'])
def experiment_delete():
    
    logger.info('[Experiment][Delete] Recieve request')
    # Extract configs from request
    if not request.is_json:
        return generate_response(
            data=None,
            success=False,
            message='Data format must be JSON!'
        ), 400
    
    
    exp_id = request.get_json()['id']
    
    if not exp_exists(exp_id, configs['exp']['dir']):
        
        logger.info('[Experiment][Delete] Id not exists')
        return generate_response(
            data=None,
            success=False,
            message='Experiment ID not found!'
        ), 400
        
    else:
        shutil.rmtree(os.path.join(configs['exp']['dir'], exp_id))
        logger.info('[Experiment][Delete] Delete Id {}'.format(exp_id))
        
        return generate_response(
            data={
                'id': exp_id
            },
            success=True,
            message='Delete {} success'.format(exp_id)
        ), 200  


# Start an created experiment
@module.route('/start', methods=['POST'])
def experiment_start():
    
    logger.info('[Experiment][Start] Recieve request')
    # Extract configs from request
    if not request.is_json:
        return generate_response(
            data=None,
            success=False,
            message='Data format must be JSON!'
        ), 400
    
    
    exp_id = request.get_json()['id']
    
    if not exp_exists(exp_id, configs['exp']['dir']):
        
        logger.info('[Experiment][Start] Id not exists')
        return generate_response(
            data=None,
            success=False,
            message='Experiment ID not found!'
        ), 400
        
    else:
        
        exp_dir = os.path.join(configs['exp']['dir'], exp_id)
        exp = Experiment(exp_dir)
        
        # Check current status
        # TODO:
        
        # Try to start experiment
        try:
            exp.try_start()
            logger.success('Experiment process works fine!')
            
        except Exception as e:
            logger.error('[Experiment][Start] Experiment process failed to start')
            return generate_response(
                data=None,
                success=False,
                message='Fail to start: {}'.format(repr(e))
            ), 400
            
        # Start experiment in background
        def start_thread():
            exp.start()
        threading.Thread(target=start_thread).start()
        
        return generate_response(
            data=None,
            success=True,
            message='Experiment {} started!'.format(exp_id)
        ), 200
        
            
        


@module.route('/status', methods=['POST'])
def experiment_status():
    # TODO: Finish this API
    return 'experiment_status'


@module.route('/stop', methods=['POST'])
def experiment_stop():
    # TODO: Finish this API
    return 'experiment_stop'

@module.route('/restart', methods=['POST'])
def experiment_restart():
    # TODO: Finish this API
    return 'experiment_restart'


@module.route('/info', methods=['POST'])
def experiment_info():
    # TODO: Finish this API
    return 'experiment_info'


@module.route('/filter', methods=['GET'])
def experiment_filter():
    # TODO: Finish this API
    return 'experiment_filter'


@module.route('/exist', methods=['GET'])
def experiment_exist():
    # TODO: Finish this API
    return 'experiment_exist'