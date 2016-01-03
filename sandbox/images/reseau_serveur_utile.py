#!/usr/bin/python3.4
# -*-coding:utf-8 -*
"""

https://openclassrooms.com/courses/apprenez-a-programmer-en-python/le-reseau

À LA FIN LE TERMINAL QUITTE PYTHON :
DONC CE PROGRAMME NE MARCHE PAS !!

"""
# Les deux lignes précédentes serviraient si je rendais ce fichier
# directement exécutable

import socket

# Construire notre socket      :    LE SERVEUR
#   socket.AF_INET : la famille d'adresses, ici ce sont des adresses Internet ;
#
#     socket.SOCK_STREAM : le type du socket, SOCK_STREAM pour le protocole TCP.

connexion_principale = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("connexion_principale :\n",connexion_principale)

# Connecter le socket

#  le nom de l'hôte sera vide et le port sera celui que vous voulez, entre 1024 et 65535.

connexion_principale.bind(("",12800))  # l'argument unique de bind est un tuple !!
print("bind :\n",connexion_principale.bind)

# Faire écouter notre socket

connexion_principale.listen(5)
print("listen :\n",connexion_principale.listen)
print("salute")


# +++                 Il y a donc deux ports dans notre histoire    +++
#
# mais celui qu'utilise le client
#  pour ouvrir sa connexion ne va pas nous intéresser.

connexion_avec_client,infos_connexion = connexion_principale.accept()

