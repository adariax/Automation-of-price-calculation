  
from flask import jsonify, make_response, abort
from flask_restful import Resource
from flask_login import current_user

from app import get_db_session, app
from app.models import RawMaterial

class MaterialResource(Resource):
    def get(self, m_id):
        session = get_db_session()
        material = session.query(RawMaterial).get(m_id)
        if not material:
            return make_response(jsonify({'result': {'material': 'not found'}}), 404)
        return make_response(jsonify({'result': {'material': material.to_dict()}}), 200)