#coding: utf-8
from flask import jsonify , g, request 
import json 
from ..models import User 
from  . import api
from .. import db

#查看个人资料
@api.route('/profile/<int:id>/',methods=['GET'])
def get_profiles(id) :
    use = User.query.get_or_404(id)
    return Response(json.dumps({
            "reaL_name" : user.real_name ,
            "gender" : user.gender ,
            "email" : user.email ,
            "portrait" : user.portrait ,
            "introduction" : user.introduction,
            "phone_number" : user.phone_number ,
            }) , mimetype="application/json" )


#编辑个人资料
@api.route('/profile/<int:id>/edit/',methods=['GET','PUT'])
def edit_profile(id) :
    if request.method == 'PUT' :
        user = User.query.get_or_404(id)
        user.real_name = request.get_json().get("real_name")
        user.gender = request.get_json().get("gender")
        user.email = request.get_json().get("gender")
        user.protrait = request.get_json().get("protrait")
        user.introduction = request.get_json().get("introduction")
        user.phone_number = request.get_json().get("phone_number")
        db.session.add(user)
        db.session.commit()
        return Response(json.dumps({
                "real_name" : user.real_name ,
                "gender" : user.gender ,
                "email" : user.email , 
                "portrait" : user.portrait ,
                "introduction" : user.introduction ,
                "phone_number" : user.phone_number ,
            }),mimetype="application/json")




























