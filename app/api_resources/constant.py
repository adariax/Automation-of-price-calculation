from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Constant

class ConstantResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', required=True)
    post_parser.add_argument('value', required=True, type=float)

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('title')
    put_parser.add_argument('value', type=float)

    def get(self, c_id):
        session = get_db_session()
        constant = session.query(Constant).filter(Constant.id == c_id).first()

        if not constant:
            return make_response(jsonify({'result': {'constant': 'not found'}}), 404)

        return make_response(jsonify({'result': {'constant': constant.to_dict()}}), 200)

    def delete(self, c_id):
        session = get_db_session()
        constant = session.query(Constant).filter(Constant.id == c_id).first()

        if not constant:
            return make_response(jsonify({'result': {'constant': 'not found'}}), 404)

        session.delete(constant)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def post(self, c_id):
        if c_id != 0:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        args = ConstantResource.post_parser.parse_args()

        session = get_db_session()
        constant = Constant()
        constant.title = args['title']
        constant.value = args['value']

        session.add(constant)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def put(self, c_id):
        session = get_db_session()
        constant = session.query(Constant).filter(Constant.id == c_id).first()

        if not constant:
            return make_response(jsonify({'result': {'constant': 'not found'}}), 404)
        
        args = ConstantResource.put_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                constant.__setattr__(key, value)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
