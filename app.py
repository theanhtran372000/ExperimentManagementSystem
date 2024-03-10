import yaml
import pprint
import pathlib
from loguru import logger
from flask import Flask
from flask_cors import CORS

import routes
import aicore


# Flask app
app = Flask(
    __name__, static_url_path='',
    template_folder='templates',
    static_folder='static'
)

cors = CORS(app) # Enable CORS
app.config['CORS_HEADERS'] = 'Content-Type'


# Main function
def main():
    ### === Preparation === ###
    # Read config
    with open('configs/configs_all.yaml', 'r') as f:
        configs = yaml.load(f, yaml.FullLoader)
    
    logger.info('Configs: {}'.format(
        pprint.pformat(configs)
    )) 
    
    # Config routes
    logger.info('Configuring routes')
    routes.configure(configs)
    app.register_blueprint(routes.module, url_prefix='/')
    
    # Prepare experiment
    logger.info('Seeding AI Core at {}'.format(configs['exp']['seed']))
    aicore.seed(configs['exp']['seed'])
    pathlib.Path(configs['exp']['dir']).mkdir(parents=True, exist_ok=True)
    
    ### === Flask Server === ###
    # Run server
    logger.info('Server is listening at {}!'.format(configs['app']['port']))
    app.run(host=configs['app']['host'], port=configs['app']['port'], threaded=configs['app']['multithread'])
    
    
if __name__ == '__main__':
    main()