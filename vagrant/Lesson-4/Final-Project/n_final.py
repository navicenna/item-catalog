from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from n_database_setup import Base, Project, Item

app = Flask(__name__)

engine = create_engine('sqlite:///projectplanner.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/project/<int:project_id>/items/JSON')
def ProjectJSON(project_id):
    project = session.query(Project).filter_by(id=project_id).one()
    items = session.query(Item).filter_by(
        project_id=project_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/project/<int:project_id>/items/<int:item_id>/JSON')
def ProjectItemJSON(project_id, menu_id):
    Project_Item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Project_Item=Project_Item.serialize)


@app.route('/project/JSON')
def allProjectsJSON():
    projects = session.query(Project).all()
    return jsonify(projects=[r.serialize for r in projects])


# Show all projects
@app.route('/')
@app.route('/project/')
def showRestaurants():
    projects = session.query(Category).all()
    # return "This page will show all my restaurants"
    return render_template('restaurants.html', projects=projects)


# # Create a new restaurant
# @app.route('/project/new/', methods=['GET', 'POST'])
# def newRestaurant():
#     if request.method == 'POST':
#         newRestaurant = Restaurant(name=request.form['name'])
#         session.add(newRestaurant)
#         session.commit()
#         return redirect(url_for('showRestaurants'))
#     else:
#         return render_template('newRestaurant.html')
#     # return "This page will be for making a new restaurant"

# # Edit a restaurant


# @app.route('/project/<int:project_id>/edit/', methods=['GET', 'POST'])
# def editRestaurant(project_id):
#     editedRestaurant = session.query(
#         Restaurant).filter_by(id=project_id).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedRestaurant.name = request.form['name']
#             return redirect(url_for('showRestaurants'))
#     else:
#         return render_template(
#             'editRestaurant.html', restaurant=editedRestaurant)

#     # return 'This page will be for editing restaurant %s' % project_id

# # Delete a restaurant


# @app.route('/project/<int:project_id>/delete/', methods=['GET', 'POST'])
# def deleteRestaurant(project_id):
#     restaurantToDelete = session.query(
#         Restaurant).filter_by(id=project_id).one()
#     if request.method == 'POST':
#         session.delete(restaurantToDelete)
#         session.commit()
#         return redirect(
#             url_for('showRestaurants', project_id=project_id))
#     else:
#         return render_template(
#             'deleteRestaurant.html', restaurant=restaurantToDelete)
#     # return 'This page will be for deleting restaurant %s' % project_id


# # Show a restaurant menu
# @app.route('/project/<int:project_id>/')
# @app.route('/project/<int:project_id>/items/')
# def showMenu(project_id):
#     restaurant = session.query(Restaurant).filter_by(id=project_id).one()
#     items = session.query(MenuItem).filter_by(
#         project_id=project_id).all()
#     return render_template('menu.html', items=items, restaurant=restaurant)
#     # return 'This page is the menu for restaurant %s' % project_id

# # Create a new menu item


# @app.route(
#     '/project/<int:project_id>/items/new/', methods=['GET', 'POST'])
# def newMenuItem(project_id):
#     if request.method == 'POST':
#         newItem = MenuItem(name=request.form['name'], description=request.form[
#                            'description'], price=request.form['price'], course=request.form['course'], project_id=project_id)
#         session.add(newItem)
#         session.commit()

#         return redirect(url_for('showMenu', project_id=project_id))
#     else:
#         return render_template('newmenuitem.html', project_id=project_id)

#     return render_template('newMenuItem.html', restaurant=restaurant)
#     # return 'This page is for making a new menu item for restaurant %s'
#     # %project_id

# # Edit a menu item


# @app.route('/project/<int:project_id>/items/<int:item_id>/edit',
#            methods=['GET', 'Project_Item'])
# def editMenuItem(oject_id, menu_id):item editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedItem.name = request.form['name']
#         if request.form['description']:
#             editedItem.description = request.form['name']
#         if request.form['price']:
#             editedItem.price = request.form['price']
#         if request.form['course']:
#             editedItem.course = request.form['course']
#         session.add(editedItem)
#         session.commit()
#         return redirect(url_for('showMenu', project_id=project_id))
#     else:

#         return render_template(
#             'editmenuitem.html', project_id=project_id, menu_id=menu_id, item=editedItem)

#     # return 'This page is for editing menu item %s' % menu_id

# # Delete a menu item


# @app.route('/project/<int:project_id>/items/<int:item_id>/delete',
#            methods=['GET', 'Project_Item'])
# def deleteMenuItem(oject_id, menu_id):item itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
#     if request.method == 'POST':
#         session.delete(itemToDelete)
#         session.commit()
#         return redirect(url_for('showMenu', project_id=project_id))
#     else:
#         return render_template('deleteMenuItem.html', item=itemToDelete)
#     # return "This page is for deleting menu item %s" % menu_id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
