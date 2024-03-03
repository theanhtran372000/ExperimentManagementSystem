from flask import Blueprint, request, make_response, \
    redirect, render_template
from . import api # Submodules


module = Blueprint('root', __name__)

# Configs
configs = None

def configure(_configs):
    global configs
    
    # Config local
    configs = _configs
    
    # Config submodules
    api.configure(configs)

# Register submodules
module.register_blueprint(api.module, url_prefix='/api')


# Preflight requests
@module.before_request
def before_request():
    
    # If the request method is OPTIONS (a preflight request)
    if request.method == 'OPTIONS':
        
        # Create a 200 response and add the necessary headers
        response = make_response('OK')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        
        # Return the response
        return response

# Test connection
@module.route('/ping', methods=['GET'])
def ping():
    return 'PONG'

# Default route
@module.route('/')
def redirect_to_home():
    return redirect('/home')

@module.route('/home', methods=['GET'])
def home():
    return render_template('home.html')