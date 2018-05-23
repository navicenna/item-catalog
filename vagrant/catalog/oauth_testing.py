from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from n_database_setup import Base, Project, Item
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


app = Flask(__name__)

engine = create_engine('sqlite:///projectplanner.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Adapted from this flask-oauth example https://github.com/lepture/flask-oauthlib/blob/master/example/google.py

app.config['GOOGLE_ID'] = "825349126192-ujidiia6lfn8vok2o1ep879r37qlrumv.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "mxi8yfVHvvtTDR8fSdFGesAm"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

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


@app.route('/')
def index():
    if 'google_token' in login_session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    login_session.pop('google_token', None)
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
    return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return login_session.get('google_token')





# # Show all projects
# @app.route('/')
# @app.route('/project/')
# def showProjects():
#     projects = session.query(Project).all()
#     # return "This page will show all my restaurants"
#     return render_template('catalog-main.html', projects=projects)


# # Create anti-forgery state token
# @app.route('/login')
# def showLogin():
#     state = ''.join(random.choice(string.ascii_uppercase + string.digits)
#                     for x in range(32))
#     login_session['state'] = state
#     # return "The current session state is %s" % login_session['state']
#     return render_template('login.html', STATE=state)







if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5566)
