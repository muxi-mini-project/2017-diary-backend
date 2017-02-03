# coding: utf-8
from . import main
from flask import render_template


# test views
@main.route('/test/')
def test():
    return "<h1>just tell you everything is ok!</h1>"

#首页获取关注者日记的路由
@app.route('/users/<int:id>/',methods=['GET'])
@login_required


