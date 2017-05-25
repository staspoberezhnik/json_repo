import random
import string
import os


def protect_name(filename):
    protect = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    filename, extension = os.path.splitext(filename)
    new_name = '{0}_{1}{2}'.format(filename, protect, extension)
    print(new_name)
    return new_name

