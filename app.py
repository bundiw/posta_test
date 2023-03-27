from flask import Flask, abort, jsonify, redirect, request, url_for
from flask_cors import CORS

from model import Delivery, setup_db


app = Flask(__name__)
setup_db(app)

"""
@DONE: Set up CORS. Allow '*' for origins
"""
CORS(app)
"""
@DONE: Use the after_request decorator to set Access-Control-Allow
"""
@app.after_request
def after_request(response):
    
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response

"""
Delivery APIs
"""
"""
show all the deliveries and theri status
"""
@app.route('/deliveries')
def all_deliveries():
    
    deliveries_list = Delivery.query.all()
    deliveries = [delivery.format() for delivery in 
                  deliveries_list]
    deliveries_count = len(deliveries_list)

    return {
        "success":True,
        "message":"Deliveries fetched success",
        "data":deliveries,
        "match_count": deliveries_count
    }

"""
insert a new delivery
"""
@app.route('/deliveries/create',methods=['POST'])
def post_delivery():
    shipment = request.get_json()
    
    delivery_data = Delivery(**shipment)
    try:
        delivery_data.insert()
        
    except ValueError as e:
        print(e.sys.exec())
        abort(422)


    return {
        "success":True,
        "message":"Delivery  id {} added success".format(delivery_data.id),
        "data":shipment        
    }

@app.route('/deliveries/<int:ship_id>/update',methods=['PATCH'])
def update_ship_status(ship_id):
    delivery = Delivery.query.get(ship_id)

    # None existent field update
    if delivery is None:
        abort(404)

    delivery_data = delivery.format()

    try:
        delivery.received_status = True
        delivery.update()

    except:
        abort(422)
   
    return {
        "success":True,
        "message":"Deliveries with id {} updated success".format(ship_id),
        "data":delivery_data
    }

@app.route('/deliveries/<int:ship_id>/delete',methods=['DELETE'])
def delete_shipment(ship_id):
    delivery= Delivery.query.get(ship_id)
    # None existent field delete
    if delivery is None:
        abort(404)


    delivery_data = delivery.format() 
    try:
        delivery.delete()


    except:
        abort(422)
 
    return {
        "success":True,
        "message":"Deliveries with id {} deleted sucess".format(ship_id),
        "data":delivery_data    
        }


# def auth():
#     token_data = request.headers.get('Authorization')
#     token = token_data.split(" ")[1]
#     print(token)
#     return {
#         "token":token
#     }


@app.errorhandler(404)
def success_404(error):

    return jsonify({
        'success': False,
        'message': error.name,
        'data':None


    }), 404

@app.errorhandler(400)
def success_400(error):

    return jsonify({
        'success': False,
        'message': error.name,
        'data':None


    }), 400


@app.errorhandler(422)
def success_422(error):

    return jsonify({
        'success': False,
        'message': error.name,
        'data':None


    }), 422

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


