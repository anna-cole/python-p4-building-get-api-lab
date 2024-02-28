#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = [] # will be a list of dictionaries
    bakeries = Bakery.query.all()
    
    for bakery in bakeries:
        goods_list = [] # will be a list of dictionaries of goods from each bakery
        goods = bakery.baked_goods # list of objects
        
        for good in goods:
            good_dict = {
                'id': good.id,
                'name': good.name,
                'price': good.price,
                'created_at': good.created_at,
                'updated_at': good.updated_at,
                'bakery_id': good.bakery_id
            }
            goods_list.append(good_dict)

        bakery_dict = {
        'id': bakery.id,
        'name': bakery.name,
        'created_at': bakery.created_at,
        'updated_at': bakery.updated_at,
        'baked_goods': goods_list
        }
        bakeries_list.append(bakery_dict)
        
    return make_response(bakeries_list, 200)

    # bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    # return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    if bakery:
        goods_list = [] # will be a list of dictionaries
        goods = bakery.baked_goods # list of objects
        
        for good in goods:
            good_dict = {
                'id': good.id,
                'name': good.name,
                'price': good.price,
                'created_at': good.created_at,
                'updated_at': good.updated_at,
                'bakery_id': good.bakery_id
            }
            goods_list.append(good_dict)
    
        body = {'id': bakery.id,
                'name': bakery.name,
                'created_at': bakery.created_at,
                'updated_at': bakery.updated_at,
                'baked_goods': goods_list}
        status = 200
    else:
        body = {'message': f'Bakery {id} not found.'}
        status = 404

    return make_response(body, status)

    # bakery = Bakery.query.filter_by(id=id).first()
    # bakery_serialized = bakery.to_dict()
    # return make_response (bakery_serialized, 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    body = []  # array to store a dictionary for each baked good

    for good in BakedGood.query.order_by(desc('price')).all(): # list of objects
        if good.bakery is not None:
            bakery_dict = good.bakery.to_dict(only=('id', 'name', 'created_at', 'updated_at',)) # to_dict is on a relationship, not on the obj, that's why the serialiation rules are not applying. Use serialization rules in the to_dict method. 
        else: 
            bakery_dict = {}
        
        good_dict = {
            'bakery': bakery_dict,
            'id': good.id,
            'name': good.name,
            'price': good.price,
            'created_at': good.created_at,
            'updated_at': good.updated_at,
            'bakery_id': good.bakery_id
        }
        body.append(good_dict)
       
    return make_response(body, 200)

    # baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all() # better way, no need to import desc
    # baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    # return make_response(baked_goods_by_price_serialized, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good_obj = BakedGood.query.order_by(desc('price')).first()
    # breakpoint()
    body = good_obj.to_dict() # here the to_dict method is straight on the obj, so the serialization rules in the model apply.       
    return make_response(body, 200)

    # most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    # most_expensive_serialized = most_expensive.to_dict()
    # return make_response(most_expensive_serialized, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
