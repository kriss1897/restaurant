import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

class RestaurantHandler:
	def __init__(self):
		pass	
	
	def getAll(self,session):
		restaurants = session.query(Restaurant).getAll()
		output = ""	
		for restaurant in restaurants:
			output += "<div class=\"restaurant\"><h1>%s</h1><a>Edit</a><a>Delete</a></h1></div>" % restaurant.name
			print output


