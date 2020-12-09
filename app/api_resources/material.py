  
from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import get_db_session
from app.models import RawMaterial

class MaterialResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', required=True)
    post_parser.add_argument('price', required=True, type=float)
    post_parser.add_argument('waste_coef', required=True, type=float)

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('title')
    put_parser.add_argument('price', type=float)
    put_parser.add_argument('waste_coef', type=float)

    def get(self, m_id):
        session = get_db_session()
        material = session.query(RawMaterial).filter(RawMaterial.id == m_id).first()

        if not material:
            return make_response(jsonify({'result': {'material': 'not found'}}), 404)

        return make_response(jsonify({'result': {'material': material.to_dict()}}), 200)

    def delete(self, m_id):
        session = get_db_session()
        material = session.query(RawMaterial).filter(RawMaterial.id == m_id).first()

        if not material:
            return make_response(jsonify({'result': {'material': 'not found'}}), 404)

        session.delete(material)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def post(self, m_id):
        if m_id != 0:
            return make_response(jsonify({'result': {'error': 'wrong id'}}), 400)

        args = MaterialResource.post_parser.parse_args()

        session = get_db_session()
        material = RawMaterial()
        material.title = args['title']
        material.price = args['price']
        material.waste_coef = args['waste_coef']

        session.add(material)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)
    
    def put(self, m_id):
        session = get_db_session()
        material = session.query(RawMaterial).filter(RawMaterial.id == m_id).first()

        if not material:
            return make_response(jsonify({'result': {'material': 'not found'}}), 404)
        
        args = MaterialResource.post_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                material.__setattr__(key, value)
        session.commit()
        return make_response(jsonify({'result': {'success': 'OK'}}), 200)