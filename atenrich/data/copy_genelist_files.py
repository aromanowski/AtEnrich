#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 13:22:00 2017

@author: daniel
"""
import shutil
import os.path
from glob import glob

dst = './genelists'

home_dir = os.getenv('HOME')
genelist_path = home_dir+'/Dropbox/Work/Circadian/Data/'
files = [y for x in os.walk(genelist_path) for y in glob(os.path.join(x[0], '*.genelist'))]

for src in files:
    shutil.copy(src, dst)