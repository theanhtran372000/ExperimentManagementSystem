import random
import string


def generate_random_string(length):
    chars = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(chars, k=length))
    return random_string