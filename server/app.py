# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# add views here 
@ app.route('/')
def index():
    response_body = f'<h1>Welcome to the pet directory!</h1>'
    response = make_response(response_body, 200)

    return response

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet:
        response_body = f'{pet.name} {pet.species}'
        response = make_response(response_body, 200)
    else:
        response_body = f'Pet {id} not found'
        response = make_response(response_body, 404)

    return response

@app.route('/pets/<string:species>')
def pet_by_species(species):
    pets = Pet.query.filter_by(species = species).all()
    total = len(pets)
    response_body = f'<h2>There are {total} {species}s'
    for pet in pets:
        response_body += f'<p>{pet.name}</p>'
    response = make_response(response_body, 200)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
