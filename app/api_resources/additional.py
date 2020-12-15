from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Additional

class AdditionalResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', required=True)
    post_parser.add_argument('price', required=True, type=float)

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('title')
    put_parser.add_argument('price', type=float)

    def get(self, a_id):
        session = get_db_session()
        additional = session.query(Additional).filter(Additional.id == a_id).first()

        if not additional:
            return make_response(jsonify({'result': {'additional': 'not found'}}), 404)

        return make_response(jsonify({'result': {'additional': additional.to_dict()}}), 200)

    def delete(self, a_id):
        session = get_db_session()
        additional = session.query(Additional).filter(Additional.id == a_id).first()

        if not additional:
            return make_response(jsonify({'result': {'additional': 'not found'}}), 404)

        session.delete(additional)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def post(self, a_id):
        if a_id != 0:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        args = AdditionalResource.post_parser.parse_args()

        session = get_db_session()
        additional = Additional()
        additional.title = args['title']
        additional.price = args['price']

        session.add(additional)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def put(self, a_id):
        session = get_db_session()
        additional = session.query(Additional).filter(Additional.id == a_id).first()

        if not additional:
            return make_response(jsonify({'result': {'additional': 'not found'}}), 404)
        
        args = AdditionalResource.put_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                additional.__setattr__(key, value)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
