from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

veggiBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for burger in veggiBurgers:
	print burger.id
	print burger.price
	print burger.restaurant.name
	print "\n"