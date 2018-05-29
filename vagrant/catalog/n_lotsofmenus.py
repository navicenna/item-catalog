#! /usr/bin/env python3
# This is a Python script used to fill the item-catalog database with some data
# Code adapted from Udacity Lesson on Iterative Development


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from n_database_setup import Project, Base, Item


engine = create_engine('sqlite:///projectplanner.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# FSND project
project1 = Project(name="Full-Stack Nanodegree")

session.add(project1)
session.commit()

Item1 = Item(name="Item Catalog Project",
             description="Create an item catalog which " +
                         "implements OAuth, CRUD, and Flask.",
             project=project1)
session.add(Item1)
session.commit()

Item2 = Item(name="Learn Front-End Development", 
             description="Become proficient in Ajax, " +
                         "JQuery, and JavaScript.",
             project=project1)
session.add(Item2)
session.commit()


# Actuarial Exam IFM
project2 = Project(name="Pass Exam IFM (Investments " +
                        " and Financial Markets)")

session.add(project2)
session.commit()

Item1 = Item(name="Master the Black-Scholes Formula", description="Do many problems which use the Black-Scholes framework to price options.",
             project=project2)
session.add(Item1)
session.commit()

Item2 = Item(name="Master Exchange Options", description="Become proficient in pricing options on currency exchanges.",
             project=project2)
session.add(Item2)
session.commit()

Item3 = Item(name="Learn How to Price Futures", description="Practice computing the marginal account balance, as well as cumulative gain",
             project=project2)
session.add(Item3)
session.commit()


print("done adding items")
