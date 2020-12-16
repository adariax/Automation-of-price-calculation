from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Machine, Worker


class MachineResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', required=True)
    post_parser.add_argument('price', required=True, type=float)
    post_parser.add_argument('worker_id', required=True, type=int)

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('title', required=False)
    put_parser.add_argument('price', required=False, type=float)
    put_parser.add_argument('worker_id', required=False, type=int)

    def get(self, m_id):
        session = get_db_session()
        machine = session.query(Machine).filter(Machine.id == m_id).first()

        if not machine:
            return make_response(jsonify({'result': {'machine': 'not found'}}), 404)

        return make_response(jsonify({'result': {'machine': 
                             machine.to_dict(only=('id', 'title', 'price', 
                             'worker.id', 'worker.title'))}}), 200)

    def delete(self, m_id):
        session = get_db_session()
        machine = session.query(Machine).filter(Machine.id == m_id).first()

        if not machine:
            return make_response(jsonify({'result': {'machine': 'not found'}}), 404)

        session.delete(machine)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def post(self, m_id):
        if m_id != 0:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        args = MachineResource.post_parser.parse_args()

        session = get_db_session()
        machine = Machine()
        machine.title = args['title']
        machine.price = args['price']
        if session.query(Worker).filter(Worker.id == args['worker_id']).first():
            machine.worker_id = args['worker_id']
        else:
            return make_response(jsonify({'result': {'error': 'nonexist worker'}}), 400)

        session.add(machine)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def put(self, m_id):
        session = get_db_session()
        machine = session.query(Machine).filter(Machine.id == m_id).first()

        if not machine:
            return make_response(jsonify({'result': {'machine': 'not found'}}), 404)
        
        args = MachineResource.put_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                if key == 'worker_id':
                    if session.query(Worker).filter(Worker.id == args['worker_id']).first():
                        machine.worker_id = args['worker_id']
                    else:
                        return make_response(jsonify({'result': {'error': 'nonexist worker'}}), 400)
                else:
                    machine.__setattr__(key, value)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)


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
                                 [machine.to_dict(only=('id', 'title', 'price', 
                                 'worker.id', 'worker.title')) 
                                 for machine in session.query(Machine).all()]}}), 200)

        machines = []
        for m_id in ids:
            machine = session.query(Machine).filter(Machine.id == m_id).first()
            if machine:
                machines.append(machine)
        if not machines:
            return make_response(jsonify({'result': {'machines': 'not found'}}), 404)

        return make_response(jsonify({'result': 
                                     {'machines': [machine.to_dict(only=('id', 'title', 'price', 
                                     'worker.id', 'worker.title')) for machine in machines]}}), 200)

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
