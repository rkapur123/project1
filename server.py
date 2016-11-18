#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the postgresql test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/postgres
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# Swap out the URI below with the URI for the database created in part 2
DATABASEURI = "postgresql://aah2183:zfxw7@104.196.175.120/postgres"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
#
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
#
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
#
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
#engine.execute("""DROP TABLE IF EXISTS test;""")
#engine.execute("""CREATE TABLE IF NOT EXISTS test (id serial, name text);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper');""")
#engine.execute("""INSERT INTO test(name) VALUES ('alan turing');""")
#engine.execute("""INSERT INTO test(name) VALUES ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    print "Did Connect"
    g.conn = engine.connect()
    print "Did Connect"
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#

@app.route('/airplanes')
def airplanes():
  return render_template('airplanes.html')






@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  print "In index"
  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT * FROM air_staff ")
  names = []
  for result in cursor:
    print "This is result " + str(result)
    names.append(result)
    #names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  print names
  return render_template("index.html", names=names)


@app.route('/airport')
def airport():
  cursor = g.conn.execute("SELECT * FROM airport")
  airportList = []
  for result in cursor:
    airportList.append(result)
  cursor.close()
  print airportList

  return render_template('airport.html', airportList = airportList)


@app.route('/terminals')
def terminals():
  cursor = g.conn.execute("SELECT * FROM terminals")
  terminalList = []

  for result in cursor:
      counter = 0
      rowList = []
      for item in result:
          counter = counter + 1
          if (counter == 2):
              emptyString = ""
              for elements in item:
                  emptyString = emptyString + str(elements) + " ,"
              rowList.append(emptyString)
          else:
              rowList.append(item)
      terminalList.append(rowList)

  cursor.close()

  return render_template('terminals.html', terminalList = terminalList)



@app.route('/airlines')
def airlines():
  cursor = g.conn.execute("SELECT * FROM airlines")
  airlinesList = []

  for result in cursor:
      counter = 0
      rowList = []
      for item in result:
          counter = counter + 1
          if (counter == 3):
              emptyString = ""
              for elements in item:
                  emptyString = emptyString + str(elements) + " ,"
              rowList.append(emptyString)
          else:
              rowList.append(item)
      airlinesList.append(rowList)
  cursor.close()

  return render_template('airlines.html', airlinesList = airlinesList)


@app.route('/airstaff')
def airstaff():
  #cursor = g.conn.execute("SELECT * FROM all_staff a AND onground g where a.staffID == g.staffID")
  cursor = g.conn.execute("SELECT * FROM air_staff")
  airstaffList = []
  for result in cursor:
    airstaffList.append(result)
  cursor.close()
  return render_template('airstaff.html', airstaffList = airstaffList)

@app.route('/onground')
def onground():
  cursor = g.conn.execute("SELECT * FROM on_ground")
  ongroundList = []
  for result in cursor:
    ongroundList.append(result)
  cursor.close()
  return render_template('onground.html', ongroundList = ongroundList)

@app.route('/locations/')
def locations():
  cursor = g.conn.execute("SELECT * FROM locations")
  locationList = []
  for result in cursor:
    rowList = []
    locationName = result[2]
    layoverDestinationString = ""
    print result[1]
    if result[1] == True:
        layoverDestinationString = "Layover"
    else:
        layoverDestinationString = "Destination"
    rowList.append(locationName)
    rowList.append(layoverDestinationString)
    locationList.append(rowList)
  print locationList
  cursor.close()
  return render_template('locations.html', locationList = locationList)

@app.route('/locations/layovers')
def locations_layovers():
  cursor = g.conn.execute("SELECT * FROM locations WHERE islayover")
  locationList = []
  for result in cursor:
    rowList = []
    locationName = result[2]
    layoverDestinationString = ""
    print result[1]
    if result[1] == True:
        layoverDestinationString = "Layover"
    else:
        layoverDestinationString = "Destination"
    rowList.append(locationName)
    rowList.append(layoverDestinationString)
    locationList.append(rowList)
  print locationList
  cursor.close()
  return render_template('locations.html', locationList = locationList)

@app.route('/locations/destinations')
def locations_destinations():
  cursor = g.conn.execute("SELECT * FROM locations WHERE isdestination")
  locationList = []
  for result in cursor:
    rowList = []
    locationName = result[2]
    layoverDestinationString = ""
    print result[1]
    if result[1] == True:
        layoverDestinationString = "Layover"
    else:
        layoverDestinationString = "Destination"
    rowList.append(locationName)
    rowList.append(layoverDestinationString)
    locationList.append(rowList)
  print locationList
  cursor.close()
  return render_template('locations.html', locationList = locationList)

@app.route('/passenger.html')
def passenger():
  cursor = g.conn.execute("SELECT * FROM passengers")
  passengerList = []
  for result in cursor:
    passengerList.append(result)
  cursor.close()
  return render_template('passenger.html', passengerList = passengerList)

@app.route('/people.html')
def people():
  cursor = g.conn.execute("SELECT * FROM person")
  personList = []
  for result in cursor:
    personList.append(result)
  cursor.close()
  return render_template('people.html', personList = personList)

@app.route('/planes.html')
def planes():
  cursor = g.conn.execute("SELECT * FROM planes")
  planeList = []
  for result in cursor:
    planeList.append(result)
  cursor.close()
  return render_template('planes.html', planeList = planeList)

@app.route('/allstaff.html')
def allstaff():
  cursor = g.conn.execute("SELECT * FROM staff")
  allStaffList = []
  for result in cursor:
    allStaffList.append(result)
  cursor.close()
  return render_template('allstaff.html', allStaffList = allStaffList)


#
# This is an example of a different path.  You can see it at
#
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/another')
def another():
  return render_template("anotherfile.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  print name
  cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
  g.conn.execute(text(cmd), name1 = name, name2 = name);
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
