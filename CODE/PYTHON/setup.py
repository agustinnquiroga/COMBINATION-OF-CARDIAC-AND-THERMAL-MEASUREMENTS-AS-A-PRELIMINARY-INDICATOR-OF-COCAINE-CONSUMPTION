# -*- coding: utf-8 -*-

from distutils.core import setup 
import py2exe 
 
setup(name="Test de cocaína", 
 version="1.0", 
 description="Test de cocaína a partir de frecuencia cardíaca y temperatura corporal", 
 author="Agustín Nahuel Quiroga Baigorri", 
 author_email="nahuelquiroga93@gmail.com", 
 url="", 
 license="open", 
 scripts=["test.py"],
 console=["test.py"],
 options={"py2exe": {"bundle_files": 1}}, 
 zipfile=None,
)
