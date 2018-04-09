from flask import request, jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from instance.config import app_config

db = SQLAlchemy()


def create_app(config_name):
    from app.models import Note

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        response = jsonify({
            'status': 'yo'
        })
        response.status_code = 200
        return response

    @app.route('/user/<int:user_id>/notes/<int:note_id>', methods=["GET", "PUT"])
    @app.route('/user/<int:user_id>/notes/', defaults={'note_id': None}, methods=['GET', 'POST'])
    def all_notes(user_id, note_id, **kwargs):
        if request.method == "GET":
            if note_id is None:
                notes = Note.query.filter_by(user_id=user_id)
                print(notes)
                if not notes:
                    response = jsonify({
                        'notes': []
                    })
                    response.status_code = 200
                    return response
                else:
                    results = []

                    for note in notes:
                        obj = {
                            'id': note.id,
                            'bookId': note.book_id,
                            'content': note.content,
                            'isFav': note.is_fav
                        }
                        results.append(obj)

                    response = jsonify({
                        'userId': user_id,
                        'notes': results
                    })
                    response.status_code = 200
                    return response
            else:
                note = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()
                response = jsonify({
                    'id': note.id,
                    'userId': note.user_id,
                    'bookId': note.book_id,
                    'content': note.content,
                    'isFav': note.is_fav,
                    'dateCreated': note.date_created,
                    'dateModified': note.date_modified
                })

                response.status_code = 200
                return response

        elif request.method == "POST":
            user_id = request.values.get("userId")
            book_id = request.data.get('bookId')
            content = request.data.get('content')
            is_fav = request.data.get('isFav')
            is_fav = is_fav == 'True' or is_fav == 'true'
            if user_id and book_id and content:
                new_note = Note(user_id, book_id, content, is_fav)
                new_note.save()

                response = jsonify({
                    'id': new_note.id,
                    'userId': new_note.user_id,
                    'bookId': new_note.book_id,
                    'content': new_note.content,
                    'isFav': new_note.is_fav,
                    'dateCreated': new_note.date_created,
                    'dateModified': new_note.date_modified
                })

                response.status_code = 201
                return response
            else:
                response = jsonify({'errorMessage': 'one or more required params were missing'})
                response.status_code = 422
                return response
        elif request.method == "PUT":
            if note_id is None:
                response = jsonify({'errorMessage': 'note id is missing'})
                response.status_code = 422
                return response
            else:
                content = request.data.get('content')
                is_fav = request.data.get('isFav')
                is_fav = is_fav == 'True' or is_fav == 'true'
                if user_id and content:
                    note = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()
                    note.content = content
                    note.is_fav = is_fav
                    updated = note.save()
                    response = jsonify({
                        'id': updated.id,
                        'userId': updated.user_id,
                        'bookId': updated.book_id,
                        'content': updated.content,
                        'isFav': updated.is_fav,
                        'dateCreated': updated.date_created,
                        'dateModified': updated.date_modified
                    })

                    response.status_code = 200
                    return response

    return app
