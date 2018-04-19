from flask import request, jsonify
from flask_api import FlaskAPI
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import and_

from instance.config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    from app.models import Note
    from app.models import User

    app = FlaskAPI(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        response = jsonify({
            'status': 'yo'
        })
        response.status_code = 200
        return response

    @login_required
    @app.route('/logout')
    def logout():
        logout_user()
        response = jsonify({
            'message': 'logged out successfully'
        })
        response.status_code = 200
        return response

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            response = jsonify({
                'sessionToken': current_user.get_id()
            })
            return response
        else:
            email = request.values.get("email")
            pwd = request.values.get("password")

            user = User.query.filter(User.email == email).first()
            if user is None:
                response = jsonify({
                    'errorMessage': 'email does not exist'
                })
                response.status_code = 401
                return response
            elif user.validate_password(pwd):
                login_user(user)
                response = jsonify({
                    'sessionToken': user.session_token
                })
                response.status_code = 200
                return response
            else:
                response = jsonify({
                    "errorMessage": "incorrect password"}
                )
                response.status_code = 401
                return response

    @app.route('/register', methods=['POST'])
    def register():
        email = request.values.get('email')
        pwd = request.values.get('password')
        user = User.query.filter(User.email == email).first()
        if user is not None:
            response = jsonify({
                'errorMessage': 'email already exists'
            })
            response.status_code = 200
            return response
        else:
            user = User(email)
            user.set_password(pwd)
            user.save()
            login_user(user)
            response = jsonify({
                'sessionToken': user.session_token
            })
            response.status_code = 200
            return response

    @app.route('/book/<string:book_id>', methods=['GET'])
    @login_required
    def get_notes_for_book(book_id, **kwargs):
        user = User.query.filter(User.session_token == current_user.get_id()).first()
        user_id = user.id
        if request.method == "GET":
            notes = Note.query.filter(and_(Note.user_id == user_id, Note.book_id == book_id))
            if not notes:
                response = jsonify({
                    'bookId': book_id,
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
                    'bookId': book_id,
                    'notes': results
                })
                response.status_code = 200
                return response

    @app.route('/notes/<int:note_id>', methods=["GET", "PUT"])
    @app.route('/notes/', defaults={'note_id': None}, methods=['GET', 'POST'])
    @login_required
    def all_notes(note_id, **kwargs):
        user = User.query.filter(User.session_token == current_user.get_id()).first()
        user_id = user.id
        if request.method == "GET":
            if note_id is None:
                notes = Note.query.filter(Note.user_id == user_id)
                if not notes:
                    response = jsonify({
                        'userId': user_id,
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
                    'bookId': note.book_id,
                    'content': note.content,
                    'isFav': note.is_fav,
                    'dateCreated': note.date_created,
                    'dateModified': note.date_modified
                })

                response.status_code = 200
                return response
        elif request.method == "POST":
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
                else:
                    response = jsonify({
                        'errorMessage': 'content value is missing'
                    })
                    response.status_code = 422
                    return response

    return app
