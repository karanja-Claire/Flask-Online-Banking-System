# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail 

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # configure email sending
    app.config['MAIL_SERVER']='smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '91f2cc361ed358'
    app.config['MAIL_PASSWORD'] = 'cf2471f49f7461'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    


    mail.init_app(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User


    
    #-------------------------------------------------------------------------------
    @app.before_first_request
    def create_table():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .management_system import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    # blueprint for customer routes and controllers
    # blueprint for non-auth parts of app
    from .customer_system import customer as customer_blueprint
    app.register_blueprint(customer_blueprint)
    # from customer import customer as customer_blueprint


    return app