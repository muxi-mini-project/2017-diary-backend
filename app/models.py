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
        raise AttributeError('password is not readable')

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

