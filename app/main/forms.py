coding: utf-8
from flask_wtf import Form
from wtforms import StringField , TextAreaField , SubmitField , FileField 
from wtforms.validators import Length , Required , Email 

class EditProfileForm(Form) :
    name = StringField('姓名',validators=[Length(0,64)])
    gender = StringField('性别',validators=[Length(0,6)])
    introduction = TextAreaField('时光简介')
    email = StringField('邮箱',validators=[Email()])
    sumbit = SubmitField('提交')
    portrait=FileField('上传头像') # 上传头像 ? 待定


#评论输入表单
class CommentForm(Form) :
    body = StringField('',validators=[Required()])
    submit = SubmitField('提交评论')

#日记文章表单
class PostForm(Form) :
    body = TextAreaField('这一刻你想说什么...')
    submit = SubmitField('发送') 
