from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import RawMaterial

class MaterialsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ids', required=True)

    def get(self):
        args = MaterialsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except TypeError:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        session = get_db_session()
        materials = []
        for m_id in ids:
            material = session.query(RawMaterial).filter(RawMaterial.id == m_id).first()
            if material:
                materials.append(material)
        if not materials:
            return make_response(jsonify({'result': {'materials': 'not found'}}), 404)

        return make_response(jsonify(
            {'result': {'materials': [material.to_dict() for material in materials]}}), 200)

    def delete(self):
        args = MaterialsResource.parser.parse_args()
        try:
            ids = list(map(int, args['ids'].split(',')))
        except TypeError:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        session = get_db_session()
        for m_id in ids:
            material = session.query(RawMaterial).filter(RawMaterial.id == m_id).first()
            if material:
                session.delete(material)

        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
