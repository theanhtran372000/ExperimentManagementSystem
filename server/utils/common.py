import random
import string
from datetime import datetime


def generate_random_string(length):
    chars = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(chars, k=length))
    return random_string

def get_current_timestring(format='%Y-%m-%d %H:%M:%S.%f'):
    current_time = datetime.now()
    time_string = current_time.strftime(format)
    return time_string

def calculate_duration(start_timestamp, end_timestamp, format='%Y-%m-%d %H:%M:%S.%f'):
    start_datetime = datetime.strptime(start_timestamp, format)
    end_datetime = datetime.strptime(end_timestamp, format)
    duration = end_datetime - start_datetime
    return duration