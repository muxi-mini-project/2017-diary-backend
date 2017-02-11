#coding: utf-8
from flask import url_for , flash , request , g 
from flask_login import login_required , current_user
from .. import db 
from ..models import User 
from . import api 

#关注
@api.route('/follow/<username>',methods=['POST','GET'])
@login_required 
def follow(username): 
    user = User.query.filter_by(username=username).first()
    if user is None : 
        flash('该用户不存在.')
    if current_user.is_following(user) :
        flash('已关注该用户.')
    current_user.follow(user)
    flash('成功关注该用户!')
    
