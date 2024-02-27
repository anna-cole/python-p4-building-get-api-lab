#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

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
    bakeries_list = []
    bakeries = Bakery.query.all()
    for bakery in bakeries:

        goods_list = []
        goods = bakery.baked_goods
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

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    goods_list = []
    goods = bakery.baked_goods

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
    
    if bakery:
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

# Better way to debug this for inspecting variables? Breakpoint or flask shell?
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    body = []  # array to store a dictionary for each baked good
    for good in BakedGood.query.order_by(desc('price')):
        bakery_dict = good.bakery.to_dict()
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

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    return ''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
