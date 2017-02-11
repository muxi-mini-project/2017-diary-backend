from functools import wraps 
from flask import abort , g  , request , jsonify  
from app.models import User
from flask_login import current_user 
#import base64

def admin_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        token_header = request.headers.get('Authorization',None)
        if token_header  :
            token_hash = token_header[6:]
            decode_token = token_hash
            token = decode_token[:-1]
            g.current_user = User.verify_auth_token(token)
            if not g.current_user.is_administrator() :
                return jsonify({'message' : '403 Forbidden'}) , 403
            return f(*args, **kwargs)
        else :
            return jsonify({'message':'401 unAuthorization'}) ,401
    return decorated 

            
