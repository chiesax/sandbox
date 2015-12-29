#!/usr/bin/python3.4
# -*-coding:utf-8 -*
"""
Docstring de module :
eSSAI DU MODULE PINT .
il permet de calculer avec des grandeurs physiques,
donc munies de leurs unités .
In ne crée pas de classe pour elles , il se contente de permettre qu'on multiplie
un entier ou un flottant par une unité .
"""
# Les deux lignes précédentes serviraient si je rendais ce fichier
# directement exécutable
#
#              truc = objet.methode(arguments)
#On y va :
from pint import UnitRegistry

unit = UnitRegistry()

distance = 24.0*unit.m
temps = 7.3*unit.second
print(distance)
print(temps)
vitesse = distance/temps
print(vitesse)
print(temps.dimensionality)
print(vitesse.dimensionality)
force = 32*unit.N
print(force)
travail = force*distance
print(travail)
clouc = vitesse.to(unit.inch/unit.minute)
print(vitesse)
print(clouc)
work = travail.to(unit.joule)
print(work)
