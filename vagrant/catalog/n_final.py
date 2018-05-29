#! /usr/bin/env python3
from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from n_database_setup import Base, Project, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from flask_oauthlib.client import OAuth


# Some code adapted from this flask-oauth example
# https://github.com/lepture/flask-oauthlib/blob/master/example/google.py
# Some general concepts also come from the official 
# Udacity repositories associated with the authentication lesson

app = Flask(__name__)

engine = create_engine('sqlite:///projectplanner.db',
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Configure the OAUTH parameters
app.config['GOOGLE_ID'] =
"825349126192-ujidiia6lfn8vok2o1ep879r37qlrumv.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "mxi8yfVHvvtTDR8fSdFGesAm"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

# Configure google oauth object
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


# Login
@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    google_token = login_session.pop('google_token', None)
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
        google_token)
    result = requests.get(url)

    del login_session['username']
    del login_session['email']
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    login_session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    data = me.data
    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # Create user if doesn't exist
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return redirect(url_for('index'))


@google.tokengetter
def get_google_oauth_token():
    return login_session.get('google_token')


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Build out the JSON API endpoints
@app.route('/project/<int:project_id>/items/JSON')
def ProjectJSON(project_id):
    if 'username' not in login_session:
        return redirect('/')
    items = session.query(Item).filter_by(
        project_id=project_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/project/<int:project_id>/items/<int:item_id>/JSON')
def ProjectItemJSON(project_id, item_id):
    if 'username' not in login_session:
        return redirect('/')
    Project_Item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Project_Item=Project_Item.serialize)


@app.route('/project/JSON')
def allProjectsJSON():
    if 'username' not in login_session:
        return redirect('/')
    projects = session.query(Project).all()
    return jsonify(projects=[r.serialize for r in projects])


# Show all projects
@app.route('/')
@app.route('/project/')
def index():
    projects = session.query(Project).all()
    if 'username' not in login_session:
        return render_template('catalog-main-public.html', projects={})
    else:
        return render_template('catalog-main.html', projects=projects)


# Create a new project
@app.route('/project/new/', methods=['GET', 'POST'])
def newRestaurant():
    if 'username' not in login_session:
        return redirect('/')
    if request.method == 'POST':
        newProject = Project(name=request.form['name'])
        session.add(newProject)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('newProject.html')


# Edit a project
@app.route('/project/<int:project_id>/edit/', methods=['GET', 'POST'])
def editProject(project_id):
    if 'username' not in login_session:
        return redirect('/')
    editedProject = session.query(
        Project).filter_by(id=project_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedProject.name = request.form['name']
            return redirect(url_for('index'))
    else:
        return render_template(
            'editProject.html', project=editedProject)


# Edit a project's name
@app.route('/project/<int:project_id>/edit-name/', methods=['GET', 'POST'])
def editProjectName(project_id):
    if 'username' not in login_session:
        return redirect('/')
    editedProject = session.query(
        Project).filter_by(id=project_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedProject.name = request.form['name']
            return redirect(url_for('index'))
    else:
        return render_template(
            'editProjectName.html', project=editedProject)


# Delete a project
@app.route('/project/<int:project_id>/delete/', methods=['GET', 'POST'])
def deleteProject(project_id):
    if 'username' not in login_session:
        return redirect('/')
    projectToDelete = session.query(Project).filter_by(id=project_id).one()
    if request.method == 'POST':
        session.delete(projectToDelete)
        session.commit()
        return redirect(
            url_for('index', project_id=project_id))
    else:
        return render_template(
            'deleteProject.html', project=projectToDelete)


# Create a new item
@app.route(
    '/project/<int:project_id>/items/new/', methods=['GET', 'POST'])
def newItem(project_id):
    if 'username' not in login_session:
        return redirect('/')
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], project_id=project_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('newItem.html', project_id=project_id)


# Delete an item
@app.route('/project/<int:project_id>/items/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(project_id, item_id):
    if 'username' not in login_session:
        return redirect('/')
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# Edit a menu item
@app.route('/project/<int:project_id>/items/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(project_id, item_id):
    if 'username' not in login_session:
        return redirect('/')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        editedItem.name = request.form['name']
        # session.add(editedItem)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template(
            'editItem.html', project_id=project_id, item=editedItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5566)
