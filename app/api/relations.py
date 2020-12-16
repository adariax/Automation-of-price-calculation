from flask import request, jsonify, make_response, Blueprint

from app import get_db_session
from app.models import Operation, Part, Product, Additional

blueprint_relations = Blueprint('relations', __name__, template_folder='')


@blueprint_relations.route('/api/operationpart', methods=['DELETE', 'POST'])
def operation_part():
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

    return make_response(jsonify({'result': {'status': 'OK'}}), 200)


@blueprint_relations.route('/api/operationproduct', methods=['DELETE', 'POST'])
def operation_product():
    args = request.args
    try:
        operation_id = int(args.get('operation_id'))
        product_id = int(args.get('product_id'))
    except (ValueError, TypeError):
        return make_response(jsonify({'result': {'error': 'bad request'}}), 400)

    session = get_db_session()
    operation = session.query(Operation).filter(Operation.id == operation_id).first()
    product = session.query(Product).filter(Product.id == product_id).first()

    if not operation or not product:
        return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

    if request.method == 'POST':
        if operation in product.operations:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        product.operations.append(operation)
    elif request.method == 'DELETE':
        if operation not in product.operations:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        product.operations.remove(operation)
    session.commit()

    return make_response(jsonify({'result': {'status': 'OK'}}), 200)


@blueprint_relations.route('/api/partproduct', methods=['DELETE', 'POST'])
def part_product():
    args = request.args
    try:
        part_id = int(args.get('part_id'))
        product_id = int(args.get('product_id'))
    except (ValueError, TypeError):
        return make_response(jsonify({'result': {'error': 'bad request'}}), 400)

    session = get_db_session()
    part = session.query(Part).filter(Part.id == part_id).first()
    product = session.query(Product).filter(Product.id == product_id).first()

    if not part or not product:
        return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

    if request.method == 'POST':
        if part in product.parts:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        product.parts.append(part)
    elif request.method == 'DELETE':
        if part not in product.parts:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        product.parts.remove(part)
    session.commit()

    return make_response(jsonify({'result': {'status': 'OK'}}), 200)


@blueprint_relations.route('/api/additionalproduct', methods=['DELETE', 'POST'])
def additional_product():
    args = request.args
    try:
        additional_id = int(args.get('additional_id'))
        product_id = int(args.get('product_id'))
    except (ValueError, TypeError):
        return make_response(jsonify({'result': {'error': 'bad request'}}), 400)

    session = get_db_session()
    additional = session.query(Additional).filter(Additional.id == additional_id).first()
    product = session.query(Product).filter(Product.id == product_id).first()

    if not additional or not product:
        return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

    if request.method == 'POST':  # TODO: make possible adding any count of additionals/parts
        if additional in product.additionals:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        product.additionals.append(additional)
    elif request.method == 'DELETE':
        if additional not in product.additionals:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        product.additionals.remove(additional)
    session.commit()

    return make_response(jsonify({'result': {'status': 'OK'}}), 200)
