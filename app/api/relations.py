from flask import request, jsonify, make_response, Blueprint

from app import get_db_session
from app.models import Operation, Part, Product, Additional
from app.models import AdditionalProduct, OperationPart, OperationProduct

blueprint_relations = Blueprint('relations', __name__, template_folder='')


@blueprint_relations.route('/api/operationpart', methods=['DELETE', 'POST'])
def operation_part():
    args = request.args
    try:
        operation_id = int(args.get('operation_id'))
        part_id = int(args.get('part_id'))
        time = float(args.get('time')) if request.method == 'POST' else 0
    except (ValueError, TypeError):
        return make_response(jsonify({'result': {'error': 'bad request'}}), 400)

    session = get_db_session()
    operation = session.query(Operation).filter(Operation.id == operation_id).first()
    part = session.query(Part).filter(Part.id == part_id).first()

    if not operation or not part:
        return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

    op = session.query(OperationPart).filter(OperationPart.part_id == part_id,
                                             OperationPart.operation_id == operation_id).first()

    if request.method == 'POST':
        if op:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        op = OperationPart(operation_id=operation.id, part_id=part.id, time=time)
        session.add(op)
    elif request.method == 'DELETE':
        if op:
            session.delete(op)
    session.commit()

    return make_response(jsonify({'result': {'status': 'OK'}}), 200)


@blueprint_relations.route('/api/operationproduct', methods=['DELETE', 'POST'])
def operation_product():
    args = request.args
    try:
        operation_id = int(args.get('operation_id'))
        product_id = int(args.get('product_id'))
        time = float(args.get('time')) if request.method == 'POST' else 0
    except (ValueError, TypeError):
        return make_response(jsonify({'result': {'error': 'bad request'}}), 400)

    session = get_db_session()
    operation = session.query(Operation).filter(Operation.id == operation_id).first()
    product = session.query(Product).filter(Product.id == product_id).first()

    if not operation or not product:
        return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

    op = session.query(OperationProduct).filter(OperationProduct.product_id == product_id,
                                                OperationProduct.operation_id == operation_id
                                                ).first()
    print(operation_id, args)
    if request.method == 'POST': 
        if op:
            print(op)
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        op = OperationProduct(operation_id=operation.id, product_id=product.id, time=time)
        session.add(op)
    elif request.method == 'DELETE':
        if not op:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

        session.delete(op)
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
        count = int(args.get('count')) if request.method == 'POST' else 0
    except (ValueError, TypeError):
        return make_response(jsonify({'result': {'error': 'bad request'}}), 400)

    session = get_db_session()
    additional = session.query(Additional).filter(Additional.id == additional_id).first()
    product = session.query(Product).filter(Product.id == product_id).first()

    if not additional or not product:
        return make_response(jsonify({'result': {'error': 'bad id'}}), 400)

    ap = session.query(AdditionalProduct).filter(AdditionalProduct.product_id == product_id,
                                                 AdditionalProduct.additional_id == additional_id
                                                 ).first()
    if request.method == 'POST':
        if ap:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)
        ap = AdditionalProduct(additional_id=additional.id, product_id=product.id, count=count)
        session.add(ap)
    elif request.method == 'DELETE':
        if not ap:
            return make_response(jsonify({'result': {'error': 'bad id'}}), 400)
        session.delete(ap)
    session.commit()

    return make_response(jsonify({'result': {'status': 'OK'}}), 200)
