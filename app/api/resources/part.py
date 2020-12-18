from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import Part, RawMaterial, Operation


def dict(part):
    operation_time = []
    session = get_db_session()
    for obj in part.operations:
        operation = session.query(Operation).filter(Operation.id == obj.operation_id).first()
        time = obj.time
        operation_time.append((operation, time))
    return {'id': part.id, 'title': part.title,
            'material': {'id': part.material.id, 'title': part.material.title, 
                         'count': part.material_count},
            'operations': [{'id': info[0].id, 
                            'title': info[0].title,
                            'time': info[1]} for info in operation_time]}


class PartResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', required=True)
    post_parser.add_argument('material_id', required=True, type=int)
    post_parser.add_argument('material_count', required=True, type=int)

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('title', required=False)
    put_parser.add_argument('material_id', required=False, type=int)
    put_parser.add_argument('material_count', required=True, type=int)

    def get(self, p_id):
        session = get_db_session()
        part = session.query(Part).filter(Part.id == p_id).first()

        if not part:
            return make_response(jsonify({'result': {'part': 'not found'}}), 404)

        return make_response(jsonify({'result': {'part': dict(part)}}), 200)

    def delete(self, p_id):
        session = get_db_session()
        part = session.query(Part).filter(Part.id == p_id).first()

        if not part:
            return make_response(jsonify({'result': {'part': 'not found'}}), 404)

        session.delete(part)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)

    def post(self, p_id):
        if p_id != 0:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        args = PartResource.post_parser.parse_args()

        session = get_db_session()
        part = Part()
        part.title = args['title']
        part.material_id = args['materual_count']
        if session.query(RawMaterial).filter(RawMaterial.id == args['material_id']).first():
            part.material_id = args['material_id']
        else:
            return make_response(jsonify({'result': {'error': 'nonexist material'}}), 400)

        session.add(part)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)

    def put(self, p_id):
        session = get_db_session()
        part = session.query(Part).filter(Part.id == p_id).first()

        if not part:
            return make_response(jsonify({'result': {'part': 'not found'}}), 404)

        args = PartResource.put_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                if key == 'material_id':
                    if session.query(RawMaterial).filter(RawMaterial.id ==
                                                         args['material_id']).first():
                        part.material_id = args['material_id']
                    else:
                        return make_response(jsonify({'result':
                                             {'error': 'nonexist material'}}), 400)
                else:
                    part.__setattr__(key, value)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)


class PartsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ids', required=True)

    def get(self):
        args = PartsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            if args['ids'] != 'all':
                return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        if args['ids'] == 'all':
            return make_response(jsonify({'result': {'parts': [dict(part) 
                                 for part in session.query(Part).all()]}}), 200)

        parts = []
        for p_id in ids:
            part = session.query(Part).filter(Part.id == p_id).first()
            if part:
                parts.append(part)
        if not parts:
            return make_response(jsonify({'result': {'parts': 'not found'}}), 404)

        return make_response(jsonify({'result': {'parts': [dict(part) for part in parts]}}), 200)

    def delete(self):
        args = PartsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except ValueError:
            return make_response(jsonify({'result': {'error': 'wrong ids'}}), 400)

        session = get_db_session()
        for p_id in ids:
            part = session.query(Part).filter(Part.id == p_id).first()
            if part:
                session.delete(part)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
