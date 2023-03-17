from flask import jsonify, request
from config import app, db
from models import User


@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200  

@app.route('/create-user', methods=['POST'])
def create_user():

    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return "user created successfully.", 201

@app.route('/user', methods=['GET'])
def get_user():

    user = User.query.get(request.args.get('id'))
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@app.route('/update-user', methods=['PUT'])
def update_user():

    data = request.get_json()
    user = User.query.get(data.get('id'))
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.to_dict()), 200


@app.route('/delete-user', methods=['DELETE'])
def delete_user():

    user = User.query.get(request.args.get('id'))
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return {"message": "user deleted successfully"}, 200
