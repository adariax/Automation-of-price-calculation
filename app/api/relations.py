from flask import request, jsonify, make_response, Blueprint

from app import get_db_session
from app.models import Operation, Part

blueprint_relations = Blueprint('relations', __name__, template_folder='')


@blueprint_relations.route('/api/operation-part', methods=['DELETE', 'POST'])
def create_post(post_id=None):
    args = request.args
    try:
        operation_id = int(args.get('operation_id'))
        part_id = int(args.get('part_id'))
    except (ValueError, TypeError):
        return make_response(jsonify({'result': {'error': 'bad request'}}), 400)

    session = get_db_session()
    operation = session.query(Operation).filter(Operation.id == operation_id).first()
    part = session.query(Part).filter(Part.id == part_id).first()

    if not operation or not part:
        return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

    if request.method == 'POST':
        if operation in part.operations:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        part.operations.append(operation)
    elif request.method == 'DELETE':
        if operation not in part.operations:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        part.operations.remove(operation)
    session.commit()

    return make_response(jsonify({'result': {'status': 'OK'}}), 400)
