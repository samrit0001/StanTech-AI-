import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(username):
    exp_time = datetime.utcnow() + timedelta(hours=1)
    payload = {
        'username': username,
        'exp': exp_time
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def validate_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
