import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from pathlib import Path

from app.database import db
from app.routes.index import overview

basedir = Path(__file__).resolve().parent
load_dotenv(find_dotenv())

DATABASE = os.getenv('DATABASE')
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    f'sqlite:///{Path(basedir).joinpath(DATABASE)}'
)
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

def create_app():
    """
    Register all of our separated route files as Flask 
    Blueprints with their own group names to
    maintain a readable and coherent
    structure.

    Returns:
        Flask: Main app Flask object
    """
    app = Flask(__name__)
    app.config.from_object(__name__)

    app.register_blueprint(overview)

    db.init_app(app)

    return app

if '__main__' == __name__:
    app = create_app()

    app.run(port=5000)
