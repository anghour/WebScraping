__author__= "Azziz ANGHOUR"
__email__= "anghour@gmail.com"
__version__= "1.0.0"


from jsonpickle import encode, decode

def save_in_json_format(path, data):
    file = open(path, "w")
    file.write(encode(data))
    file.close()