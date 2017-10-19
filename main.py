import os
from cryptography.fernet import Fernet

def key_generation():
    # Put this somewhere safe!
    key = Fernet.generate_key()
    print key
    f = Fernet(key)

    return f

def crypt(key, data):
    return key.encrypt(data)


def decrypt(key, data):
    return key.decrypt(data)


def open_file(file_name):
    #Read the entire file as a single byte string
    with open(file_name, 'rb') as f:
        data = f.read()

    return data


def write_file(path, file_string):
    # Take name and extension from a path
    name_file, ext = name_and_extension(path)

    if ext == '.LOL':
        with open(path, 'wb') as f:
            f.write(file_string)
    else:
        with open(path+'.LOL', 'wb') as f:
            f.write(file_string)


def name_and_extension(path):
    name_file = os.path.splitext(os.path.basename(path))[0]
    ext = os.path.splitext(os.path.basename(path))[1]

    return name_file, ext



"""Main"""

#Name File
path= 'photo.jpg'

#Key Creation with Fernet
key = key_generation()

#Open file as a string
file_string = open_file(path)

#File Encryption
encrypted = crypt(key, file_string)
print encrypted

#Create a file with .LOL extension
write_file(path, encrypted)

#Decript the file
decrypted = decrypt(key, encrypted)
print decrypted

