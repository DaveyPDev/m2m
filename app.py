"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """ Homepage """

    return redirect('/users')

''' Users route '''
@app.route('/users')
def user_list():
    """ User Info"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """ Show new user form """

    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def new_user():
    """ Submit new user form """

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_info(user_id):
    """ show user info """

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """ shows user editing form """

    user= User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']  

    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

''' Post Route '''

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """ Show form for new post"""

    user = User.query.get_or_404(user_id)

    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_new(user_id):
    """ Handle submission form for new post of {user_id} """

    user = User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form['title'],
        content = request.form['content'],
        user = user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):

    post = Post.query.get_or_404(post_id)
    return  render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_posts(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    flash(f"Post '{post.title}' edited")

    db.session.add(post_id)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_posts(post_id):

    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted")

    return redirect(f"/users/{post.user_id}")
