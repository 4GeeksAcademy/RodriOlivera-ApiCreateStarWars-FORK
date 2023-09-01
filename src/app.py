"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Characters,Planets,Vehicles,Starships,Favorite
import datetime

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Peticion para usuarios y usuario espesifico
@app.route('/user',methods=["GET"])
def Obtener_Usuario():
    #generamos la consulta
    usuarios_query = User.query.all()

    #pasamos cada usuario a formato que podamos ver
    result = list(map(lambda item:item.serialize(),usuarios_query))

    response_body = {
        "msg":"hay usuarios",
        "results":result
    }

    if len(result) == 0:
        return jsonify({"msg":"No hay usuarios"}),404
    else:
        return jsonify(response_body),200


@app.route('/user/<int:idUser>')
def Obtener_Usuario_Espesifico(idUser):
    print("xd")
    #generamos la consulta
    usuario_query = User.query.filter_by(id=idUser).first()

    if usuario_query == None :
        return jsonify({"msg":"No hay usuario con ese id"}),404
    else: 
        return jsonify({"msg":"el usuario existe","result":usuario_query.serialize()})



# Peticion para planeta y planeta espesifico, insertar planeta, actualizar y borrar
@app.route('/planets',methods=["GET"])
def Obtener_Planetas():
    #generamos la consulta
    planetas_query = Planets.query.all()

    #pasamos cada usuario a formato que podamos ver
    result = list(map(lambda item:item.serialize(),planetas_query))

    response_body = {
        "msg":"hay planetas",
        "results":result
    }

    if len(result) == 0:
        return jsonify({"msg":"No hay planetas"}),404
    else:
        return jsonify(response_body),200

    #insertar un planeta
@app.route("/planets",methods=["POST"])
def InsertarPeople():
    request_body = request.json
    
    planetExist = Planets.query.filter_by(name=request_body["name"]).first()

    if planetExist == None:
        newPlanet = Planets(
            name=request_body["name"],
            rotation_period=request_body["rotation_period"],
            orbital_period=request_body["orbital_period"],
            diameter=request_body["diameter"],
            climate=request_body["climate"],
            gravity=request_body["gravity"],
            terrain=request_body["terrain"],
            surface_water=request_body["surface_water"],
            population=request_body["population"]
        )
    else:
        return jsonify({"msg":"Este planeta ya existe"})
    
    db.session.add(newPlanet)
    db.session.commit()

    return jsonify({"msg":"Planeta insertado correctamente"}),200

    #Actualizar un planeta
@app.route("/planets/<int:id_planet>",methods = ["PUT"])
def ActualizarPlaneta(id_planet):
    data = request.json
    planet = Planets.query.filter_by(id=id_planet).first()
    if planet == None:
        return jsonify({"msg":"El planeta no existe"})
    
    planet.name=data["name"],
    planet.rotation_period=data["rotation_period"],
    planet.orbital_period=data["orbital_period"],
    planet.diameter=data["diameter"],
    planet.climate=data["climate"],
    planet.gravity=data["gravity"],
    planet.terrain=data["terrain"],
    planet.surface_water=data["surface_water"],
    planet.population=data["population"]

    db.session.commit()

    return jsonify({"msg":"El planeta se actualizo correctamente"})



    #Eliminar un planeta
@app.route("/planets/<int:id_planet>",methods = ["DELETE"])
def BorrarPlanets(id_planet):
    planetExist = Planets.query.filter_by(id=id_planet).first()
    if planetExist == None:
        return jsonify({"msg":"El Planeta no existe"})
    db.session.delete(planetExist)
    db.session.commit()
    return jsonify({"msg":"El planeta se borro"})

    #Planeta espesifico 
@app.route('/planets/<int:idPlanet>')
def Obtener_Planeta_Espesifico(idPlanet):
    print("xd")
    #generamos la consulta
    Planets_query = Planets.query.filter_by(id=idPlanet).first()

    if Planets_query == None :
        return jsonify({"msg":"No hay Planeta con ese id"}),404
    else: 
        return jsonify({"msg":"el planeta existe","result":Planets_query.serialize()}),200


    


# Peticion para starships y starship espesifico
@app.route('/starships',methods=["GET"])
def Obtener_StarShips():
    #generamos la consulta
    starships_query = Starships.query.all()

    #pasamos cada usuario a formato que podamos ver
    result = list(map(lambda item:item.serialize(),starships_query))

    response_body = {
        "msg":"hay naves",
        "results":result
    }

    if len(result) == 0:
        return jsonify({"msg":"No hay naves"}),404
    else:
        return jsonify(response_body),200



@app.route('/starships/<int:idStarShip>')
def Obtener_StarShip_Espesifica(idStarShip):
    print("xd")
    #generamos la consulta
    Starships_query = Starships.query.filter_by(id=idStarShip).first()

    if Starships_query == None :
        return jsonify({"msg":"No hay Nave con ese id"}),404
    else: 
        return jsonify({"msg":"la nave existe","result":Starships_query.serialize()}),200

    #Insertar Starship
@app.route("/starships",methods=["POST"])
def InsertarStarShip():
    request_body = request.json
    
    starShipExist = Starships.query.filter_by(name=request_body["name"]).first()

    if starShipExist == None:
        newStarShip = Starships(
            name = request_body["name"],
	        model = request_body["model"],
	        manufacturer = request_body["manufacturer"],
	        cost_in_credits = request_body["cost_in_credits"],
	        length = request_body["length"],
	        max_atmosphering_speed = request_body["max_atmosphering_speed"],
	        crew = request_body["crew"],
	        passengers = request_body["passengers"],
	        cargo_capacity = request_body["cargo_capacity"],
	        consumables = request_body["consumables"],
	        hyperdrive_rating = request_body["hyperdrive_rating"],
	        MGLT = request_body["hyperdrive_rating"],
	        starship_class = request_body["starship_class"]
        )
    else:
        return jsonify({"msg":"Esta Nave ya existe"})
    
    db.session.add(newStarShip)
    db.session.commit()

    return jsonify({"msg":"Nave insertada correctamente"}),200


    #Actualizar starship
@app.route("/starships/<int:id_starship>",methods = ["PUT"])
def ActualizarStarShip(id_starship):
    data = request.json
    starshipsExist = Starships.query.filter_by(id=id_starship).first()
    if starshipsExist == None:
        return jsonify({"msg":"La Nave no existe"})
    

    starshipsExist.name=data["name"],
    starshipsExist.model=data["model"],
    starshipsExist.manufacturer=data["manufacturer"],
    starshipsExist.cost_in_credits=data["cost_in_credits"],
    starshipsExist.length=data["length"],
    starshipsExist.max_atmosphering_speed=data["max_atmosphering_speed"],
    starshipsExist.crew=data["crew"],
    starshipsExist.passengers=data["passengers"],
    starshipsExist.cargo_capacity=data["cargo_capacity"],
    starshipsExist.consumables=data["consumables"],
    starshipsExist.MGLT=data["MGLT"] 
    starshipsExist.hyperdrive_rating=data["hyperdrive_rating"] 
    starshipsExist.starship_class=data["starship_class"] 
    
    db.session.commit()

    return jsonify({"msg":"El vehicle se actualizo correctamente"})

    #Borrar character
@app.route("/starships/<int:id_starships>",methods = ["DELETE"])
def BorrarStarships(id_starships):
    starShipExist = Starships.query.filter_by(id=id_starships).first()
    if starShipExist == None:
        return jsonify({"msg":"La Nave no existe"})
    db.session.delete(starShipExist)
    db.session.commit()
    return jsonify({"msg":"La Nave se borro"})



# Peticion para Vehiculos y Vehiculo espesifico
@app.route('/vehicles',methods=["GET"])
def Obtener_Vehicles():
    #generamos la consulta
    Vehicles_query = Vehicles.query.all()

    #pasamos cada usuario a formato que podamos ver
    result = list(map(lambda item:item.serialize(),Vehicles_query))

    response_body = {
        "msg":"hay Vehiculos",
        "results":result
    }

    if len(result) == 0:
        return jsonify({"msg":"No hay vehiculos"}),404
    else:
        return jsonify(response_body),200
    
    #Insertar Vehiculo
@app.route("/vehicles",methods=["POST"])
def InsertarVehicle():
    request_body = request.json
    
    vehicleExist = Vehicles.query.filter_by(name=request_body["id"]).first()

    if vehicleExist == None:
        newVehicle = Vehicles(
            name=request_body["name"],
            model=request_body["model"],
            manufacturer=request_body["manufacturer"],
            cost_in_credits=request_body["cost_in_credits"],
            length=request_body["length"],
            max_atmosphering_speed=request_body["max_atmosphering_speed"],
            crew=request_body["crew"],
            passengers=request_body["passengers"],
            cargo_capacity=request_body["cargo_capacity"],
            consumables=request_body["consumables"],
            vehicle_class=request_body["vehicle_class"] 
        )
    else:
        return jsonify({"msg":"Este vehiculo ya existe"})
    
    db.session.add(newVehicle)
    db.session.commit()

    return jsonify({"msg":"Planeta insertado correctamente"}),200

    

    #Actualizar Vehiculo
@app.route("/vehicles/<int:id_vehicle>",methods = ["PUT"])
def ActualizarVehicle(id_vehicle):
    data = request.json
    vehicle = Vehicles.query.filter_by(id=id_vehicle).first()
    if vehicle == None:
        return jsonify({"msg":"El vehiclea no existe"})
    
    vehicle.name=data["name"],
    vehicle.model=data["model"],
    vehicle.manufacturer=data["manufacturer"],
    vehicle.cost_in_credits=data["cost_in_credits"],
    vehicle.length=data["length"],
    vehicle.max_atmosphering_speed=data["max_atmosphering_speed"],
    vehicle.crew=data["crew"],
    vehicle.passengers=data["passengers"],
    vehicle.cargo_capacity=data["cargo_capacity"],
    vehicle.consumables=data["consumables"],
    vehicle.vehicle_class=data["vehicle_class"] 

    db.session.commit()

    return jsonify({"msg":"El vehicle se actualizo correctamente"})


    #Borrar Vehiculo 
@app.route("/vehicles/<int:id_vehicle>",methods = ["DELETE"])
def BorrarVehiculo(id_vehicle):
    vehicleExist = Vehicles.query.filter_by(id=id_vehicle).first()
    if vehicleExist == None:
        return jsonify({"msg":"El vehiculo no existe"})
    db.session.delete(vehicleExist)
    db.session.commit()
    return jsonify({"msg":"El vehiculo se borro"})
    


    #Vehiculo espesifico
@app.route('/vehicles/<int:idVehicle>')
def Obtener_Vehicle_Espesifica(idVehicle):
    #generamos la consulta
    Vehicles_query = Vehicles.query.filter_by(id=idVehicle).first()

    if Vehicles_query == None :
        return jsonify({"msg":"No hay Vehiculo con ese id"}),404
    else: 
        return jsonify({"msg":"El vehiculo existe","result":Vehicles_query.serialize()}),200



# Peticion para Personajes y Personaje espesifico
@app.route('/characters',methods=["GET"])
def Obtener_Personaje():
    #generamos la consulta
    Personaje_query = Characters.query.all()

    #pasamos cada usuario a formato que podamos ver
    result = list(map(lambda item:item.serialize(),Personaje_query))

    response_body = {
        "msg":"hay personajes",
        "results":result
    }

    if len(result) == 0:
        return jsonify({"msg":"No hay personajes"}),404
    else:
        return jsonify(response_body),200


@app.route('/characters/<int:idPj>')
def Obtener_Personaje_Espesifica(idPj):
    #generamos la consulta
    Personaje_query = Characters.query.filter_by(id=idPj).first()

    if Personaje_query == None :
        return jsonify({"msg":"No hay Pj con ese id"}),404
    else: 
        return jsonify({"msg":"El Pj existe","result":Personaje_query.serialize()}),200
    #Insertar character
    #Insertar Vehiculo
@app.route("/characters",methods=["POST"])
def InsertarCharacter():
    request_body = request.json
    
    characterExist = Characters.query.filter_by(name=request_body["name"]).first()

    if characterExist == None:
        newCharacter = Characters(
            birth_year = request_body["birth_year"],
            eye_color = request_body["eye_color"],
            gender = request_body["gender"],
            hair_color = request_body["hair_color"],
            height = request_body["height"],
            homeworld = request_body["homeworld"],
            name = request_body["name"],
            skin_color = request_body["skin_color"],
        )
    else:
        return jsonify({"msg":"Este Personaje ya existe"})
    
    db.session.add(newCharacter)
    db.session.commit()

    return jsonify({"msg":"Personaje insertado correctamente"}),200



    #Actualizar character
@app.route("/characters/<int:id_character>",methods = ["PUT"])
def ActualizarCharacter(id_character):
    data = request.json
    character = Characters.query.filter_by(id=id_character).first()
    if character == None:
        return jsonify({"msg":"El character no existe"})
    

    character.birth_year= data["birth_year"]
    character.eye_color= data["eye_color"]
    character.gender= data["gender"]
    character.hair_color= data["hair_color"]
    character.height= data["height"]
    character.homeworld: data["homeworld"]
    character.name= data["name"],
    character.skin_color=data["skin_color"]

    db.session.commit()

    return jsonify({"msg":"El Personaje se actualizo correctamente"})

    #Borrar character
@app.route("/characters/<int:id_character>",methods = ["DELETE"])
def BorrarCharacter(id_character):
    characterExist = Characters.query.filter_by(id=id_character).first()
    if characterExist == None:
        return jsonify({"msg":"El Personaje no existe"})
    db.session.delete(characterExist)
    db.session.commit()
    return jsonify({"msg":"El Personaje se borro"})

#  Añade un nuevo planeta favorito al usuario actual con el planet id = planet_id.
@app.route("/user/favorite/planet/<int:planet_id>",methods=["POST"])
def InsertarPlanetaFav(planet_id):
    #Validar si el usuario existe y el planeta
    infoBody = request.json
    user = User.query.filter_by(id=infoBody["id_user"]).first()
    planet = Planets.query.filter_by(id=planet_id).first()

    if user == None:
        return jsonify({"msg":"el usuario no existe"}),404
    elif planet == None:
        return jsonify({"msg":"El planeta no existe"}),404
    
    # ahora validaremos que pueda insertarlo solo si no lo tiene en favs
    favExist = Favorite.query.filter_by(id_user =infoBody["id_user"], id_planets = planet_id).first()
    if favExist == None:
        newFavorite = Favorite(id_user=infoBody["id_user"],id_planets=planet_id)
        db.session.add(newFavorite)
        db.session.commit()
 
        response_body = {
            "msg":"Planeta Añadido a favoritos"
        }
        return jsonify(response_body),200
    return jsonify({"msg":"Ya lo tienes en favoritos"}),404


#Añade una nueva Characters favorita al usuario actual con el people.id = people_id.

@app.route("/user/favorite/characters/<int:character_id>",methods=["POST"])
def InsertarCharacterFavorite(character_id):
    #Validar si el usuario existe y el planeta
    infoBody = request.json
    user = User.query.filter_by(id=infoBody["id_user"]).first()
    character = Characters.query.filter_by(id=character_id).first()

    if user == None:
        return jsonify({"msg":"el usuario no existe"}),404
    elif character == None:
        return jsonify({"msg":"El personaje no existe"}),404
    
    # ahora validaremos que pueda insertarlo solo si no lo tiene en favs
    favExist = Favorite.query.filter_by(id_user =infoBody["id_user"], id_characters = character_id).first()
    if favExist == None:
        newFavorite = Favorite(id_user=infoBody["id_user"],id_characters=character_id)
        db.session.add(newFavorite)
        db.session.commit()
    
        response_body = {
            "msg":"Personaje Añadido a favoritos"
        }
        return jsonify(response_body),200
    return jsonify({"msg":"Ya tienes este personaje en favoritos"}),404


# Elimina un planet favorito con el id = planet_id
@app.route("/user/favorite/planet/<int:planet_id>",methods=["DELETE"])
def BorrarPlanetFavorito(planet_id):
    #Validar si el usuario existe y el planeta
    infoBody = request.json
    user = User.query.filter_by(id=infoBody["id_user"]).first()
    planet = Planets.query.filter_by(id=planet_id).first()

    if user == None:
        return jsonify({"msg":"el usuario no existe"}),404
    elif planet == None:
        return jsonify({"msg":"El planeta no existe"}),404
    
    # ahora validaremos que pueda insertarlo solo si no lo tiene en favs
    favExist = Favorite.query.filter_by(id_user =infoBody["id_user"], id_planets = planet_id).first()
    if favExist == None:
        return jsonify({"msg":"no existe este registro en favoritos"}),404
    
    db.session.delete(favExist)
    db.session.commit()
    response_body = {
        "msg":"Planeta Eliminado Correctamente de Favs"
    }
    return jsonify(response_body),200


# Elimina una people favorita con el id = people_id.
@app.route("/user/favorite/characters/<int:character_id>",methods=["DELETE"])
def BorrarPeopleFavorito(character_id):
    #Validar si el usuario existe y el planeta
    infoBody = request.json
    user = User.query.filter_by(id=infoBody["id_user"]).first()
    character = Planets.query.filter_by(id=character_id).first()

    if user == None:
        return jsonify({"msg":"el usuario no existe"}),404
    elif character == None:
        return jsonify({"msg":"El personaje no existe"}),404
    
    # ahora validaremos que pueda insertarlo solo si no lo tiene en favs
    favExist = Favorite.query.filter_by(id_user =infoBody["id_user"], id_characters = character_id).first()
    if favExist == None:
        return jsonify({"msg":"no existe este registro en favoritos"}),404
    
    db.session.delete(favExist)
    db.session.commit()
    response_body = {
        "msg":"Personaje Eliminado Correctamente de Favs"
    }
    return jsonify(response_body),200

#Registrar Usuario
@app.route("/register",methods = ["POST"])
def RegisterUser():
    bodyInfo = request.json
    name = bodyInfo["name"]
    lastname = bodyInfo["lastname"]
    subscription_date = datetime.datetime.now()
    email = bodyInfo["email"]
    password = bodyInfo["password"]
    #Validar si el email ya existe , si existe deberiamos de decirle al usuario que ingrese una nueva
    emailExist = User.query.filter_by(email=email).first()
    if emailExist == None:
        print("No existe")
        user = User(
        name = name,
        lastname = lastname,
        subscription_date = subscription_date,
        email = email,
        password = password
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg":"Usuario creado"}),200
    return jsonify({"msg":"Debe de ingresar un correo inexistente "}),404



# Login
@app.route("/login",methods = ["POST"])
def Loginuser():
    bodyInfo = request.json
    email = bodyInfo["email"]
    password = bodyInfo["password"]
    # traigo el usuario en base al email
    user = User.query.filter_by(email=email).first()
    #chekeo si ese usuario existe
    if user != None:
        userCheck = user.serialize()
        print(userCheck)
        if email == userCheck["email"] and password == userCheck["password"]:
            access_token = create_access_token(identity=email)
            return jsonify({"msg":"Login Correcto","token":access_token}),200
        return jsonify({"msg":"Error en las credenciales."})

    return jsonify({"msg":"No hay ningun usuario con este email"}),404

# Listar todos los favoritos que pertenecen al usuario actual
@app.route('/user/<int:idUser>/favorite',methods=["GET"])
@jwt_required()
def Obtener_Favoritos_User(idUser):
    current_user = get_jwt_identity()
    #generamos la consulta
    user = User.query.filter_by(id=idUser).first()
    query_user_Favorites = Favorite.query.filter_by(id_user=idUser).all()

    if user == None:
        return jsonify({"msg":"El usuario no existe"})
    
    if query_user_Favorites == []:
        return jsonify({"msg":"Este usuario no tiene ningun favorito"})
    else : 
        result = list(map(lambda item:item.serialize(),query_user_Favorites))
        return jsonify({"msg":"estos son los favoritos del usuario","result":result,"user":current_user}),200 
            


#Ruta favorito protegida


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
