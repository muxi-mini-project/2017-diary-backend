#coding: utf-8
from flask import jsonify , request , g , abort , url_for , current_app
from ..  import db 
from ..models import Post , Permission 
from . import api 

#上传日记
@api.route('/edit_diary' ,methods=['POST','GET'])
def new_post() :
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201 , \
            {'Location': url_for('api.get_post',id=post.id , _external=True)} #待定 



            
#查看日记(所有) 
@api.route('/posts',methods=['GET']) # 注意 
def get_posts() :
    page = request.args.get('page',1,type=int)
    pagination = Post.query.paginate(
            page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE)'] ,
            error_out=False)
    posts = pagination.items 
    prev = None
    if pagination.has_prev :
        prev = url_for('api.get_posts',page=page-1,_external= True)
    next = None 
    if pagination.has_next :
        next = url_for('api.get_posts',page=page+1,_external=True)
    return jsonify({
        'posts' : [post.to_json() for post in posts ] , 
        'prev' : prev ,
        'next' : next ,
        'count' : pagination.total ,
        }) 
    # 就只用返回这些 ? ? 

    
#查看日记(一篇) 
@api.route('/posts/<int:id>',methods=['GET'])
def get_post(id) :
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())



























