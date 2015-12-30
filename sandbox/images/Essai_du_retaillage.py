#!/usr/bin/python3.4
# -*-coding:utf-8 -*

# coding: utf8

# Pillow n'existe pas en tant que tel
import PIL
from PIL import Image
import io
import os
from tempfile import NamedTemporaryFile
#                        img = Image.open('brick-house.png')
path_image = "/home/jean-louis_s/Documents/JL_Python/sandbox/sandbox/data/Eglise de Songeons.png"
chemin= "/home/jean-louis_s/Documents/JL_Python/sandbox/sandbox/data/"
ratio = 0.5
image_format = "png"

print(type(os.listdir(chemin)),os.listdir(chemin))

init_size = os.path.getsize(path_image)


im = Image.open(path_image) # cr�e un objet Image de PIL
old_size = im.size # c'est un tuple de deux �l�ments , la hauteur et la largeur
# https://pillow.readthedocs.org/en/3.0.x/reference/Image.html?highlight=thumbnail
# r�duire la taille � une taille fix�e
im.thumbnail((int(old_size[0]*ratio),   # nouvelle hauteur
              int(old_size[1]*ratio)),  # nouvelle largeur
             PIL.Image.ANTIALIAS)       # Argument de r��chantillonnage
# https://pillow.readthedocs.org/en/3.0.x/releasenotes/2.7.0.html?highlight=antialias
out = io.BytesIO()   #  c'est un "flux binaire"
nouveau_nom_image = "nouvelle_eglise"

im.save(out, image_format) # sauvegarde l'objet Image "PIL" dans le fichier de nom out
                           # (chaine de caract�re) , de format image_format
                           # (chaine de caract�re) lel que : "png"
val = out.getvalue()       # flottant : taille du fichier obtenu
out.close()                # on ferme ce fichier image
taille = 800


target_size = 800000
ntf = NamedTemporaryFile(delete=False)
ntf.write(val)
ntf.close()
fsize = os.path.getsize(ntf.name)
diff =  abs(fsize - target_size)

print("type de NamedTemporaryFile",ntf)
taux_txt = "taux de reduction : "
print(taux_txt,ratio)
print("taille de l'image originale",init_size,"soit",float(init_size)/1000," kO")
print("taille atteinte :",type(diff),fsize,"soit",float(fsize)/1000," kO")


    # val = out.getvalue()       # flottant : taille du fichier obtenu
    # out.close()
    # /home/jean-louis_s/.PyCharm50/config/scratches/Essai_du_retaillage.py