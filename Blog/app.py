from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json

with open('config.json','r') as c:
    params = json.load(c)["params"]
local_server = True


app = Flask(__name__)


# MAIL

# app.config.update(
#     MAIL_SERVER =  'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['gmail-user'],
#     MAIL_PASSWORD = params['gmail-password']
#     )
# mail = Mail(app)


if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']


# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:database123@localhost:3306/flask_tutorial"

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.String(20), nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    img_file = db.Column(db.String(12), nullable=False)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact", methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, phone_num=phone, msg=message, email=email)

        db.session.add(entry)
        db.session.commit()

        # mail.send_message('New message from ' + name,
        #                     sender = email,
        #                     recipients = [params['gmail-user']],
        #                     body = message + "\n" + phone
        #                     )

    return render_template('contact.html')


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html', params=params, post=post)

# @app.route("/post")
# def post():
#     return render_template('post.html')


app.run(debug=True)