import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import UserMixin

database_name = "travelbook_login"
database_path = 'postgresql://postgres@localhost:5432/travelbook_login'

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


SECRET_KEY = os.urandom(32)

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    db.app = app
    db.init_app(app)
    bcrypt.app = Bcrypt(app)
    login_manager.app = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


@login_manager.user_loader
def load_user(guide_id):
    return Guide.query.get(int(guide_id))

# Models
class Guide(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    travels = db.relationship('Travel', backref='guide', lazy=True)

    def __repr__(self):
        return f'<Guide: {self.name} {self.surname}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.Text, nullable=False)
    guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'), nullable=False)

    def __repr__(self):
        return f'<Travel: {self.title}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
