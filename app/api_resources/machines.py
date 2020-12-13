from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Machine

class MachinesResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ids', required=True)

    def get(self):
        args = MachinesResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            if args['ids'] != 'all':
                return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        if args['ids'] == 'all':
            return make_response(jsonify({'result': {'machines': 
                                 [machine.to_dict(only=('id', 'title', 'price')) 
                                 for machine in session.query(Machine).all()]}}), 200)

        machines = []
        for m_id in ids:
            machine = session.query(Machine).filter(Machine.id == m_id).first()
            if machine:
                machines.append(machine)
        if not machines:
            return make_response(jsonify({'result': {'machines': 'not found'}}), 404)

        return make_response(jsonify({'result': 
                                     {'machines': [machine.to_dict(only=('id', 'title', 'price')) 
                                     for machine in machines]}}), 200)

    def delete(self):
        args = MachinesResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        for m_id in ids:
            machine = session.query(Machine).filter(Machine.id == m_id).first()
            if machine:
                session.delete(machine)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
