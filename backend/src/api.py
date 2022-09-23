import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from jose import jwt

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def getDrinks():
    drinks = Drink.query.all()
    
    theDrinks = [drink.short() for drink in drinks]
    
    return jsonify({
        'success': True,
        'drinks': theDrinks
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinkDetails(payload):
    drinks = Drink.query.all()
    
    theDrinks = [drink.long() for drink in drinks]
    print(payload)
    return jsonify({
        'success': True,
        'drinks': theDrinks
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def postDrink(payload):
    body = request.get_json()

    newTitle = body.get("title", None)
    newRecipe = json.dumps(body.get("recipe", None))
    
    try:
        drink = Drink(
            title=newTitle,
            recipe=newRecipe
        )
        drink.insert()
        theDrink = [drink.long()]
        
        print(payload)
        return jsonify(
            {
                "success": True,
                'drinks': theDrink,
                "created": drink.id,
            }
        )
    except Exception:
        abort(422)
    


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def editDrink(payload, drink_id):
    body = request.get_json()
    
    try:
        # get the drink with the provided ID
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        
        # if no drink with the provided drink ID, abort with 404 status code
        if drink is None:
            abort(404)
        
        # get new details for the drink and update it
        drink.title = body['title']
        drink.recipe = json.dumps(body.get('recipe'))
        drink.update()
        
        theDrink = [drink.long()]
        return jsonify({
            'success': True,
            'drinks': theDrink
        })
    except:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        # get the drink with the provided ID
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        
        # if no drink with the provided drink ID, abort with 404 status code
        if drink is None:
            abort(404)
        
        # else Delete The Drink
        drink.delete()
        
        return jsonify(
            {
                "success": True,
                "deleted": drink_id
            }
        )
            
    except:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with appropriate messages):
            jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": 404,
        "success": False,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def authentication_Error(auth_error):
    return jsonify({
        "error": auth_error.status_code,
        "success": False,
        "message": auth_error.error
    }), auth_error.status_code