from datetime import datetime

# Content as a dictionary
def generate_response(data, message=None, success=True):
    
    # Get current time
    current_time = datetime.now()
    time_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'timestamp': time_string,
        'success': success,
        'message': message,
        'data': data
    }