from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Constant

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
        except TypeError:
            return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        for c_id in ids:
            constant = session.query(Constant).filter(Constant.id == c_id).first()
            if constant:
                session.delete(constant)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
