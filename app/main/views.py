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




#关注路由
@main.route('follow/<username>')
@login_required
def follow(username) :
    user = User.query.filter_by(username=username).first()
    if  user is None : 
        flash('该用户不存在')
        return redirect(url_for('.index')) # 返回首页 ? 
    if current_user.is_following(user) : 
        flash('早已关注该用户!')
        return redirect(url_for('.user',username=username))
    current_user.follow(user)
    flash('成功关注 %s!' % username )
    return redirect(url_for('.user',username=username))

#取消关注路由
@main.route('unfollow/<username>')
@login_required
def unfollow(username) :
    user = User.query.filter_by(username=username).first()
    if user is None :
        flash('该用户不存在')
        return redirect(url_for('.index')) # 存疑
    if not current_user.is_following(user) :
        flash('早已取消关注该用户!')
        return redirect(url_for('.user',username=username))
    current_user.unfollow(user)
    flash('已取消关注 %s .' % username )
    return redirect(url_for('.user',username=username))


#编辑资料的路由 , 包括头像上传
@main.route('/edit_profile',methods=['GET','POST'])
@login_required 
def edit_profile() :
    form = EditProfileForm()
    if form.validate_on_submit() :
        current_user.name = form.name.data
        current_user.gender = form.gender.data
        current_user.introduction = form.introduction.data 
        current_user.phone_number = form.phone_number.data
        portrait = request.files['portrait']
        fname = portrait.filename
        flag = '.' in fname and fname.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS'] 
        if not flag :
            flash('头像格式错误')
            return redirect(url_for('.user',username=username))
        portrait.save('{}{}_{}'.format(current_app.config['UPLOAD_FOLDER'], current_user.username, fname))
        current_user.portrait = '{}_{}'.format(current_user.username, fname)
        db.session.add(current_user)
        db.session.commit()
    form.name.data = current_user.name
    form.gender.data = current_user.gender 
    form.introduction.data = current_user.introduction
    form.phone_number.data = current_user.phone_number
    return render_template('') # 待定 , 其实这个地方我很疑惑 QWQ!



