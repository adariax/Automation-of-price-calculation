from app import db, app
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)


class Part(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    material_id = db.Column(db.Integer, db.ForeignKey('raw_material.id'), nullable=False)


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    r_coef = db.Column(db.Float, nullable=False)
    r_cost = db.Column(db.Float, nullable=False)
    w_cost = db.Column(db.Float, nullable=False)


fav_posts = db.Table('operation_part',
                     db.Column('operation_id', db.Integer, db.ForeignKey('operation.id')),
                     db.Column('part_id', db.Integer, db.ForeignKey('part.id'))
                     )

fav_posts = db.Table('part_product',
                     db.Column('part_id', db.Integer, db.ForeignKey('part.id')),
                     db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
                     )

fav_posts = db.Table('operation_product',
                     db.Column('operation_id', db.Integer, db.ForeignKey('operation.id')),
                     db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
                     )

fav_posts = db.Table('additional_product',
                     db.Column('additional_id', db.Integer, db.ForeignKey('additional.id')),
                     db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
                     )
