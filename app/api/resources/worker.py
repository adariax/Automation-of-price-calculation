from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Worker


class WorkerResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', required=True)
    post_parser.add_argument('price', required=True, type=float)

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('title', required=False)
    put_parser.add_argument('price', required=False, type=float)

    def get(self, w_id):
        session = get_db_session()
        worker = session.query(Worker).filter(Worker.id == w_id).first()

        if not worker:
            return make_response(jsonify({'result': {'worker': 'not found'}}), 404)

        return make_response(jsonify({'result': {'worker':
                             worker.to_dict(only=('id', 'title', 'price',
                             'machines.id', 'machines.title'))}}), 200)

    def delete(self, w_id):
        session = get_db_session()
        worker = session.query(Worker).filter(Worker.id == w_id).first()

        if not worker:
            return make_response(jsonify({'result': {'worker': 'not found'}}), 404)

        session.delete(worker)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)

    def post(self, w_id):
        if w_id != 0:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        args = WorkerResource.post_parser.parse_args()

        session = get_db_session()
        worker = Worker()
        worker.title = args['title']
        worker.price = args['price']

        session.add(worker)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)

    def put(self, w_id):
        session = get_db_session()
        worker = session.query(Worker).filter(Worker.id == w_id).first()

        if not worker:
            return make_response(jsonify({'result': {'worker': 'not found'}}), 404)

        args = WorkerResource.put_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                worker.__setattr__(key, value)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)


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
