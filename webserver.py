from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from views import RestaurantViews
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
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

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output =  open('index.html').read()
                self.wfile.write(output)
                return
            elif self.path.endswith("/home"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                restaurants = RestaurantViews()
                output = restaurants.generateHTML()
                self.wfile.write(output)
                return
            elif self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    output = open('/templates/header.html').read()
                    output += "<h1>%s</h1>" % myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'>" % restaurantIDPath 
                    output += "<input name='newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'></form>"
                    output+= open('/templates/footer.html').read() 

            elif self.path.endswith('/add_restaurant'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = open('templates/header.html').read()
                output += open('templates/add_restaurant.html').read()
                output += open('templates/footer.html').read()
                self.wfile.write(output)

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/add_restaurant"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type')) 
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                name = fields.get('name')
                r = Restaurant(name = name[0])
                session.add(r)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                newName - fields.get('newRestaurantName')
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    myRestaurantQuery.name = newName[0]
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type','text-html')
                    self.send_header('Location','/home')
                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()