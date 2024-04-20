from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Define relationship
    vendors = relationship('VendorSweet', back_populates='sweet')

    # Serialization
    def to_dict(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Define relationship
    sweets = relationship('VendorSweet', back_populates='vendor')

    # Serialization
    def to_dict(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Define foreign keys
    sweet_id = db.Column(db.Integer, ForeignKey('sweets.id'))
    vendor_id = db.Column(db.Integer, ForeignKey('vendors.id'))

    # Define relationship
    sweet = relationship('Sweet', back_populates='vendors')
    vendor = relationship('Vendor', back_populates='sweets')

    # Serialization
    def to_dict(self):
        return {'id': self.id, 'price': self.price, 'sweet_id': self.sweet_id, 'vendor_id': self.vendor_id}

    # Validation (for example, price must be positive)
    #@validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be positive")
        return price


    def __repr__(self):
        return f'<VendorSweet {self.id}>'
