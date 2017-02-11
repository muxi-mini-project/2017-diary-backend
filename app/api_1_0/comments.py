#coding: utf-8
from flask import jsonify , request , g , url_for , current_app
from .. import db
from ..models import Post ,Comment 
from . import api
from app.decorators import login_required


#某篇日记的所有评论
@api.route('/posts/<int:id>/comments_view',methods=['POST'])
def get_post_comments(id) :
    post = Post.query.get_or_404(id)
    page = request.args.get('page',1,type=int)
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
            page,per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
            error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_post_comments', id=id,page=page-1,
                        _external=True)
    next = None 
    if pagination.has_next :
        next = url_for('api.get_post_comments', id=id,page=page+1,
                        _external=True)

    return jsonify ({
        'comments' : [comment.to_json() for comment in comments ] ,
        'prev' : prev ,
        'next' : next ,
        'count' : pagination.total 

        })
    # 只用返回这些 ????



# 发评论 , 需不需要验证权限 ?????
@api.route('/posts/<int:id>/comments',methods=['POST'])
@login_required
def new_post_comment(id) :
    post = Post.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()) , 201, \
            {'Location' : url_for('api.get_post_commets' , id = comment.id ,
                          _external = True )}



























