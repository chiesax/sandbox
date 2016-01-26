# -*- coding: utf-8 -*-
"""
Created by chiesa on 07.01.15

Copyright 2015 Alpes Lasers SA, Neuchatel, Switzerland
"""
import importlib

__author__ = 'chiesa'
__copyright__ = "Copyright 2015, Alpes Lasers SA"


def dynimport(importspec):
    module, attr = importspec.split(":")
    return getattr(importlib.import_module(module),
                   attr)
