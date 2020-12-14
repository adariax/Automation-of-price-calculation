from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Operation

class OperationsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ids', required=True)

    def get(self):
        args = OperationsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            if args['ids'] != 'all':
                return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        if args['ids'] == 'all':
            return make_response(jsonify({'result': {'opetations': 
                                 [opetation.to_dict(only=('id', 'title', 
                                 'machine.id', 'machine.title')) 
                                 for opetation in session.query(Operation).all()]}}), 200)

        opetations = []
        for o_id in ids:
            opetation = session.query(Operation).filter(Operation.id == o_id).first()
            if opetation:
                opetations.append(opetation)
        if not opetations:
            return make_response(jsonify({'result': {'opetations': 'not found'}}), 404)

        return make_response(jsonify({'result': {'opetations': 
                                     [opetation.to_dict(only=('id', 'title', 
                                     'machine.id', 'machine.title')) 
                                     for opetation in opetations]}}), 200)

    def delete(self):
        args = OperationsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        for o_id in ids:
            opetation = session.query(Operation).filter(Operation.id == o_id).first()
            if opetation:
                session.delete(opetation)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
