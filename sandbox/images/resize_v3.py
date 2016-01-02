#!/usr/bin/python3.4
# -*-coding:utf-8 -*
"""
Docstring de module :
Ce module permet de retailler des images contenues dans un dossier,
en imposant une taille (poids) en octets (Bytes) .
donc munies de leurs unitÃ©s .
On lui passe cette taille (T) et le chemin du dossier (dir ) de la maniÃ¨re suivante :

sandbox_resize_dir -t 100000 . #  , car Samuele a fait un fichier setup ,
 le "   .  "" veut dire le répertoire où on a lancé le terminal

ou
resize.py -t 800000   "/home/jean-louis_s/Documents/JL_Python/sandbox/sandbox/data/"

Le "-t" est obligatoire , suivi d'un blanc, le chemin doit Ãªtre entre guillemets anglais .
Notez que vous pouvez aussi Ã©crire dans le terminal

resize.py -t 800000  .
Le point . signifie le rÃ©pertoire courant.
Ou bien  .. qui signifie le rÃ©pertoire un niveau plus haut.

Il ne touche pas aux images d'origine, mais crÃ©e de nouvelles images de la taille dÃ©sirÃ©e .
Il les place dans le mÃªme dossier .

Se placer dans
le rÃ©pertoire oÃ¹ sest le programme resize.py .

Clic-droit :
    ouvrir un terminal

faire :
    pwd     on rÃ©cupÃ¨re le path par shift/CRTL-C


Se placer dans
    le rÃ©pertoire oÃ¹ sont les images Ã  retailler .

Clic-droit :
    ouvrir un terminal

taper
    python3.4  /home/jean-louis_s/Bureau/Programmes_Py/retailler/resize.py   -t   800000   .
(On rÃ©cupÃ¨re le chemin du programme par CRTL-V )
(le   "   .   " de la fin signifie le rÃ©pertoire courant  )



"""


# Les deux lignes du dÃ©but serviraient si on rendait ce fichier
# directement exÃ©cutable

# DiffÃ©rences avec la version python 2.7 :
# Les StringIO et cStringIO modules sont partis. Au lieu de cela, importer le io module
# et utiliser io.StringIO ou io.BytesIO pour le texte et les donnÃ©es respectivement
# Image est remplacÃ©e par PIL (Python Imaging Library )

import io
import PIL
import argparse

import os
import scipy
from scipy.optimize._minimize import minimize_scalar

from tempfile import NamedTemporaryFile   # CrÃ©e et manipule des fichiers temporaires
# stockÃ©s dans un "nom" (name) soit, je pense, une variable
# https://docs.python.org/2/library/tempfile.html?highlight=tempfile#module-tempfile
from PIL import Image

import logging
# LOGGING   :
# https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook
#
# The ability to create new handlers with higher- or lower-severity filters
# can be very helpful when writing and testing an application.
# Instead of using many print statements for debugging, use logger.debug:
#  Unlike the print statements, which you will have to delete or comment out later,
#  the logger.debug statements can remain intact in the source code and remain dormant
#  until you need them again. At that time, the only change that needs to happen is
# to modify the severity level of the logger and/or handler to debug.

import sys
print(sys.argv)


compteur_appel_resize_image = 0  # variable globale


def resize_image(ratio, path, image_format=None):
    """
    thumbnail est une imagette

    :param ratio:entier   : Taux de rÃ©duction
    :param path:  string :  chemin du fichier image Ã  rÃ©duire .
    :param image_format: string : extension indiquant le type de l'image (PPM, PNG, JPEG, GIF, TIFF and BMP etc )
    :return: string : l' imagette , stokÃ©e comme un string
    """
    global compteur_appel_resize_image
    compteur_appel_resize_image += 1

    init_size = os.path.getsize(path)
    if compteur_appel_resize_image <= 2 :
        print(path,init_size,"soit",float(init_size)/1000," kO")

    if image_format is None:
        filename, file_extension = os.path.splitext(path)
        image_format = file_extension.strip('.')
    im = Image.open(path) # crÃ©e un objet Image de PIL
    old_size = im.size # c'est un tuple de deux Ã©lÃ©ments , la hauteur et la largeur
    # https://pillow.readthedocs.org/en/3.0.x/reference/Image.html?highlight=thumbnail
    # rÃ©duire la taille Ã  une taille fixÃ©e
    im.thumbnail((int(old_size[0]*ratio),   # nouvelle hauteur
                  int(old_size[1]*ratio)),  # nouvelle largeur
                 PIL.Image.ANTIALIAS)       # Argument de rÃ©Ã©chantillonnage
    # https://pillow.readthedocs.org/en/3.0.x/releasenotes/2.7.0.html?highlight=antialias
    out = io.BytesIO()   #  " out " , c'est un "flux binaire"
    im.save(out, image_format) # sauvegarde l'objet Image "PIL" dans le fichier de nom out
                               # (chaine de caractÃ¨re) , de format image_format
                               # (chaine de caractÃ¨re) lel que : "png"
    val = out.getvalue()       # fichier image de l'image rÃ©duite ,enregistrÃ© comme une chaÃ®ne de
    # caractÃ¨res dans la variable val
    out.close()                # on ferme ce fichier image

    return val      # l' imagette , stokÃ©e comme un string


def get_ratio_for_file_size(path, target_size):
    """

    :param path: string :  chemin du dossier oÃ¹ sont les images Ã  retailler .
    :param target_size: entier : taille visée en octets (Bytes)
    :return: Taux de rÃ©duction Ã  utiliser   ,    variable que je n'ai pas comprise :  x
    """
    if os.path.getsize(path) < target_size:
        return 1.0

    def f(ratio):
        """
        CrÃ©e un fichier temporaire contenant l'image retaillÃ©e .
        calcule sa taille .
        La compare Ã  la taille visÃ©e .
        ferme le fichier
        :param ratio: entier : Taux de rfÃ©duction .
        :return: float : Ã©cart absolu entre la taille visÃ©e et la taille obtenue .
        """
        ntf = NamedTemporaryFile(delete=False)
        ntf.write(resize_image(ratio, path))
        ntf.close()
        fsize = os.path.getsize(ntf.name)  # type : "long"  ;  Long integers have unlimited precision
                                           # taille du fichier

        # taux_txt = "taux de reduction : "
        # print(taux_txt,ratio)
        # print("taille atteinte :","soit",float(fsize)/1000," kO")

        global compteur_appel_resize_image
        actuelle_size = fsize
        if compteur_appel_resize_image <= 2 :
            print(path,actuelle_size,"soit",float(actuelle_size)/1000," kO")

        return abs(fsize - target_size)
    borne_sup= 1.0 # précédemment 1.0 (regarder comment fonctionne minimize_scalar
    r = minimize_scalar(f, method='Bounded', bounds=(0.1, borne_sup)) # manipule le paramÃ¨tre scalaire de f , Ã  savoir ratio
    # pour minimiser f
    return r.x


def resize_dir(args=None):
    """
    Fabrique de nouveaux fichiers image de la taille requise .
    Utilise les fonctions dÃ©finies ci-dessus .
    Elle ne touche pas aux images d'origine, mais crÃ©e de nouvelles images de la taille dÃ©sirÃ©e .
    Elle les place dans le mÃªme dossier .

    Cette fonction utilise les paramÃ¨tres :
    dir : 'the path to the directory containing the images '
          'to be resized. All images contained in the directory '
          'will be processed.'
    -t   : 'target size (in bytes) of the images.'
    Qui sont passÃ©s directement Ã  l'intÃ¨rieur de la fonction .

    Une fois tous les arguments dÃ©clarÃ©es, il faut rÃ©ellement parser les arguments
    ---      passÃ©s dans la ligne de commande.    ------------
    Cela se fait avec cette ligne de code :
    opt = parser.parse_args(args=args)


    :return:
    """
    trieur = argparse.ArgumentParser()
    trieur.add_argument('dir', help='the path to the directory containing the images '
                                    'to be resized. All images contained in the directory '
                                    'will be processed.')
    # Le fait de dÃ©clarer l' arguments dir  sans tirets (cf Partie suivante)
    # indique Ã  argparse de le considÃ©rer comme argument obligatoire.

    def _positive_int(val):
        myval = int(val)
        if myval <= 10:
            raise ValueError('too small value provided for target size (must be > 10)')
        return myval

    trieur.add_argument('-t', help='target size (in kbytes) of the images.',
                        default=None, required=True, type=_positive_int)
    # opt = trieur.parse_args(args=args)
    arguments = trieur.parse_args()
    print("\nVous voulez une taille de :  ", arguments.t," kO")
    taille_visee = arguments.t*1000   # en octets , pour le module image  .
    precision_taille = 20000 # en octets , pour qu'il n'y ait pas trop d'itérations
    print("Plus tard la précision sera fixée à : ",precision_taille/1000," kO\n")

    print("arguments =",arguments)
    print("arguments.dir = ",arguments.dir)
    print("arguments.t = ",arguments.t)

    # opt et arguments sont des instances de la classe : <class 'argparse.Namespace'>
    # opt.dir est un string
    # -t : option courte
    # -taille : option longue
    # ici notre programme dit que l'option attend un argument .

    print(type(arguments))

    chemin_dir = os.getcwd()
    liste_rep= chemin_dir.split("/")
    nb_rep = len(liste_rep)
    ma_dir = liste_rep[nb_rep-1]
    print(ma_dir)
    new_taille = str(int(arguments.t))
    chemin_dossier_im_retaillees = "../"+ma_dir+"_"+new_taille+"_ko"
    print("chemin_dossier_im_retaillées :",chemin_dossier_im_retaillees)

    print(nb_rep)
    print(ma_dir)
    if not os.path.exists(chemin_dossier_im_retaillees):
        os.mkdir(chemin_dossier_im_retaillees)
    if not os.path.exists(arguments.dir):  # arguments.dir est la variable dir de l'espace de nom arguments
        raise Exception('the specified path {} does not exist!'.format(arguments.dir))
    for fname in os.listdir(arguments.dir):  # fname parcourt les noms des fichiers
        #  présents dans le dossier de chemin donnÃ© par le paramÃ¨tre dir dans la liste des paramÃ¨tres
        #  construite par le "parser"
        print(fname)
        global compteur_appel_resize_image
        compteur_appel_resize_image =0
        # remise Ã  zero Ã  chaque traitement d'une nouvelle image

        try:
            file_path = os.path.join(arguments.dir, fname)
            best_ratio = get_ratio_for_file_size(file_path, taille_visee)
            # arguments.t est l'argument repèré par le parser comme ayant le nom t
            if best_ratio >= 1.0:
                raise Exception('could not minimize {}'.format(file_path))
            new_chemin_image =new_taille+"_ko_"+"{}".format(fname)
            print(new_chemin_image)
            # new_file_path = os.path.join(opt.dir, 'new_{}'.format(fname))
            new_file_path = os.path.join(chemin_dossier_im_retaillees, new_chemin_image)

            # fname est le nom du fichier que l'on est en train de traiter .
            print(new_file_path)
            if os.path.exists(new_file_path):
                raise Exception('file {} exist already'.format(new_file_path))
            with open(new_file_path, 'bw') as f:
                # le "bw' est capital , c'est lui qui dit qu'on Ã©crit en binaire ,
                # et donc que   val ,renvoyÃ© ci-dessous par resize_image
                #  en dÃ©finitive doit Ãªtre en Bytes !!!
                f.write(resize_image(best_ratio, file_path))
            logging.info('image {} resized to {}, ratio {}'.format(file_path,
                                                                   new_file_path,
                                                                   best_ratio))
        except Exception as e:
            logging.exception(e)


#   TEST

# La variable a n'est pas passÃ©e en paramÃ¨tre de la fonction print_a.
# Et pourtant, Python la trouve,
# tant qu'elle a Ã©tÃ© dÃ©finie avant l'appel de la fonction.
#
# C'est lÃ  qu'interviennent les diffÃ©rents espaces.

if __name__ == '__main__':
    # dir = os.path.join(os.path.dirname(__file__), '..', 'A_retailler')
    # dir = "/home/jean-louis_s/Bureau/Documents/JL_Python/images_data"
    resize_dir(args=['-t', '1000', "."])






