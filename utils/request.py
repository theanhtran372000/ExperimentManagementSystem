from .common import get_current_timestring


# Content as a dictionary
def generate_response(data, message=None, success=True):
    
    # Get current time
    time_string = get_current_timestring()
    
    return {
        'timestamp': time_string,
        'success': success,
        'message': message,
        'data': data
    }