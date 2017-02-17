from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class RestaurantViews:
	def getRestaurants(self):
		restaurants = session.query(Restaurant)
		output = "<div class='restaurants'>"
		for restaurant in restaurants:
			output +=  "<a href='/%s/menu' style='display:block'>" % restaurant.id
			output += restaurant.name
			output += "</a><a href='/%s/edit'>Edit</a><a href='#'>Delete</a>" % restaurant.id
		output += "</div>"
		return output
	
	def generateHTML(self):
		output = open('templates/header.html').read()
		output += "<a class='add-restaurant' href='/add_restaurant'>Add New Restaurant</a>"
		output += self.getRestaurants()
		output += open('templates/footer.html').read()
		return output

	def getRestaurantById(self,rid):
		return session.query(Restaurant).filter_by(id=rid).one()

	def getFirst(self):
		return session.query(Restaurant).first()

class MenuViews:
	def getMenus(self,restaurant):
		menus = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
		output = "<center><h1>%s Menu</h1></center>"% restaurant.name +"<hr>"
		for menu in menus:
			output += "<p>Name: "+menu.name+"</p>"
			output += "<p>Course: "+menu.course+"</p>"
			output += "<p>Description: "+menu.description+"</p>"
			output += "<p>Price: "+menu.price+"</p>"
			output += "<a href='#'>Edit</a><br/><a href='#'>Delete</a><br/><br/>"
		return output


