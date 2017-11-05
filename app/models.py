from datetime import datetime
import hashlib
from werkzeug.security import  generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request
from flask_login import UserMixin,AnonymousUserMixin
from . import db,login_manager

class Permission:
    OPERATE = 0x01
    APPROVE = 0x02
    ADMINISTOR=0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer)
    users =db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles={
            'Operator':(Permission.OPERATE,True),
            'Manager':(Permission.APPROVE,False),
            'Administrator':(0xff,False)
        }
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.permissions=roles[r][0]
            role.default=roles[r][1]
            db.session.add(role)

        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64))
    user_id= db.Column(db.String(10),unique=True,index=True)
    status=db.Column(db.Boolean,default=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash=db.Column(db.String(128))

    @staticmethod
    def init_users():
        userlist={
            '001':('o001','001','Operator'),
            '002':('m002','002','Manager'),
            '003':('a003','003','ADMINISTOR')
        }
        for u in userlist:
            role =Role.query.filter_by(name=userlist[u][2]).first()
            if role is None:
                role=Role.query.filter_by(default=True).first()
            u=User(user_id=userlist[u][1],username=userlist[u][0],role=role,password=userlist[u][1])

            db.session.add(u)

        db.session.commit()

    def __init__(self,**kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role=Role.query.filter_by(default=True).first()


    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def can(self,permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.OPERATE)

    def get_user_by_id(user_id):
        return User.query.filter_by(user_id=user_id).first()



    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(selfself,permissions):
        return False
    def is_adminsitrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LG(db.Model):
    __tablename__ = 'lg_gts'
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(5), index=True)
    no= db.Column(db.String(20),unique=True,index=True)
    companyname = db.Column(db.String(64))
    amt = db.Column(db.String(64))

    custom_no=db.Column(db.String(10))

    createdate = db.Column(db.String(8),index=True)
    updatedate = db.Column(db.String(8))
    status = db.Column(db.Integer)
    def __init__(self,**kwargs):
        super(LG,self).__init__(**kwargs)
    def get_by_no(no):
        return LG.query.filter_by(no=no).first()












