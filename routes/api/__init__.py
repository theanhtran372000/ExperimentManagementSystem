from flask import Blueprint


module = Blueprint('api', __name__)

# Configs
configs = None

def configure(_configs):
    global configs
    
    configs = _configs
    
@module.route('/', methods=['GET'])
def api():
    return 'API'