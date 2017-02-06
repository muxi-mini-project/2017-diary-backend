# coding: utf-8

from . import auth
from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from .forms import LoginForm

#登录路由
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect('main.index')
        flash('Invaild email or password.')
    return render_template('auth/login.html', form=form)

#用户登出路由
@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash('You have logged out !')
    return redirect(url_for('auth.login'))

#用户注册路由 ,发送邮件
@auth.route('/register',methods=['GET','POST'])
def register() :
    form = Register() 
    if form.validate_on_submit() :
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.passwors.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index')) #转到首页? 存疑 
    return render_template(' ') #存疑 

