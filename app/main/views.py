# coding: utf-8
from . import main
from flask import render_template


# test views
@main.route('/test/')
def test():
    return "<h1>just tell you everything is ok!</h1>"

# 待添加 关注路由 和 取消关注 路由 


# 查看关注者路由 
@main.route('/follwers/<username>')
def followers(username) :
    user = User.query.filter_by(username=username).first()
    if user is None :
        flash('该用户不存在')
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = user.followers.paginate(page,per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
                error_out=False)
    follows = [{'user':item.follower,'timestamp':item.timestamp} for item in pagination.items]
    return render_template('',user=user,pagination=pagination,follows=follows) # 渲染什么 ? 待定

#查看用户关注的人的路由 
@main.route('/following/<username>')
def following(username) :
    user = User.query.filter_by(username=username).first()
    if user is None :
        flash('该用户不存在')
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = user.followed.pagination(page,per_page=current_app.config['FLASKY_FOLLOWERS_PAGE'],error_out=False)
    follows = [{'user':item.followed,'timestamp':item.timestamp} for item in pagination.items]
    return render_template('',user=user,pagination=pagination,follows=follows) #待定
