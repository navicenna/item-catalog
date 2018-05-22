# -*- coding: utf-8 -*-
"""
Created on Sat May 19 11:10:28 2018

@author: Nav
"""

import sqlite3
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from n_database_setup import Base, Project, Item


conn = sqlite3.connect('projectplanner.db')
c = conn.cursor()

engine = create_engine('sqlite:///projectplanner.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

query = 'select 1;'
rv = c.execute(query).fetchall()
#print("TEST", rv)
#print('')

query = 'select * from project;'
rv = c.execute(query).fetchall()
#print("PROJECTS", rv)
#print('')

query = 'select * from item limit 2;'
rv = c.execute(query).fetchall()
#print("ITEMS", rv)
#print('')

project = session.query(Project).all()
items = session.query(Item).filter_by(project_id=1).all()

for p in project:
    print('foo')
    print(p.name)
    for i in p.items:
        print(i.name)