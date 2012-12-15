#!/usr/bin/env python
# -*- coding: utf8 -*-

import irclib
import ircbot
import socket
import time
import random

class BotIRCbyGHOST(ircbot.SingleServerIRCBot):
    def __init__(self):
        print "OwnYourIRCBot"
        name = raw_input('nom de votre bot:')
        serveur = raw_input('serveur irc:')
        port = input('port:')
        ircbot.SingleServerIRCBot.__init__(self, [(serveur, port)],
                                           name, "OwnYourIRCBot by GHOSTnew")
        self.insultes = ["merde","shit","pute","bitch","elle est baisable","she´s good to fuck","cette fille a des oeufs sur le plat","il paraît que je fais bien l´amour","they say, im good in bed","dégage","Fuck off","va te faire foutre enculé","fuck off asshole","baise toi","f*ck you","mon cul","bite me","Ta mère est une pute!","your mother´s a bitch","tete de con","shitface","gros cul","fat ass","honky tonk","Salsalop","dirty bitch","fils de pute","son of a b*tch","Ta gueule!","Shut up"]
        print 'connection en cours'

    def on_welcome(self, serv, ev):
        global your_target
        your_target = "no target"
        global owner
        owner = raw_input('votre pseudo sur IRC:')
        global chan
        chan = raw_input('Chan (sans le #):')
        serv.join("#"+chan)
        serv.privmsg(chan, "salut tous le monde")
        print 'le bot est desormais sur le chan'
    def on_kick(self, serv, ev):
        serv.join("#"+chan)
    def on_pubmsg(self, serv, ev):
        global your_target
        global owner
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        canal_verification = (ev.target(), self.channels[ev.target()])
        message = ev.arguments()[0].lower()
        if message == "&quit" and owner == auteur:
            print 'vous avez deconnecter votre bot'
            self.die()
        elif message == "&quit" and owner != auteur:
            serv.privmsg(canal, "\00304\002Vous n'avez pas les privilège sur ce bot\002")
            print 'un utilisateur a voulu deconnecter le bot'
        elif message[0:5] == "&join":
            serv.join(message[6:100])
            serv.privmsg(message[6:100], "salut tous le monde")
        elif message == "&part":
            serv.part(canal)
        elif message == "&target":
            serv.privmsg(canal, "Target: " + your_target)
        elif message[0:11] == "&set-target" and owner == auteur:
            your_target = message[12:100]
            serv.privmsg(canal, "Target défini ;)")
        elif message[0:11] == "&set-target" and owner != auteur:
            serv.privmsg(canal, "\00304\002Vous n'avez pas les privilège sur ce bot\002")
        elif message[0:6] == "&check":
            host_a_tester = message[7:100]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((host_a_tester, 80))
                s.shutdown(2)
                serv.privmsg(canal, "It is just you. " + host_a_tester + " is up.")
            except:
                serv.privmsg(canal, "It's not just you! " + host_a_tester + " looks down from here.")
        elif message == "&time":
            serv.privmsg(canal, "nous sommes le: "  + time.strftime("%A %d %B %Y %H:%M:%S"))
        elif message[0:5] == "&kick" and canal_verification[1].is_halfoper(auteur) or canal_verification[1].is_oper(auteur):
            serv.kick(canal, message[6:100] , "kicked by " + auteur)
        elif message[0:5] == "&kick"  and not canal_verification[1].is_halfoper(auteur) and not canal_verification[1].is_oper(auteur):
            serv.privmsg(canal, "\00304\002Vous n'avez pas les privilège sur ce chan\002")
        elif message[0:4] == "&say":
            serv.privmsg(canal, message[5:400])
        elif message == "&random" :
            serv.privmsg(canal, "\00304\002Voici un nombre : " + str(random.random()) + "\002")
        elif message == "&copy" :
            serv.privmsg(canal, "OwnYourIRCBot v1.2")
            serv.privmsg(canal, "Team Mondial Production 2012")
            serv.privmsg(canal, "by GHOSTnew")
            serv.privmsg(canal, "avec la participation de lumir")
            serv.privmsg(canal, "source: https://github.com/GHOSTnew/OwnYourIRCBot")
        elif message == "&help":
            serv.privmsg(canal, "\002\037les commandes sont:\037\002")
            serv.privmsg(canal, "\00310\002&join\002 #chan \00315,01(pour que le bot se connecte a un chan)")
            serv.privmsg(canal, "\00310\002&part\002 \00315,01(pour que le bot quitte le chan)")
            serv.privmsg(canal, "\00310\002&target\002 \00315,01(affiche le target)")
            serv.privmsg(canal, "\00310\002&set-target\002 \00315,01(defini un target)")
            serv.privmsg(canal, "\00310\002&check\002 \00315,01(verifie si un site est down ou pas)")
            serv.privmsg(canal, "\00310\002&time\002 \00315,01(affiche la date et l'heure)")
            serv.privmsg(canal, "\00310\002&kick\002 \00315,01(kick un joueur)")
            serv.privmsg(canal, "\00310\002&random\002 \00315,01(génère un nombre aléatoire entre 0 et 1)")
            serv.privmsg(canal, "\00310\002&say\002 \00315,01(permet de faire dire quelque chose au bot)")
            serv.privmsg(canal, "\00310\002&copy\002 \00315,01(affiche les credits)")
            serv.privmsg(canal, "\00310\002&quit\002 \00315,01(pour déconnecter le bot)")
        elif not canal_verification[1].is_voiced(auteur)and not canal_verification[1].is_halfoper(auteur) and not canal_verification[1].is_oper(auteur):
            for insulte in self.insultes:
                if insulte in message:
                    serv.kick(canal[0], auteur, "Les insultes ne sont pas autorisées ici !")
                    break
if __name__ == "__main__":
    BotIRCbyGHOST().start()
