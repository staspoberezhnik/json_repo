import random
import string


def protect_name(filename):
    protect = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    new_name = filename + protect

    return new_name



