from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)
# Since SQLite is a file DB, need to specify where the file should reside.
# Here, we are making it reside in the same foder as the app.
basedir = os.path.abspath(os.path.dirname(__file__))
# adding some config variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

# adding some test data to the DB to start with
@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=2.258e23,
                     radius=1516,
                     distance=35.98e6)

    venus = Planet(planet_name='Venus',
                         planet_type='Class K',
                         home_star='Sol',
                         mass=4.867e24,
                         radius=3760,
                         distance=67.24e6)

    earth = Planet(planet_name='Earth',
                     planet_type='Class M',
                     home_star='Sol',
                     mass=5.972e24,
                     radius=3959,
                     distance=92.96e6)

    # add records to the DB
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='William',
                     last_name='Herschel',
                     email='test@test.com',
                     password='P@ssw0rd')

    db.session.add(test_user)
    # you have to commit to actually see the DB in the DB
    db.session.commit()
    print("Database seeded!")

@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/super_simple")
def super_simple():
    return jsonify(message="Hello from the planetary API! boo yahhh"), 200

# HTTP status codes
@app.route("/not_found")
def not_found():
    return jsonify(message="that msg was not found."), 404


#URL Parameters
@app.route("/parameters")
def parameters():

    #print(request)
    #import pdb
    #pdb.set_trace()
    name = request.args.get('name')
    # str received to int for age
    
    age = int(request.args.get('age'))

    #print(request, name, age)
    if age<18:
        return jsonify(message= "Sorry " + name + " - you are not old enough."), 401
    else:
        return jsonify(message= "Welcome " + name + ", you are not old enough.")


# Pretty URLs instead of ?, ", &"
@app.route("/url_variables/<string:name>/<int:age>")
def url_variables(name: str, age: int):
    if age<18:
        return jsonify(message= "Sorry " + name + " - you are not old enough."), 401
    else:
        return jsonify(message= "Welcome " + name + ", you are not old enough.")

#DB models
# two tables: users, planets
# ORM takes python objects/class and converts to SQL queries.
class User(db.Model):
    # SQLite creates a table with name = "users"
    __tablename__ = 'users'
    # id = uniquely identifies a record in the DB - primary key
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    # email : should be unique
    email = Column(String, unique=True)
    password = Column(String)

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)