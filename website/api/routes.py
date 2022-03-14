from flask import Blueprint, jsonify, request
from flask_login import login_required
from website.helpers import token_required
from website.models import db, User, Post, post_schema, posts_schema

api = Blueprint('api',__name__, url_prefix = '/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return jsonify({ 'some': 'value',
                    'Other': 22.7,
                    'random': 'thing'})


# CREATE Post Route
api.route('/posts', medthods=['POST'])
@token_required
def create_post(current_user_token):
    title = request.json['title']
    description = request.json['description']
    price = request.json['price']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    img_url = request.json['img_url']
    model_url = request.json['model_url']
    user_token = current_user_token.token

    post = Post(title, description, price, dimensions, weight, img_url, model_url, user_token)

    db.session.add(post)
    db.session.commit()

    response = post_schema.dump(post)
    return jsonify(response)

# Retrieve All posts
@api.route('/posts', methods=['GET'])
@token_required  #won't need this for final inventory site, remove when ready
def get_posts(current_user_token):  #revise the current_user_token condition
    owner = current_user_token.token
    posts = Post.query.filter_by(user_token = owner).all()
    response = posts_schema.dump(posts)
    return jsonify(response)

# Retrieve a post
@api.route('/post/<id>', methods=['GET'])
@token_required #won't need this for final inventory site, remove when ready
def get_post(current_user_token, id):
    owner = current_user_token.token
    post = Post.query.get(id)
    response = post_schema.dump(post)
    return jsonify(response)

# Update a post
@api.route('/posts/<id>', methods=['POST', 'PUT'])
@token_required
def update_post(current_user_token, id):
    post = Post.query.get(id) 

    post.title = request.json['title']
    post.description = request.json['description']
    post.price = request.json['price']
    post.dimensions = request.json['dimensions']
    post.weight = request.json['weight']
    post.img_url = request.json['img_url']
    post.model_url = request.json['model_url']

    db.session.commit()
    response = post_schema.dump(post)
    return jsonify(response)

# Delete a post
@api.route('/posts/<id>', methods = ['DELETE'])
@token_required
def delete_post(current_user_token, id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()

    response = post_schema.dump(post)
    return jsonify(response)
