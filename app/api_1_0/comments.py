#coding: utf-8
from flask import jsonify , request , g , url_for , current_app , Response  
from flask_login import current_user
from .. import db
from ..models import Post ,Comment 
from . import api
from app.decorators import login_required
import json 



#某篇日记的所有评论
@api.route('/posts/<int:id>/comments_view',methods=['GET'])
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



@api.route('/comments',methods=['POST','GET'])
def new_post_comment() :
    if request.method == 'POST' :
        comment = Comment()
        comment.post_id = request.get_json().get("post_id") #被评论的文章的id
        comment.body = request.get_json().get('body')
        comment.author_id = request.get_json().get('author_id') #评论者的id
       # comment.comment_id = request.get_json().get('comment_id') 

        db.session.add(comment)
        db.session.commit()
        return Response(json.dumps({
            "message" : "successful add a comment "}), mimetype='application/json')


























