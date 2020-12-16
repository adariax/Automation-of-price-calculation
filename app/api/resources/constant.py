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


class ConstantsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ids', required=True)

    def get(self):
        args = ConstantsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            if args['ids'] != 'all':
                return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        if args['ids'] == 'all':
            return make_response(jsonify(
                {'result': {'constants': [constant.to_dict() 
                for constant in session.query(Constant).all()]}}
                ), 200)

        session = get_db_session()
        constants = []
        for c_id in ids:
            constant = session.query(Constant).filter(Constant.id == c_id).first()
            if constant:
                constants.append(constant)
        if not constants:
            return make_response(jsonify({'result': {'constants': 'not found'}}), 404)

        return make_response(jsonify(
            {'result': {'constants': [constant.to_dict() for constant in constants]}}), 200)

    def delete(self):
        args = ConstantsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        for c_id in ids:
            constant = session.query(Constant).filter(Constant.id == c_id).first()
            if constant:
                session.delete(constant)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
