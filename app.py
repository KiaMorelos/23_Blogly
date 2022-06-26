"""Blogly application."""
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SECRET_KEY'] = "its_a_secret_to_everybody"
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """Home Page"""
    return redirect('/users')

### Users Routes ###
@app.route('/users')
def user_list_page():
    """Users Page View"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('/users/all-users.html', users=users)

@app.route('/users/new', methods=['GET'])
def get_user_form():
    """Add User Form View"""
    return render_template('/users/add-new-user.html')
    
@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Store Added User in Database"""
    
    new_user = User(first_name = request.form['firstname'],
    last_name = request.form['lastname'],
    image_url = request.form['url'] or None)
   
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """View User Details"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/user-details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Edit User Form View"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit-user-details.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Edit User Form Submit"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['firstname']
    user.last_name = request.form['lastname']
    user.image_url = request.form['url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete User"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

### Posts Routes ###
@app.route('/all-posts')
def show_all_posts():
    """Show all posts"""
    posts = Post.query.order_by(Post.title).all()

    return render_template('/posts/all-posts.html', posts=posts)

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Show New Post Form View"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('/posts/add-post-form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    """New Post Form Submit"""
    
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show Individual Post view with edit and delete buttons"""
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/post-details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Edit Post Form View"""
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Edit Post Form Submit"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete a Post"""
    post = Post.query.get_or_404(post_id)
    user = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user}')


### Tag Routes ###
@app.route('/tags')
def tag_list():
    """Show List View of all Tags with Links to tag details"""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('/tags/all-tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Tag Detail Page View"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/tag-details.html', tag=tag)

@app.route('/tags/new')
def new_tag_form():
    """Show Add Tag Form View"""
    return render_template('tags/add-tag-form.html')

@app.route('/tags/new', methods=['POST'])
def new_tag():
    """Tag form Submitted"""
    new_tag = Tag(name=request.form['name'])

    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Edit existing tag, show form view"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Tag edit form submitted"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete Tag"""
    tag = Tag.query.get_or_404(tag_id)    
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
