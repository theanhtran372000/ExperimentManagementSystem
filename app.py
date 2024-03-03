import yaml
import pprint
from loguru import logger
from flask import Flask, request, make_response, render_template, redirect
from flask_cors import CORS

import routes

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
    routes.configure(configs)
    app.register_blueprint(routes.module, url_prefix='/')
    
    ### === Flask Server === ###
    # Run server
    logger.info('Server is listening at {}!'.format(configs['app']['port']))
    app.run(host=configs['app']['host'], port=configs['app']['port'], threaded=configs['app']['multithread'])
    
    
if __name__ == '__main__':
    main()