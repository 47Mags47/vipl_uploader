import pickle as pk
import os

file_name = 'data.pickle'

def write(key, value):
    data = readAll()
    data[key] = value
    with open(file_name, 'wb') as f:
        pk.dump(data, f)
        
def read(key):
    if not os.path.isfile(file_name):
        with open(file_name, 'wb') as f:
            pk.dump({}, f)
    with open(file_name, 'rb') as f:
        data = pk.load(f)
        return data[key] if key in data else None

def readAll():
    if not os.path.isfile(file_name):
        with open(file_name, 'wb') as f:
            pk.dump({}, f)
    
    with open(file_name, 'rb') as f:
        return pk.load(f)