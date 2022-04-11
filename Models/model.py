from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



class User():
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True,)
    password = db.Column(db.String(60), nullable=False)
    phoneNumber = db.Column(db.String(60))
    age = db.Column(db.Integer)
    description = db.Column(db.Text ,default='')
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User('username {self.firstName}', 'email :{self.email}', 'password :{self.password}')"


class Picture_Admin(db.Model):
    picture_id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))


class Admin(db.Model, User):
    pictures = db.relationship('Picture_Admin', backref="admin")
    comments = db.relationship('Comment', backref="admin")
    notification = db.relationship('Notification', backref="admin")
    carote = db.relationship('Carote', backref="admin")
    posts = db.relationship('Post', backref="admin")
    NumberOfCarrot = db.Column(db.Integer, default=0)
    NumberOfGifts = db.Column(db.Integer, default=0)
    deleted = db.Column(db.DateTime)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))


class Admin3dwave(db.Model, User):
    pictures = db.relationship('Picture_Admin3dWave', backref="admin3dwave")


class Picture_Admin3dWave(db.Model):
    picture_id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    admin3dWave_id = db.Column(db.Integer, db.ForeignKey("admin3dwave.id"))


class Employees(db.Model, User):
    pictures = db.relationship('Picture_Employees', backref="employees")
    comments = db.relationship('Comment', backref="employees")
    deleted = db.Column(db.DateTime)
    NumberOfCarrot = db.Column(db.Integer, default=0)
    NumberOfGifts = db.Column(db.Integer, default=0)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    notification = db.relationship('Notification', backref="employees")
    # senders=db.relationship('Carote',backref="employees_sender")
    # receivers=db.relationship('Carote',backref="employees")


class Picture_Employees(db.Model):
    picture_id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(120),default="")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text,default='')
    likes_user = db.Column(db.Text,default="")
    title = db.Column(db.String(120))
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    pictures = db.relationship('Picture_Post', backref="post")
    comments = db.relationship('Comment', backref="post")


class Picture_Post(db.Model):
    picture_id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=True)


class Logo(db.Model):
    picture_id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(120),unique=True,)
    nbEmployee = db.Column(db.String(120),default=0)
    logo =db.relationship('Logo', backref="company")
    employees = db.relationship('Employees', backref="company")
    admin =db.relationship('Admin', backref="company" ,)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))


class Carote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.Text)
    date_activities = db.Column(db.DateTime, default=datetime.utcnow)
    accepted = db.Column(db.Boolean, default=None)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    sender_id = db.Column(db.String(120))
    receiver_id = db.Column(db.String(120))


