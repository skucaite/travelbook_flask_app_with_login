import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
# from travelbook.config import Config       # And when you can move all app.config variables + import os


database_name = "travelbook_login"
database_path = 'postgresql://postgres@localhost:5432/travelbook_login'

SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
CORS(app)

login_manager = LoginManager(app)
# login_manager.login_view = 'login'   - If we don't use Blueprints
login_manager.login_view = 'guides.login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)


from travelbook.guides.routes import guides
from travelbook.travels.routes import travels
from travelbook.main.routes import main
from travelbook.errors.handlers import errors

app.register_blueprint(guides)
app.register_blueprint(travels)
app.register_blueprint(main)
app.register_blueprint(errors)
