#!/usr/bin/python3.4
# -*-coding:utf-8 -*
"""
Docstring de module :
Ce module permet de retailler des images contenues dans un dossier,
en imposant une taille (poids) en octets (Bytes) .
donc munies de leurs unités .
On lui passe cette taille (T) et le chemin du dossier (dir ) de la manière suivante :

resize.py -t800000   "/home/jean-louis_s/Documents/JL_Python/sandbox/sandbox/data/"

Le "-t" est obligatoire , le chemin doit être entre guillemets anglais .

Il ne touche pas aux images d'origine, mais crée de nouvelles images de la taille désirée .
Il les place dans le même dossier .
"""
# Les deux lignes du début serviraient si on rendait ce fichier
# directement exécutable

# Différences avec la version python 2.7 :
# Les StringIO et cStringIO modules sont partis. Au lieu de cela, importer le io module
# et utiliser io.StringIO ou io.BytesIO pour le texte et les données respectivement
# Image est remplacée par PIL (Python Imaging Library )

import io
import PIL
import argparse
import logging
import os
import scipy
from scipy.optimize._minimize import minimize_scalar
from tempfile import NamedTemporaryFile
from PIL import Image


def resize_image(ratio, path, image_format=None):
    """
    thumbnail est une imagette

    :param ratio:entier   : Taux de réduction
    :param path:  string :  chemin du fichier image à réduire .
    :param image_format: string : extension indiquant le type de l'image (PPM, PNG, JPEG, GIF, TIFF and BMP etc )
    :return: string : l' imagette , stokée comme un string
    """
    if image_format is None:
        filename, file_extension = os.path.splitext(path)
        image_format = file_extension.strip('.')
    im = Image.open(path) # crée un objet Image de PIL
    old_size = im.size # c'est un tuple de deux éléments , la hauteur et la largeur
    # https://pillow.readthedocs.org/en/3.0.x/reference/Image.html?highlight=thumbnail
    # réduire la taille à une taille fixée
    im.thumbnail((int(old_size[0]*ratio),   # nouvelle hauteur
                  int(old_size[1]*ratio)),  # nouvelle largeur
                 PIL.Image.ANTIALIAS)       # Argument de rééchantillonnage
    # https://pillow.readthedocs.org/en/3.0.x/releasenotes/2.7.0.html?highlight=antialias
    out = io.BytesIO()   # ou io.StringIO . " out " , c'est un "flux binaire"
    im.save(out, image_format) # sauvegarde l'objet Image "PIL" dans le fichier de nom out
                               # (chaine de caractère) , de format image_format
                               # (chaine de caractère) lel que : "png"
    val = out.getvalue()       # fichier image de l'image réduite ,enregistré comme une chaîne de
    # caractères dans la variable val
    out.close()                # on ferme ce fichier image

    return val      # l' imagette , stokée comme un string


def get_ratio_for_file_size(path, target_size):
    """

    :param path: string :  chemin du dossier où sont les images à retailler .
    :param target_size: entier : taille visée en octets (Bytes)
    :return: Taux de réduction à utiliser   ,    variable que je n'ai pas comprise :  x
    """
    if os.path.getsize(path) < target_size:
        return 1.0

    def f(ratio):
        """
        Crée un fichier temporaire contenant l'image retaillée .
        calcule sa taille .
        La compare à la taille visée .
        ferme le fichier
        :param ratio: entier : Taux de rféduction .
        :return: float : écart absolu entre la taille visée et la taille obtenue .
        """
        ntf = NamedTemporaryFile(delete=False)
        ntf.write(resize_image(ratio, path))
        ntf.close()
        fsize = os.path.getsize(ntf.name)
        return abs(fsize - target_size)

    r = minimize_scalar(f, method='Bounded', bounds=(0.1, 1.0)) # manipule le paramètre scalaire de f , à savoir ratio
    # pour minimiser f
    return r.x


def resize_dir():
    """
    Fabrique de nouveaux fichiers image de la taille requise .
    Utilise les fonctions définies ci-dessus .
    Elle ne touche pas aux images d'origine, mais crée de nouvelles images de la taille désirée .
    Elle les place dans le même dossier .

    Cette fonction utilise les paramètres :
    dir : 'the path to the directory containing the images '
          'to be resized. All images contained in the directory '
          'will be processed.'
    -t   : 'target size (in bytes) of the images.'
    Qui sont passés directement à l'intèrieur de la fonction .


    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='the path to the directory containing the images '
                                    'to be resized. All images contained in the directory '
                                    'will be processed.')
    def _positive_int(val):
        myval = int(val)
        if myval <= 10:
            raise ValueError('too small value provided for target size (must be > 10)')
        return myval

    parser.add_argument('-t', help='target size (in bytes) of the images.',
                        default=None, required=True, type=_positive_int)
    opt = parser.parse_args()
    if not os.path.exists(opt.dir):
        raise Exception('the specified path {} does not exist!'.format(opt.dir))
    for fname in os.listdir(opt.dir):
        try:
            file_path = os.path.join(opt.dir, fname)
            best_ratio = get_ratio_for_file_size(file_path, opt.t)
            if best_ratio >= 1.0:
                raise Exception('could not minimize {}'.format(file_path))
            new_file_path = os.path.join(opt.dir, 'new_{}'.format(fname))
            if os.path.exists(new_file_path):
                raise Exception('file {} exist already'.format(new_file_path))
            with open(new_file_path, 'w') as f:
                f.write(resize_image(best_ratio, file_path))
            logging.info('image {} resized to {}, ratio {}'.format(file_path,
                                                                   new_file_path,
                                                                   best_ratio))
        except Exception as e:
            logging.exception(e)


#   TEST

if __name__ == '__main__':

    dir ="/home/jean-louis_s/Documents/JL_Python/sandbox/sandbox/data/"
    T=1000000
    # resize_dir() -t1000000    "/home/jean-louis_s/Documents/JL_Python/sandbox/sandbox/data/"
    # le "-t1000000" soulève toujours une erreur "unresolved reference" chez moi .
    # Je passe l'interprèteur de python 3.4 à python 2.7.6  : Le problème reste !
    # Je repasse en python 3.4 et passe StingIO en io et Image en PIL
   # Mais je n'ai pas changé les méthodes utilisées !

#     /usr/bin/python2.7 /home/jean-louis_s/Documents/JL_Python/sandbox/sandbox/images/resize.py
#   File "/home/jean-louis_s/Documents/JL_Python/sandbox/sandbox/images/resize.py", line 86
#     resize_dir()  -t1000000  "/home/jean-louis_s/Documents/JL_Python/sandbox/sandbox/data/"
#                                                                                           ^
# SyntaxError: invalid syntax
#
# Process finished with exit code 1





