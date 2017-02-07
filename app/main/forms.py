# coding: utf-8
from flask_wtf import Form
# from wtforms import
# from wtforms.validators import

class EditProfileForm(Form) :
    name = StringField('姓名',validators=[Length(0,64)])
    gender = StringField('性别',validators=[Length(0,6)])
    introduction = TextAreaField('时光简介')
    email = StringField('邮箱',validators=[Email()])
    sumbit = SubmitField('提交')
    portrait=FileField('上传头像') # 上传头像 ? 待定
