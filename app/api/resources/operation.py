from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Operation, Machine


class OperationResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', required=True)
    post_parser.add_argument('machine_id', required=True, type=int)

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('title', required=False)
    put_parser.add_argument('machine_id', required=False, type=int)

    def get(self, o_id):
        session = get_db_session()
        operation = session.query(Operation).filter(Operation.id == o_id).first()

        if not operation:
            return make_response(jsonify({'result': {'operation': 'not found'}}), 404)

        return make_response(jsonify({'result': {'operation': 
                             operation.to_dict(only=('id', 'title', 
                             'machine.id', 'machine.title'))}}), 200)

    def delete(self, o_id):
        session = get_db_session()
        operation = session.query(Operation).filter(Operation.id == o_id).first()

        if not operation:
            return make_response(jsonify({'result': {'operation': 'not found'}}), 404)

        session.delete(operation)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def post(self, o_id):
        if o_id != 0:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        args = OperationResource.post_parser.parse_args()

        session = get_db_session()
        operation = Operation()
        operation.title = args['title']
        if session.query(Machine).filter(Machine.id == args['machine_id']).first():
            operation.machine_id = args['machine_id']
        else:
            return make_response(jsonify({'result': {'error': 'nonexist machine'}}), 400)

        session.add(operation)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def put(self, o_id):
        session = get_db_session()
        operation = session.query(Operation).filter(Operation.id == o_id).first()

        if not operation:
            return make_response(jsonify({'result': {'operation': 'not found'}}), 404)
        
        args = OperationResource.put_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                if key == 'machine_id':
                    if session.query(Machine).filter(Machine.id == args['machine_id']).first():
                        operation.machine_id = args['machine_id']
                    else:
                        return make_response(jsonify({'result': {'error': 'nonexist machine'}}), 400)
                else:
                    operation.__setattr__(key, value)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)


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
            return make_response(jsonify({'result': {'operations': 
                                 [operation.to_dict(only=('id', 'title', 
                                 'machine.id', 'machine.title')) 
                                 for operation in session.query(Operation).all()]}}), 200)

        operations = []
        for o_id in ids:
            operation = session.query(Operation).filter(Operation.id == o_id).first()
            if operation:
                operations.append(operation)
        if not operations:
            return make_response(jsonify({'result': {'operations': 'not found'}}), 404)

        return make_response(jsonify({'result': {'operations': 
                                     [operation.to_dict(only=('id', 'title', 
                                     'machine.id', 'machine.title')) 
                                     for operation in operations]}}), 200)

    def delete(self):
        args = OperationsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        for o_id in ids:
            operation = session.query(Operation).filter(Operation.id == o_id).first()
            if operation:
                session.delete(operation)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
