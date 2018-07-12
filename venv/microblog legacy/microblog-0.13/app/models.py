from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app, db, login


# followers = db.Table(
#     'followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
# )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    authenticated = db.Column(db.Boolean)
    # followed = db.relationship(
    #     'User', secondary=followers,
    #     primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # def follow(self, user):
    #     if not self.is_following(user):
    #         self.followed.append(user)

    # def unfollow(self, user):
    #     if self.is_following(user):
    #         self.followed.remove(user)

    # def is_following(self, user):
    #     return self.followed.filter(
    #         followers.c.followed_id == user.id).count() > 0

    # def followed_posts(self):
    #     followed = Post.query.join(
    #         followers, (followers.c.followed_id == Post.user_id)).filter(
    #             followers.c.follower_id == self.id)
    #     own = Post.query.filter_by(user_id=self.id)
    #     return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    #to authenticae users.
    def generate_account_comfirmation_token(self, expires_in=600):
        return jwt.encode({'auth_req': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
        

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)


'''
Classroom Model for the CBBAS.

Fields:

id: Class ID used to list class models within the database. Primary Key.
instructor: Instructor that runs the class. Initially, will be a one-to-one relationship.
start_date: Start Date of the class.
end_date: end date of the class.
curr_week: The current week fo the class.
attendance: Attendance data. Will be stored in a one-to-many relationship.
class_day_time: the day & time the class is run. one-to-one relationship. Will be implemented in the future.






The initiation form should contain the following information:

The implicit data that is already available are: {Instructor}

Class Name
Class Start Date
Class End Date
Classroom Schedule. {DAYS(multiple), {Start time, End time}}
    // meaning: classroom schedule can have multiple days a week in which it runs, and the form must adjust according to the requirements. Each day must have a start and end time, which must also be filled subsequently.


The data editing forms shoudl contain the following imformation:

FORM: ADD STUDENT

    <> Student Name (First, Last)
    <> Student SBUID

FORM: DELETE STUDENT

    <> Student SBUID

FORM: Edit Attendance:
 (TBD) -- according to database logic.


'''

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    current_week = db.Column(db.Integer)
    class_name = db.Column(db.String(70))
    # relationships
    # instructor: 1:1
    # attendance: 1:N
    # class_day_time: 1:1
    # <?> sudent_list  

    def __repr__(self):
        return '<Class {}>'.format(self.class_name)
'''

Student Model for the CBBAS


'''

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sbuid = db.Column(db.Integer, index=True, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    #relationships
    # class_id

# USER

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))