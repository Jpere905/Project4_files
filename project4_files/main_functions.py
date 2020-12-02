import json

def write_to_file(data, file_name):
    with open(file_name,'w') as write_file:
        json.dump(data, write_file, indent=4)
        print("{0} file successfully written...".format(file_name))

def read_from_file(file_name):
    with open(file_name, 'r') as read_file:
        data = json.load(read_file)
        print("{0} file successfully read...".format(file_name))
        return data