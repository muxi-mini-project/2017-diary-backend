# coding: utf-8
from . import main
from flask import render_template


# test views
@main.route('/test/')
def test():
    return "<h1>just tell you everything is ok!</h1>"



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


# 支持博客文章评论
@main.route('/posts/<int:id>',methods=['GET','POST'])
def post(id) :
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit() :
        comment = Comment(body=form.body.data ,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('评论已发布')
        return redirect(url_for('.post',id=post.id,page=-1))
    page = request.args.get('page',1,type=int)
    if page == -1 :
        page = (post.comments.count()-1) / current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).pagination(
            page,per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
            error_out=False)
    comments = pagination.itmes 
    return render_template('post.html',posts=[post],form=form,
            comments=comments,pagination=pagination) # 存疑 另: 如何在首页加入指向评论的链接


# 处理博客文章的首页路由
@main.route('/',methods=['GET','POST']) # 为什么是这样的 ? 
def index() :
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \  # 是否需要检验能有写日记  ?
            form.validate_on_submit() :
        post  = Post(body=form.body.data,
                     author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('   ',form=form,posts=posts) # 待定 

#点赞
@main.route('/like_post',methods=['POST'])
@login_required
def like_post() :
    if  current_user.is_authenticated :
          post = Post.query.get_or_404(int(request.form.get('id')))  #post 方法的数据存在request.form.get里
        if current_user.like_post(post):
            return 'like'
        else:
            return 'cancel'
