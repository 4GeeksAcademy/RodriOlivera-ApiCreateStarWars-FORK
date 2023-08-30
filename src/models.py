from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer ,primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250),nullable=False)
    subscription_date = db.Column(db.DATE,nullable = False)
    email = db.Column(db.String(250),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    
    # Relacion con fav 
    Favorito = db.relationship('Favorite', backref='user', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "subscription_date": self.subscription_date,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.Integer,nullable=False)
    orbital_period = db.Column(db.Integer,nullable=False)
    diameter = db.Column(db.Float,nullable=False)
    climate = db.Column(db.String(50))
    gravity = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
    population = db.Column(db.Integer,nullable=False)
    
    Favorito = db.relationship('Favorite', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            # do not serialize the password, its a security breach
        }

class Starships(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    model =  db.Column(db.String(250), nullable=False)
    manufacturer =  db.Column(db.String(250) )
    cost_in_credits =  db.Column(db.Float,nullable=False)
    length =  db.Column(db.Float,nullable=False )
    max_atmosphering_speed = db.Column(db.Integer,nullable=False)
    crew =  db.Column(db.String(250),nullable=False )
    passengers =  db.Column(db.Integer,nullable=False )
    cargo_capacity =  db.Column(db.Float,nullable=False)
    consumables =  db.Column(db.Integer,nullable=False)
    hyperdrive_rating =  db.Column(db.Float)
    MGLT =  db.Column(db.Integer,nullable=False)
    starship_class =  db.Column(db.String(200))

    Favorito = db.relationship('Favorite', backref='starships', lazy=True)

    # Relacion 
    def __repr__(self):
        return '<Starships %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "starship_class": self.starship_class
            # do not serialize the password, its a security breach
        }


class Vehicles(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    model =  db.Column(db.String(250), nullable=False)
    manufacturer =  db.Column(db.String(250) )
    cost_in_credits =  db.Column(db.Float,nullable=False)
    length =  db.Column(db.Float,nullable=False )
    max_atmosphering_speed = db.Column(db.Integer,nullable=False)
    crew =  db.Column(db.String(250),nullable=False )
    passengers =  db.Column(db.Integer,nullable=False )
    cargo_capacity =  db.Column(db.Float,nullable=False)
    consumables =  db.Column(db.Integer,nullable=False)
    vehicle_class =  db.Column(db.String(200))

    Favorito = db.relationship('Favorite', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "vehicle_class": self.vehicle_class,
            # do not serialize the password, its a security breach
        }
    


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Float, nullable=False)
    hair_color = db.Column(db.String(), nullable=False)
    skin_color = db.Column(db.String(), nullable=False)
    eye_color = db.Column(db.String(), nullable=False)
    birth_year = db.Column(db.Date ,nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    homeworld = db.Column(db.String(100), nullable=False)

    Favorito = db.relationship('Favorite', backref='characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.id
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            # do not serialize the password, its a security breach
        }
    

class Favorite(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    id_characters = db.Column(db.Integer, db.ForeignKey('characters.id'),nullable=True)
    id_planets = db.Column(db.Integer, db.ForeignKey('planets.id'),nullable=True)
    id_vehicles = db.Column(db.Integer, db.ForeignKey('vehicles.id'),nullable=True)
    id_starships = db.Column(db.Integer, db.ForeignKey('starships.id'),nullable=True) 


    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "id_characters": self.id_characters,
            "id_planets": self.id_planets,
            "id_vehicles": self.id_vehicles,
            "id_starships": self.id_starships,
        }

