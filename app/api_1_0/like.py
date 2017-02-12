#coding: utf-8
from flask import jsonify, Response , g ,request
import json 
from ..models import Like 
from . import api
from .. import db 

@api.route('/like/post/' ,methods=['POST','GET'])
def like_post() : 
    if request.method == 'POST' :
        like = Like()
        like.post_id = request.get_json().get('post_id')
        db.session.add(like)
        db.session.commit()
        return jsonify({ 'status' : 200 
                          })
        

