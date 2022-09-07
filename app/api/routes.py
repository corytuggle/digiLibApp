from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Hello': 'World'}

# CREATE
@api.route('/books', methods=['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    illustrator = request.json['illustrator']
    isbn10 = request.json['isbn10']
    isbn13 = request.json['isbn13']
    product = request.json['product']
    narrator = request.json['narrator']
    publisher = request.json['publisher']
    yearmd = request.json['yearmd']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(title, author, illustrator, isbn10, isbn13, product, narrator, publisher, yearmd, user_token=user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

# RETRIEVE
# all books
@api.route('/books', methods=['GET'])
@token_required
def get_all_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# single book
@api.route('/books/<id>', methods=['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

# UPDATE
@api.route('/books/<id>', methods=['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.title = request.json['title']
    book.author = request.json['author']
    book.illustrator = request.json['illustrator']
    book.isbn10 = request.json['isbn10']
    book.isbn13 = request.json['isbn13']
    book.product = request.json['product']
    book.narrator = request.json['narrator']
    book.publisher = request.json['publisher']
    book.yearmd = request.json['yearmd']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# DELETE
@api.route('/books/<id>', methods=['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)