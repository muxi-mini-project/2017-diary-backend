#coding: utf-8
from flask import url_for , flash , request , g ,jsonify
from flask_login import  current_user
from .. import db 
from ..models import User 
from . import api 
from app.decorators import login_required

#关注
@api.route('/follow/<id>',methods=['POST','GET'])
@login_required 
def follow(id): 
    user = User.query.filter_by(id=g.current_user.id).first()
    user.follow(User.query.filter_by(id=id).first())
    return jsonify({ 
           "message" : 'hah' })    

#关注者 
@api.route('/follower/<id>',methods=['GET'])
@login_required
def follower_of(id) :
    user = User.query.filter_by(id=id).first()
    followers = user.followers 
    return jsonify({ 
        "message" : [ item.follower_id for item in followers ] })
