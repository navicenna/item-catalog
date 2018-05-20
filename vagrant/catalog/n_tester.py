# -*- coding: utf-8 -*-
"""
Created on Sat May 19 11:10:28 2018

@author: Nav
"""

import sqlite3

conn = sqlite3.connect('projectplanner.db')
c = conn.cursor()

query = 'select 1;'
rv = c.execute(query).fetchall()
print("TEST", rv)
print('')

query = 'select * from project;'
rv = c.execute(query).fetchall()
print("PROJECTS", rv)
print('')

query = 'select * from item limit 2;'
rv = c.execute(query).fetchall()
print("ITEMS", rv)
print('')