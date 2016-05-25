#!/usr/bin/python
# coding=utf-8
from flask import Blueprint, current_app, request
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.api import status
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

prefix_module = 'authentication'
authentication = Blueprint(prefix_module, __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(username)
    except SignatureExpired:
        print('Expire')
        return False  # valid token, but expired
    except BadSignature:
        print('Bad signature')
        return False  # invalid token

    return True
    ## End Verify_password

    # if username != 'hola':
    #     return False
    #
    # return True


## End verify_password

@authentication.route('/token', methods=['GET', 'POST'])
def generate_token():
    try:
        json_info = request.json
    except Exception as e:
        return {'error': 'It is not JSON information'}, status.HTTP_400_BAD_REQUEST

    if json_info is None:
        return {'error': 'It is not JSON information'}, status.HTTP_400_BAD_REQUEST

    username = json_info['username']
    password = json_info['password']

    if username == 'nestor' and password == 'hola':
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=60 * 60 * 24 * 30)
        token = s.dumps({})
        return {'status': 'Ok', 'token': token}
    # str(variable) para convertir en string

    return {'status': 'Error', 'message': 'User or password was not found'}, status.HTTP_404_NOT_FOUND

## End generate_token
