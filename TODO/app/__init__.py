from flask import Flask
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret1'

    # MongoDB setup
    client = MongoClient('mongodb+srv://s25717:12345gg_@s25717cluster.0dnmwk0.mongodb.net/?retryWrites=true&w=majority&appName=s25717cluster')
    app.db = client['todo_db']

    with app.app_context():
        from . import routes

    return app