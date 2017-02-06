# coding: utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField , BooleanField 
from wtforms.validators import DataRequired ,Email , Length 
from ..models import User 
from wtforms import ValidationError 

class LoginForm(Form):
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired(), Email(), Length(1,64) ]
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')
    

#用户注册表单
class Register(Form):
    email = StringField('email',validators=[DataRequired() , Length(1,64),Email()])
    username =
    StringField('username',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名必须只包括数字,字母,下划线或点号.')])
    password = PasswordField('password',validators=[DataRequired(),EqualTo('password2',message='两次密码输入不一致')])

    passwod2 = PasswordField('确认密码' , validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册!')

    def validate_username(self,field) :
        if User.query.filter_by(username=field.data).first() :
            raise ValidationError('用户已存在!')
    



