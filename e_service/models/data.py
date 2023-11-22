from werkzeug.security import generate_password_hash, check_password_hash
from e_service.app import app, db
from datetime import datetime
from flask_login import UserMixin
from flask_migrate import Migrate
from datetime import datetime





migrate = Migrate(app, db)

# Intermediate tables to represent many-to-many relationships
trader_product_association = db.Table(
    'trader_product_association',
    db.Column('trader_id', db.Integer, db.ForeignKey('traders.trader_id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.pro_id'))
)

product_category_association = db.Table(
    'product_category_association',
    db.Column('product_id', db.Integer, db.ForeignKey('product.pro_id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.cat_id'))
)

# Additional intermediate table for many-to-many relationship between Trader and Category
trader_category_association = db.Table(
    'trader_category_association',
    db.Column('trader_id', db.Integer, db.ForeignKey('traders.trader_id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.cat_id'))
)


class Trader(db.Model, UserMixin):
    __tablename__ = 'traders'

    trader_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    coords = db.relationship('TraderLocation', backref='user', lazy=True)
    services = db.relationship('Product', secondary=trader_product_association, backref='traders', lazy='dynamic')
    reset_token = db.Column(db.String(100), nullable=True)


    def __init__(self, full_name, email, phone_number, business_name, password):
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.business_name = business_name
        self.set_password(password)

    def get_id(self):
        return (self.trader_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self, expires_sec=1800):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in=expires_sec)
        self.reset_token = s.dumps({'trader_id': self.trader_id}).decode('utf-8')
        db.session.commit()
        return self.reset_token

    @staticmethod
    def verify_reset_token(token):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
        try:
            trader_id = s.loads(token)['trader_id']
        except BadSignature:
            return None
        return Trader.query.get(trader_id)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    coords = db.relationship('UserLocation', backref='user', lazy=True)
    reset_token = db.Column(db.String(100), nullable=True)

    def __init__(self, full_name, email, phone_number, password):
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.set_password(password)

    def get_id(self):
        return (self.id_user)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def generate_reset_tokens(self, expires_sec=1800):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in=expires_sec)
        self.reset_token = s.dumps({'id_user': self.id_user}).decode('utf-8')
        db.session.commit()
        return self.reset_token

    @staticmethod
    def verify_reset_tokens(token):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
        try:
            id_user = s.loads(token)['id_user']
        except BadSignature:
            return None
        return User.query.get(id_user)

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, full_name, password, email):
        self.full_name = full_name
        self.set_password(password)
        self.email = email

    def get_id(self):
        return (self.admin_id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


class Category(UserMixin, db.Model):
    __tablename__ = 'category'

    cat_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)

    def __init__(self, category_name):
        self.category_name = category_name

    def get_id(self):
        return (self.cat_id)


class Product(db.Model):
    __tablename__ = 'product'

    pro_id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.String(100), nullable=False)
    pro_dec = db.Column(db.String(300), nullable=False)
    pro_cont = db.Column(db.String(10), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.cat_id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('product', lazy=True))
    filename = db.Column(db.String(255))
    # trader_id = db.Column(db.Integer, db.ForeignKey('traders.trader_id'), nullable=False)
    # trader = db.relationship('Trader', backref=db.backref('products', lazy=True))

    def __init__(self, pro_name, pro_dec, pro_cont, filename, category_id):
        self.pro_name = pro_name
        self.pro_dec = pro_dec
        self.pro_cont = pro_cont
        self.filename = filename
        self.category_id = category_id

    def get_id(self):
        return (self.pro_id)

class UserLocation(db.Model):
    __tablename__ = 'userlocation'

    cord_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    latitude = db.Column(db.Float(100), nullable=False)
    longitude = db.Column(db.Float(100), nullable=False)

    def __init__(self, latitude, longitude, user_id):
        self.latitude = latitude
        self.longitude= longitude
        self.user_id = user_id

    def get_id(self):
        return (self.cord_id)

class TraderLocation(db.Model):
    __tablename__ = 'Traderlocation'

    cord_id = db.Column(db.Integer, primary_key=True)
    trader_id = db.Column(db.Integer, db.ForeignKey('traders.trader_id'), nullable=False)
    latitude = db.Column(db.Float(100), nullable=False)
    longitude = db.Column(db.Float(100), nullable=False)

    def __init__(self, latitude, longitude, trader_id):
        self.latitude = latitude
        self.longitude= longitude
        self.trader_id = trader_id

    def get_id(self):
        return (self.cord_id)
