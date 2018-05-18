from flask import request, jsonify, url_for, make_response
from flask_api import FlaskAPI
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import and_
from werkzeug.utils import secure_filename
import os

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
    app.config['UPLOAD_FOLDER'] = "./images/"
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
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

    @app.route('/book/<string:book_id>', methods=['GET', 'DELETE'])
    @login_required
    def book(book_id, **kwargs):
        user = User.query.filter(User.session_token == current_user.get_id()).first()
        user_id = user.id
        notes = Note.query.filter(and_(Note.user_id == user_id, Note.book_id == book_id)).all()

        if request.method == "GET":
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
                    results.append(note.get_response_object())

                response = jsonify({
                    'bookId': book_id,
                    'notes': results
                })
                response.status_code = 200
                return response
        elif request.method == "DELETE":
            if notes:
                for note in notes:
                    note.delete()
            response = jsonify({'success': 'all notes deleted'})
            response.status_code = 200
            return response

    @app.route('/notes/<int:note_id>', methods=["GET", "PUT", "DELETE"])
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
                        results.append(note.get_response_object())

                    response = jsonify({
                        'userId': user_id,
                        'notes': results
                    })
                    response.status_code = 200
                    return response
            else:
                note = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()
                response = jsonify(note.get_response_object())
                response.status_code = 200
                return response
        elif request.method == "POST":
            book_id = request.data.get('bookId')
            title = request.data.get('title')
            content = request.data.get('content')
            is_fav = request.data.get('isFav')
            is_fav = is_fav == 'True' or is_fav == 'true'
            tags = request.data.get('tags')

            if user_id and title and book_id and content:
                new_note = Note(user_id, book_id, title, content, is_fav, tags if tags is not None else "")
                new_note.save()

                response = jsonify(new_note.get_response_object())
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
                title = request.data.get('title')
                content = request.data.get('content')
                is_fav = request.data.get('isFav')
                is_fav = is_fav == 'True' or is_fav == 'true'
                tags = request.data.get('tags')
                if content is not None:
                    note = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()
                    note.title = title
                    note.content = content
                    note.is_fav = is_fav
                    note.tags = tags

                    updated = note.save()

                    response = jsonify(updated.get_response_object())
                    response.status_code = 200
                    return response
                else:
                    response = jsonify({
                        'errorMessage': 'content value is missing'
                    })
                    response.status_code = 422
                    return response
        elif request.method == "DELETE":
            if note_id is None:
                response = jsonify({'errorMessage': 'note id is missing'})
                response.status_code = 422
                return response

            note = Note.query.filter(Note.user_id == user_id, Note.id == note_id).first()
            note.delete()

            response = jsonify({
                'successMessage': 'successfully deleted note'
            })
            response.status_code = 200
            return response

    @app.route('/images/', methods=['GET', 'POST'])
    @login_required
    def upload_image():
        user = User.query.filter(User.session_token == current_user.get_id()).first()
        user_id = user.id
        user_dir_path = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
        if request.method == 'POST':
            if not os.path.exists(user_dir_path):
                os.makedirs(user_dir_path)
            if 'file' not in request.files:
                response = jsonify({
                    'errorMessage': 'file missing'
                })
                response.status_code = 422
                return response
            else:
                file_input = request.files['file']
                if file_input:
                    filename = secure_filename(file_input.filename)
                    file_input.save(os.path.join(user_dir_path, filename))
                    response = jsonify({
                        'url': url_for('upload_image',
                                       filename=filename)
                    })
                    response.status_code = 200
                    return response
        elif request.method == 'GET':
            filename = request.args.get('filename')
            filepath = os.path.join(user_dir_path, filename)
            if not os.path.exists(filepath):
                response = jsonify({
                    'errorMessage': 'file does not exist'
                })
                response.status_code = 404
                return response
            response = make_response(open(filepath, 'rb').read())
            response.content_type = "image/jpeg"
            response.status_code == 200
            return response

    return app
