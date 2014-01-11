#!/usr/bin/env python
# -*- coding: utf8 -*-

import irclib, ircbot, socket, time, random, ConfigParser

class BotIRCbyGHOST(ircbot.SingleServerIRCBot):
    def __init__(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read('config.ini')
        print "OwnYourIRCBot"
        name = cfg.get('OwnYourIRCBot', 'name')
        serveur = cfg.get('OwnYourIRCBot', 'server')
        port = cfg.getint('OwnYourIRCBot', 'port')
        ircbot.SingleServerIRCBot.__init__(self, [(serveur, port)],
                                           name, "OwnYourIRCBot by GHOSTnew")
        self.your_target = "No target"
        self.your_video = "No video"
        self.owner = cfg.get('OwnYourIRCBot', 'owner')
        self.chans = cfg.get('OwnYourIRCBot', 'channels')
        self.version = "1.4"
        self.insultes = ["merde","shit","pute","bitch","elle est baisable","she´s good to fuck","il paraît que je fais bien l´amour","they say, im good in bed","dégage","Fuck off","va te faire foutre enculé","fuck off asshole","baise toi","f*ck you","mon cul","bite me","Ta mère est une pute!","your mother´s a bitch","tete de con","shitface","gros cul","fat ass","honky tonk","Salsalop","dirty bitch","fils de pute","son of a b*tch","Ta gueule!","Shut up"]
        print 'connection en cours'

    def on_welcome(self, serv, ev):
        if "," in self.chans:
            for chan in self.channels.split(","):
                serv.join(chan)
                serv.privmsg(chan, "salut tous le monde")
        else:
             serv.join(self.chans)
             serv.privmsg(self.chans, "salut tous le monde")
        print 'le bot est desormais sur le(s) channel(s)'
    def on_kick(self, serv, ev):
        serv.join(ev.target())
    def on_pubmsg(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        canal_verification = (ev.target(), self.channels[ev.target()])
        message = ev.arguments()[0].lower()
        if message == "&quit" and self.owner == auteur:
            self.success_msg(canal, "Déconnexion", serv)
            print 'vous avez deconnecter votre bot'
            self.die()
        elif message == "&quit" and self.owner != auteur:
            self.error_msg(canal, "\00304\002Vous n'avez pas les privilège sur ce bot\002", serv)
            print 'un utilisateur a voulu deconnecter le bot'
        elif message.startswith("&join"):
            serv.join(message.split(" ")[1])
            serv.privmsg(message.split(" ")[1], "salut tous le monde")
        elif message == "&part":
            serv.part(canal)
        elif message.startswith("&target"):
            self.success_msg(canal, "Target: " + self.your_target)
        elif message.startswith("&set-target") and self.owner == auteur:
            self.your_target = message.split(" ")[1]
            self.success_msg(canal, "Target défini ;)", serv)
        elif message.startswith("&set-target") and self.owner != auteur:
            self.error_msg(canal, "\00304\002Vous n'avez pas les privilège sur ce bot\002", serv)
        elif message.startswith("&check"):
            host_a_tester = message.split(" ")[1]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((host_a_tester, 80))
                s.shutdown(2)
                self.success_msg(canal, "It is just you. \00310" + host_a_tester + "\003 is up.", serv)
            except:
                self.warning_msg(canal, "It's not just you! \00310" + host_a_tester + "\003 looks down from here.", serv)
        elif message == "&time":
            self.success_msg(canal, "nous sommes le: "  + time.strftime("%A %d %B %Y %H:%M:%S", serv))
        elif message.startswith("&kick") and canal_verification[1].is_halfoper(auteur) or canal_verification[1].is_oper(auteur):
            serv.kick(canal, message.split(" ")[1] , "kicked by " + auteur)
        elif message.startswith("&kick")  and not canal_verification[1].is_halfoper(auteur) and not canal_verification[1].is_oper(auteur):
            self.error_msg(canal, "\00304\002Vous n'avez pas les privilège sur ce chan\002", serv)
        elif message.startswith("&say"):
            serv.privmsg(canal, message.split("&say ")[1])
        elif message.startswith("&random"):
            self.success_msg(canal, "\00304\002Voici un nombre : " + str(random.random()) + "\002", serv)
        elif message.startswith("&set-video") and self.owner == auteur:
            your_video = message.split(" ")[1]
            self.success_msg(canal, "video défini ;)", serv)
        elif message.startswith("&set-video") and self.owner != auteur:
            self.error_msg(canal, "\00304\002Vous n'avez pas les privilège sur ce bot\002", serv)
        elif message.startswith("&video"):
            self.success_msg(canal, "video: " + self.your_video, serv)
        elif message.startswith("&tools"):
            self.success_msg(canal, "\00310\002hping:\002 \00315http://www.hping.org/ ]-[ OS: Linux, FreeBSD, NetBSD, OpenBSD, Solaris, MacOs X, Windows", serv)  
            self.success_msg(canal, "\00310\002Slowloris:\002 \00315http://ha.ckers.org/slowloris/ ]-[ OS: Linux", serv)
            self.success_msg(canal, "\00310\002HOIC:\002 \00315http://www.mediafire.com/?jkc7924jsa0161z ]-[ OS: Windows", serv)
            self.success_msg(canal, "\00310\002Pyloris:\002 \00315http://sourceforge.net/projects/pyloris/ ]-[ OS: Windows, MacOs X, Linux", serv)
            self.success_msg(canal, "\00310\002THC-SSL-DOS:\002 \00315http://www.thc.org/thc-ssl-dos/ ]-[ OS: Windows, Linux", serv)
            self.success_msg(canal, "\00310\002Torshammer:\002 \00315http://packetstormsecurity.org/files/98831 ]-[ OS: Linux", serv)
            self.warning_msg(canal, "Use protection (tor, vpn, vps, etc.)", serv)
            self.warning_msg(canal, "We are not responsible for any of the actions nor do we condone using these tools to intentionally cause harm or damage to any website(s) or server(s). Do so at your own risk.", serv)
        elif message.startswith("&copy") :
            serv.privmsg(canal, "\00315OwnYourIRCBot v\00310\002" + self.version)
            serv.privmsg(canal, "\00315Team Mondial Production 2012")
            serv.privmsg(canal, "\00315by \00310\002GHOSTnew")
            serv.privmsg(canal, "\00315avec la participation de \00310\002lumir")
            serv.privmsg(canal, "\00315source: https://github.com/GHOSTnew/OwnYourIRCBot")
        elif message.startswith("&help"):
            self.success_msg(canal, "\002\037les commandes sont:\037\002", serv)
            self.success_msg(canal, "\00310\002&join\002 #chan \00315,01(pour que le bot se connecte a un chan)", serv)
            self.success_msg(canal, "\00310\002&part\002 \00315,01(pour que le bot quitte le chan)", serv)
            self.success_msg(canal, "\00310\002&target\002 \00315,01(affiche le target)", serv)
            self.success_msg(canal, "\00310\002&set-target\002 \00315,01(defini un target)", serv)
            self.success_msg(canal, "\00310\002&check\002 \00315,01(verifie si un site est down ou pas)", serv)
            self.success_msg(canal, "\00310\002&time\002 \00315,01(affiche la date et l'heure)", serv)
            self.success_msg(canal, "\00310\002&kick\002 \00315,01(kick un joueur)", serv)
            self.success_msg(canal, "\00310\002&random\002 \00315,01(génère un nombre aléatoire entre 0 et 1)", serv)
            self.success_msg(canal, "\00310\002&video\002 \00315,01(affiche le lien d'une video)", serv)
            self.success_msg(canal, "\00310\002&set-video\002 \00315,01(définit une video)", serv)
            self.success_msg(canal, "\00310\002&tools\002 \00315,01(affiche les logiciels pour DDoS)", serv)
            self.success_msg(canal, "\00310\002&say\002 \00315,01(permet de faire dire quelque chose au bot)", serv)
            self.success_msg(canal, "\00310\002&copy\002 \00315,01(affiche les credits)", serv)
            self.success_msg(canal, "\00310\002&quit\002 \00315,01(pour déconnecter le bot)", serv)
        elif not canal_verification[1].is_voiced(auteur)and not canal_verification[1].is_halfoper(auteur) and not canal_verification[1].is_oper(auteur):
            for insulte in self.insultes:
                if insulte in message:
                    serv.kick(canal[0], auteur, "Les insultes ne sont pas autorisées ici !")
                    break

    def error_msg(self, channel, msg, serv):
        serv.privmsg(channel, "\002[\0034-\003]\002 " + msg)

    def success_msg(self, channel, msg, serv):
        serv.privmsg(channel, "\002[\0039+\003]\002 " + msg)

    def warning_msg(self, channel, msg, serv):
        serv.privmsg(channel, "\002[\0037*\003]\002 " + msg)

if __name__ == "__main__":
    BotIRCbyGHOST().start()
