import re
import datetime
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from restapi.models.user_models import Users
from restapi.utilities.validations import  check_format_of_phone_number, check_unfilled_fields,\
    check_length_of_fields, check_proper_email_format, check_special_characters


class UserController:

    def __init__(self):
        pass

    def create_users(self):
        users = Users()

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "400",
                "message": "A key is missing"
            })
        if check_unfilled_fields(data['username'], data['last_name'], data['othernames'],
                                 data['phone_number'], data['email'], data['password']):
            return jsonify({
                "status": "400",
                "message": "Please fill in a missing field"
            }), 400
        if check_length_of_fields(data['username'], data['last_name'], data['othernames']):
            return jsonify({
                "status": "400",
                "message": "The names should have a length of at most 30 characters"
            }), 400
        if check_special_characters(data['username']):
            return jsonify({
                "status": "400",
                "message": "The username should be a normal string without special characters"
            }),

        if len (data['phone_number']) < 10:
            return jsonify({
                "status": "400",
                "message": "The phone number should be a string of atleast 10 digits"
            }), 400
        if not check_format_of_phone_number(data['phone_number']):
            return jsonify({
                "status": "400",
                "message": "The phone number should be a string of only digits from 0 to 9"
            }), 400
        if not check_proper_email_format(data['email']):
            return jsonify({
                "status": "400",
                "message": "The email address is in the wrong format"
            }), 400
        user_exist = users.check_username_exists(username=data['username'])
        if user_exist:
            return jsonify({
                "status": 400,
                "message": "That username already exists"
            }), 400
        email_taken = users.check_email_exists(email=data['email'])
        if email_taken:
            return jsonify({
                "status": 400,
                "message": "That email is already taken"
            }), 400

        new = users.register_users(username=data['username'],
                                   email=data['email'],
                                   password=data['password'],
                                   firstname=data['first_name'],
                                   lastname=data['last_name'],
                                   othernames=data['othernames'],
                                   phonenumber=data['phone_number'])

        user_exist = users.check_username_exists(username=data['username'])
        token = {
            "user_id": user_exist['user_id']}
        current_user_id = token['user_id']

        exp = datetime.timedelta(days=3)

        token = create_access_token(
            identity=current_user_id, expires_delta=exp)
        return jsonify({
            "status": 201,
            "data": [{
                "token": token,
                "message": "User has been succesfully created"
            }]
        }), 201

    def login_user(self):
        """endpoint for logging in  users"""
        data = request.get_json()

        user = Users()

        user_login = user.check_login_user(data['username'], data['password'])

        if user_login:
            token = {
                "user_id": user_login['user_id']}
            current_user_id = token['user_id']

            exp = datetime.timedelta(days=4)

            token = create_access_token(
                identity=current_user_id, expires_delta=exp)
            return jsonify({
                "message": "successfully logged in",
                "token": token
            }), 200
        return jsonify({
            "status": 400,
            "message": "Please enter valid username and password"}), 400
