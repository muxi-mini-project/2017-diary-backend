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
           "message" : 'successfully follow' })    
#取消关注 
@api.route('/unfollow/<id>',methods=['POST','GET'])
@login_required
def unfollow(id) :
    user = User.query.filter_by(id=g.current_user.id).first()
    user.unfollow(User.query.filter_by(id=id).first())
    return jsonify({ 
        "message" : 'successfully unfollow'})


#关注者 
@api.route('/follower/<id>',methods=['GET'])
@login_required
def follower_of(id) :
    user = User.query.filter_by(id=id).first()
    followers = user.followers 
    return jsonify({ 
        "message" : [ item.follower_id for item in followers ] })

#查看关注他的人
@api.route('/followed/<id>',methods=['GET'])
@login_required
def followed_of(id) :
    user = User.query.filter_by(id=id).first()
    followed = user.followed 
    return jsonify ({
        "message" : [ item.followed_id for item in followed ]  })
