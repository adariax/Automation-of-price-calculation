from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Worker

class WorkersResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ids', required=True)

    def get(self):
        args = WorkersResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            if args['ids'] != 'all':
                return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        if args['ids'] == 'all':
            return make_response(jsonify({'result': {'workers': 
                [worker.to_dict(only=('id', 'title', 'price', 'machines.id', 'machines.title')) 
                for worker in session.query(Worker).all()]}}
                ), 200)

        workers = []
        for w_id in ids:
            worker = session.query(Worker).filter(Worker.id == w_id).first()
            if worker:
                workers.append(worker)
        if not workers:
            return make_response(jsonify({'result': {'workers': 'not found'}}), 404)

        return make_response(jsonify({'result': {'workers': 
            [worker.to_dict(only=('id', 'title', 'price', 'machines.id', 'machines.title')) 
            for worker in workers]}}), 200)

    def delete(self):
        args = WorkersResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        for w_id in ids:
            worker = session.query(Worker).filter(Worker.id == w_id).first()
            if worker:
                session.delete(worker)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
