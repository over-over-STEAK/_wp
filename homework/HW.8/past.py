from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from src.models.post import Post
from src.models.user import User
from src.main import db

post_bp = Blueprint('post', __name__)


def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None


@post_bp.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    user = get_current_user()
    return render_template('index.html', posts=posts, user=user)


@post_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    user = get_current_user()
    if not user:
        flash('You must be logged in to create a post.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash('Title and content are required.', 'error')
            return render_template('new_post.html', title=title, content=content)

        new_post = Post(
            title=title,
            content=content,
            user_id=user.id
        )
        db.session.add(new_post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('post.index'))

    return render_template('new_post.html')


@post_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    user = get_current_user()
    if not user:
        flash('You must be logged in to delete a post.', 'error')
        return redirect(url_for('auth.login'))

    post = Post.query.get_or_404(post_id)

    if post.user_id != user.id:
        flash('You can only delete your own posts.', 'error')
        return redirect(url_for('post.index'))

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully!', 'success')
    return redirect(url_for('post.index'))
