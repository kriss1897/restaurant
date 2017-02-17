from flask import Flask,request,redirect,url_for,render_template,flash,jsonify
from controller import RestaurantController,MenuItemController

app = Flask(__name__)
restaurantC = RestaurantController()
menuC = MenuItemController()

@app.route('/')
@app.route('/restaurants')
def ShowRestaurants():
	return restaurantC.getRestaurants()

@app.route('/<int:restaurant_id>/menu')
def ShowMenus(restaurant_id):
	restaurant = restaurantC.getRestaurantById(restaurant_id)
	return menuC.getMenus(restaurant)

@app.route('/<int:restaurant_id>/new_item',methods=['GET','POST'])
def AddMenuItem(restaurant_id):
	if request.method=='POST':
		menuC.addNew(request.form['name'],restaurant_id)
		return redirect(url_for('ShowMenus',restaurant_id=restaurant_id))
	else:
		restaurant = restaurantC.getRestaurantById(restaurant_id)
		return render_template('newmenuitem.html',restaurant=restaurant)

@app.route('/<int:restaurant_id>/<int:menu_id>/edit',methods=['GET','POST'])
def EditMenuItem(restaurant_id,menu_id):
	if request.method == 'POST':
		menuC.editMenu(restaurant_id,menu_id,request.form['name'])
		return redirect(url_for('ShowMenus',restaurant_id=restaurant_id))
	else:
		menu = menuC.getMenuItemById(restaurant_id,menu_id)
		restaurant = restaurantC.getRestaurantById(restaurant_id)
		return render_template('editmenuitem.html',menuItem = menu,restaurant=restaurant)


@app.route('/<int:restaurant_id>/<int:menu_id>/delete',methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
	if request.method == 'POST':
		menuC.deleteMenu(restaurant_id,menu_id)
		return redirect(url_for('ShowMenus',restaurant_id=restaurant_id))
	else:
		menu = menuC.getMenuItemById(restaurant_id,menu_id)
		return render_template('deletemenuitem.html',item=menu)

#Making An API Endpoint(GET Request)
@app.route('/<int:restaurant_id>/menu/JSON')
def restaurantMenusJSON(restaurant_id):
	items = menuC.getEveryMenuItem(restaurant_id)
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/<int:restaurant_id>/<int:menu_id>/JSON')
def restaurantMenuJSON(restaurant_id,menu_id):
	item = menuC.getMenuItemById(restaurant_id,menu_id)
	return jsonify(MenuItems=item.serialize)


if __name__ == '__main__':
	app.secret_key = 'super_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)

