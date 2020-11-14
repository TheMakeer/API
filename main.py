from flask import jsonify, request
from flask_pymongo import pymongo 
from app import create_app
from bson.json_util import dumps
import db_config as db 

#kaka 

app = create_app()

token = 6516847846548746151

@app.route('/', methods=['GET'])
def show_all_characters():
    characters = list(db.db.mr_robot_characters.find())
    for character in characters:
        del character ["_id"]

    return jsonify({"characters":characters}) 

@app.route('/api/character/<int:id>/', methods=['GET'])
def show_a_character(id):
    character = db.db.mr_robot_characters.find_one({"id":id})
    del character ["_id"]
    if character == 'null':
        return jsonify({
            "status":"404",
            "message":"Character not found"
        })
    else:
        return jsonify({"character":character})


@app.route(f'/api/{token}/new_character/', methods=['POST']) #recibe dos parametros, uno es la ruta a la que queremos acceder y el otro es el metodo con el que trabajaremos  
def add_new_character():
    if len(request.json) == 6:
        db.db.mr_robot_characters.insert_one({
            "id":request.json["id"],
            "name":request.json["name"],
            "actor":request.json["actor"],
            "quote":request.json["quote"],
            "img":request.json["img"],
            "c_status":request.json["c_status"]
    })
    else:
        return jsonify({
            "error":"ERROR",
            "message":"You're missing some data"
        })
    return jsonify({
            "status":200,
            "message":f"{request.json['name']} was added",
        })

@app.route(f'/api/{token}/character/update/<int:id>/', methods=['PUT'])
def update_character(id):

    if db.db.mr_robot_characters.find_one({"id":id}):
        db.db.mr_robot_characters.update_one({"id":id},
        {'$set':{

            "id":request.json["id"],
            "name":request.json["name"],
            "actor":request.json["actor"],
            "quote":request.json["quote"],
            "img":request.json["img"],
            "c_status":request.json["c_status"]
            
                }})
        
    else:
        return jsonify({
            "status":404,
            "message":f"Character # {id} doesn't exist"
        })
    return jsonify({
                "status":200,
                "message":f"The character it's been succesfully updated"
            })

@app.route(f'/api/{token}/character/delete/<int:id>/', methods=['DELETE'])
def del_character(id):
    if db.db.mr_robot_characters.find_one({"id":id}):
        db.db.mr_robot_characters.delete_one({"id":id})
    else:
        return jsonify({
            "status":404,
            "message":f"Character # {id} doesn't exist"
        })
    return jsonify({
                "status":200,
                "message":f"{id} it's been succesfully deleted"
            })


if __name__=='__main__':
    app.run(load_dotenv = True, port=8081)