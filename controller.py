from flask import render_template, url_for,flash

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class RestaurantController:
	def getRestaurants(self):
		restaurants = session.query(Restaurant)
		return render_template('restaurant.html',restaurants=restaurants)

	def getRestaurantById(self,rid):
		return session.query(Restaurant).filter_by(id=rid).one()

	def getFirst(self):
		return session.query(Restaurant).first()


class MenuItemController:
	def getMenus(self,restaurant):
		menus = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
		output = "<center><h1>%s Menu</h1></center>"% restaurant.name +"<hr>"
		return render_template('menu.html',restaurant=restaurant,items=menus)

	def getMenuItemById(self,r_id,m_id):
		return session.query(MenuItem).filter_by(id=m_id,restaurant_id=r_id).first()

	def addNew(self,name,r_id):
		newItem = MenuItem(name=name,restaurant_id=r_id)
		session.add(newItem)
		session.commit()
		flash("New Menu Item Created")

	def editMenu(self,r_id,m_id,name):
		menuItem = self.getMenuItemById(r_id,m_id)
		menuItem.name = name
		session.add(menuItem)
		session.commit()
		flash("Item Successfully Edited")

	def deleteMenu(self,r_id,m_id):
		menuItem = self.getMenuItemById(r_id,m_id)
		session.delete(menuItem)
		session.commit()
		flash("Item Successfully Deleted")

	def getEveryMenuItem(self,r_id):
		return session.query(MenuItem).filter_by(restaurant_id=r_id).all()

