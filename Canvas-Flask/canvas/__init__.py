from functools import wraps
from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder='../templates', static_folder="../static")
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# dashboard.bind(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# login_manager.login_message = "You are not authorized to access this page!"


@app.before_first_request
def create_tables():
    from canvas.models import ClassList
    db.create_all()


# def login_required(role=None):
#     if role is None:
#         role = ["ANY"]
#
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated_view(*args, **kwargs):
#             if not current_user.is_authenticated:
#                 return login_manager.unauthorized()
#             if (current_user.role not in role) and ("ANY" not in role):
#                 return login_manager.unauthorized()
#
#             return fn(*args, **kwargs)
#
#         return decorated_view
#
#     return wrapper


import canvas.routes
