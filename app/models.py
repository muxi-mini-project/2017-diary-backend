# coding: utf-8
"""
sql models

    use: Flask-SQLAlchemy
    -- http://flask-sqlalchemy.pocoo.org/2.1/

"""

from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin, current_user
from wtforms.validators import Email

# permissions
class Permission:
    """
    1. COMMENT: 0x01
    2. MODERATE_COMMENTS: 0x02
    3. ADMINISTER: 0x04
    """
    COMMENT = 0x01
    MODERATE_COMMENTS = 0x02
    ADMINISTER = 0x04


# user roles
class Role(db.Model):
    """
    1. User: COMMENT
    2. Moderator: MODERATE_COMMENTS
    3. Administrator: ADMINISTER
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.COMMENT, True),
            'Moderator': (Permission.COMMENT |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (
                Permission.COMMENT |
                Permission.MODERATE_COMMENTS |
                Permission.ADMINISTER,
                False
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    """user"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(164), unique=True, index=True)
    email = db.Column(db.String(164), info={'validator' : Email()})
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(164))
    portrait = db.Column(db.String(128),default='None') # 默认头像是什么 ?  待定
    name = db.Column(db.String(64))
    introduction = db.Column(db.Text())
    gender = db.Column(db.String(6)) # 性别应该如何选择 ? 
    phone_number = db.Column(db.String(11))  
    comments = db.relationship('Comment',backref='author',lazy='dynamic')
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    followed = db.relationship('Follow' ,
                                foreign_keys=[Follow.follower_id] ,
                                backref=db.backref('follower',lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    followers = db.relationship('Follow' ,
                                foregin_keys=[Follow.followed_id] ,
                                backref=db.backref('followed',lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
                                

    @property
    def password(self):
        raise AttributeError('password is not readable') # 密码不可读 ? 

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def is_admin(self):
        if self.role_id == 2:
            return True
        return False

    def __repr__(self):
        return "<User %r>" % self.username

    # 生成令牌
    def generate_token(self,expiration=1800) :
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    # 检验令牌
    def confirm(self,token) :
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        try : 
            data = s.loads(token)
        except : 
            return False
        if  data.get('confirm') != self.id :
            return False 
        self.comfirmed = True 
        db.session.add(self)
        db.session.commit()
        return True 

    #关注关系的辅助方法
    def follow(self,user) :
        if not self.is_following(user) :
            f = Follow(follower=self,followed=user)
            db.session.add(f)
            db.seesion.commit()

    def unfollow(self,user) :
        f = self.followed.filter_by(followed_id=user.id).first()
        if f :
            db.session.delete(f)
            db.session.commit()
            
    def is_following(self,user) :
        return self.followed.filter_by(followed_id=user.id).first() is not  None 

    def is_followed_by(self,user) :
        return self.followers.filter_by(follower_id=user.id).first() is not  None
  
   # 点赞
    def vote_post(self, post):
        vote = self.voted_posts.filter_by(post_id=post.id).first()
        if vote is None:
            vote = PostVote(user_id=self.id,post_id=post.id)
            db.session.add(vote)
            db.session.commit()
            return True
        else  :
            db.session.delete(vote)
            db.session.commit()                                                                                    
            return False


#关注关联表的模型实现
class Follow(db.Model) :
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    fokkowed_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow) #是否需要关注时间 ? 暂定



class AnonymousUser(AnonymousUserMixin):
    """ anonymous user """
    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser

# you can writing your models here:

# 评论模型
class Comment(db,Model) :
    __table__ = 'comments' 
    id = db.Column(db.Integer , primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text) #存疑 ? 
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator) :
        allowed_tags = ['a','abbr','acronym','b','code','em','i','strong']
        target.body_html =
        bleach.linkify(bleach.clean(markdown(value,output_format='html'),tags=allowed_tags,strip=True))

db.event.listen(Comment.body,'set',Comment.on_changed_body) # 存疑

class Post(db.Model) :
    __tablename__ = 'posts' 
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer , db.ForeignKey='users.id')
    comments = db.relationship('Comment',backref='post',lazy='dynamic')
    likes = db.relationship('Like',backref='post', lazy='dynamic')
    
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b','blockquote', 'code',
                        'em', 'i', 'li', 'ol',  'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3','p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value,output_format='html'),
            tags=allowed_tags,strip=True))

    def to_json(self) :
        json_post = { 
                'url' : url_for('api.get_post',id=self.id , _external=True) ,
                'body' : self.body , 
                'body_html' : self.body_html , 
                'timestamp' : self.timestamp ,
                'author' : url_for('api.get_user',id=self.author_id,_external=True) ,
                'comments' : url_for('api.get_post_comments',id=self.id ,_external=True) ,
                'comment_count' : self.comments.count() ,
                'like_count' : self.likes.count() ,
                
                }
        return json_post 

    
    @staticmethod
    def from_json(json_self) :
        body = json_post.get('body')
        return  Post(body=body)

#点赞
class Like(db.Model) :
    __table__ = 'like' 
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey='posts.id')

    def __repr__(self):
        return "<Like %r>" % self.id

