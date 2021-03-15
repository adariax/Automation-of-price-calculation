from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Product, Additional, Operation


def dict(product):
    operation_time, additional_count = [], []
    session = get_db_session()

    for obj in product.operations:
        operation = session.query(Operation).filter(Operation.id == obj.operation_id).first()
        time = obj.time
        operation_time.append((operation, time))

    for obj in product.additionals:
        additional = session.query(Additional).filter(Additional.id == obj.additional_id).first()
        count = obj.count
        additional_count.append((additional, count))

    return {'id': product.id, 'title': product.title, 'profitability': product.r_coef,
            'retale cost': '%.2f' % product.r_cost, 'wholesale cost': '%.2f' % product.w_cost,
            'parts': [{'id': part.id, 'title': part.title} for part in product.parts],
            'operations': [{'id': info[0].id, 
                            'title': info[0].title,
                            'time': info[1]} for info in operation_time],
            'additionals': [{'id': info[0].id, 
                            'title': info[0].title, 'count': info[1]} for info in additional_count]}


class ProductResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', required=True)
    post_parser.add_argument('r_coef', required=True, type=float)
    post_parser.add_argument('r_cost', required=True, type=float)
    post_parser.add_argument('w_cost', required=True, type=float)

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('title')
    put_parser.add_argument('r_coef', type=float)
    put_parser.add_argument('r_cost', type=float)
    put_parser.add_argument('w_cost', type=float)

    def get(self, p_id):
        session = get_db_session()
        product = session.query(Product).filter(Product.id == p_id).first()

        if not product:
            return make_response(jsonify({'result': {'product': 'not found'}}), 404)

        return make_response(jsonify({'result': {'product': dict(product)}}), 200)

    def delete(self, p_id):
        session = get_db_session()
        product = session.query(Product).filter(Product.id == p_id).first()

        if not product:
            return make_response(jsonify({'result': {'product': 'not found'}}), 404)

        session.delete(product)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def post(self, p_id):
        if p_id != 0:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        args = ProductResource.post_parser.parse_args()

        session = get_db_session()
        product = Product()
        product.title = args['title']
        product.r_coef = args['r_coef']
        product.r_cost = args['r_cost']
        product.w_cost = args['w_cost']

        session.add(product)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def put(self, p_id):
        session = get_db_session()
        product = session.query(Product).filter(Product.id == p_id).first()

        if not product:
            return make_response(jsonify({'result': {'product': 'not found'}}), 404)
        
        args = ProductResource.put_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                product.__setattr__(key, value)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)


class ProductsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ids', required=True)

    def get(self):
        args = ProductsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            if args['ids'] != 'all':
                return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        if args['ids'] == 'all':
            return make_response(jsonify({'result': {'products': [dict(product) 
                                         for product in session.query(Product).all()]}}), 200)

        session = get_db_session()
        products = []
        for p_id in ids:
            product = session.query(Product).filter(Product.id == p_id).first()
            if product:
                products.append(product)
        if not products:
            return make_response(jsonify({'result': {'products': 'not found'}}), 404)

        return make_response(jsonify(
            {'result': {'products': [dict(product) for product in products]}}), 200)

    def delete(self):
        args = ProductsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        for p_id in ids:
            product = session.query(Product).filter(Product.id == p_id).first()
            if product:
                session.delete(product)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
