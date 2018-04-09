from flask import request, jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()


def create_app(config_name):
    from app.models import Note

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/')
    def index():
        response = jsonify({
            'status': 'yo'
        })
        response.status_code = 200
        return response

    @app.route('/note', methods=['POST', 'GET'])
    def note():
        if request.method == "POST":
            user_id = str(request.data.get('userId'), '')
            book_id = str(request.data.get('bookId', ''))
            content = str(request.data.get('content', ''))
            is_fav = str(request.data.get('isFav', ''))
            is_fav = is_fav == 'True' or is_fav == 'true'
            if user_id and book_id and content:
                note = Note(user_id, book_id, content, is_fav)
                note.save()

                response = jsonify({
                    'id': note.id,
                    'userId': note.user_id,
                    'bookId': note.book_id,
                    'content': note.content,
                    'isFav': note.is_fav,
                    'dateCreated': note.date_created,
                    'dateModified': note.date_modified
                })

                response.status_code = 201
                return response
            else:
                response = jsonify({'errorMessage': 'one or more required params were missing'})
                response.status_code = 422
                return response

    return app
