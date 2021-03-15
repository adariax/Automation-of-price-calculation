from app import db
from sqlalchemy_serializer import SerializerMixin

part_product = db.Table('part_product',
                        db.Column('part_id', db.Integer, db.ForeignKey('part.id')),
                        db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
                        )


class OperationPart(db.Model, SerializerMixin):
    operation_id = db.Column(db.Integer, db.ForeignKey('operation.id'), primary_key=True)
    operation = db.relationship('Operation', backref=db.backref('parts', 
                                             cascade='save-update, merge, delete, delete-orphan'))

    part_id = db.Column(db.Integer, db.ForeignKey('part.id'), primary_key=True)
    part = db.relationship('Part', backref=db.backref('operations', 
                                   cascade='save-update, merge, delete, delete-orphan'))

    time = db.Column(db.Float, nullable=False)


class OperationProduct(db.Model, SerializerMixin):
    operation_id = db.Column(db.Integer, db.ForeignKey('operation.id'), primary_key=True)
    operation = db.relationship('Operation', backref=db.backref('products', 
                                             cascade='save-update, merge, delete, delete-orphan'))
    
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product = db.relationship('Product', backref=db.backref('operations', 
                                         cascade='save-update, merge, delete, delete-orphan'))

    time = db.Column(db.Float, nullable=False)


class AdditionalProduct(db.Model, SerializerMixin):
    additional_id = db.Column(db.Integer, db.ForeignKey('additional.id'), primary_key=True)
    additional = db.relationship('Additional', backref=db.backref('products', 
                                               cascade='save-update, merge, delete, delete-orphan'))

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product = db.relationship('Product', backref=db.backref('additionals', 
                                         cascade='save-update, merge, delete, delete-orphan'))

    count = db.Column(db.Integer, nullable=False)


class RawMaterial(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    waste_coef = db.Column(db.Float, nullable=False)


class Worker(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Machine(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)
    worker = db.relationship('Worker', backref=db.backref('machines', lazy=True))


class Operation(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    
    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'), nullable=False)
    machine = db.relationship('Machine', backref=db.backref('operations', lazy=True))


class Additional(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Constant(db.Model, SerializerMixin):
    title = db.Column(db.String, nullable=False, primary_key=True, unique=True)
    value = db.Column(db.Float, nullable=False)


class Part(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    material_id = db.Column(db.Integer, db.ForeignKey('raw_material.id'), nullable=False)
    material = db.relationship('RawMaterial', backref=db.backref('parts', lazy=True))

    material_count = db.Column(db.Float, nullable=False)


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    r_coef = db.Column(db.Float, nullable=False)
    r_cost = db.Column(db.Float, nullable=False)
    w_cost = db.Column(db.Float, nullable=False)
    
    parts = db.relationship('Part', 
                            secondary=part_product, 
                            backref=db.backref('products'))
