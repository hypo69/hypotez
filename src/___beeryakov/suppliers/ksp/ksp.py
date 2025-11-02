## \file /src/___beeryakov/suppliers/ksp/ksp.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.___beeryakov.suppliers.ksp 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.___beeryakov.suppliers.ksp """


"""  [File's Description]

@namespace src: src
 \package beeryakov.suppliers.ksp 
 
\file ksp.py
 @section libs imports:
  - json 
  - webdriver 
Author(s):
  - Created by [Davidka] [BenAvraham] on 08.11.2023 .
"""
import json
from src.webdriver import executor

with open('suppliers\\ksp\\locators.json', 'r',  encoding='utf-8') as f:
    locators = json.load(f)

def get_worlds():
    worlds = executor(locators['worlds'])
    worlds_dic: dict = {}
    for world in worlds:
        worlds_dic.update(world)
    # with open('suppliers\\ksp\\worlds.json','w') as f:
    #     json.dump(worlds_dic, f)
    
    return worlds_dic

def get_subs_from_world():
    subs = executor(locators['subs_from_worlds'])
    subs_dic: dict = {}
    for sub in subs:
        subs_dic.update(sub)
    return subs_dic

def get_all_brands_list():
    executor(locators['open_full_brands_list'])
    brands_list: list = str(executor(locators['get_brands_list'])[0]).split('\n')
    brands_dict: dict = dict(zip(brands_list[::2], brands_list[1::2]))
    return brands_dict


def get_product(url: str = 'https://ksp.co.il/web/item/227307') -> dict:
    ...

