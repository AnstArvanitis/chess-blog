from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
# Import forms from local forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

# --- ENVIRONMENT CONFIGURATION ---
# Load environment variables from .env file only if the file exists (Local Development).
# On Render, variables are loaded from the Dashboard settings.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is not installed/needed in production


'''
===========================================================
APP CONFIGURATION & SETUP
===========================================================
'''


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login to manage user sessions
login_manager = LoginManager()
login_manager.init_app(app)

# Configure Gravatar for user profile images
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

'''
===========================================================
DATABASE MODELS
===========================================================
'''
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(UserMixin, db.Model):
    """
    User Table: Stores registered user information.
    Acts as Parent to both 'BlogPost' and 'Comment' tables.
    """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    
    # Relationships
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


class BlogPost(db.Model):
    """
    BlogPost Table: Stores blog articles.
    Child of 'User' (Author). Parent to 'Comment'.
    """
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Foreign Key to User (Author)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    
    # Relationship to Comments
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    """
    Comment Table: Stores user comments on blog posts.
    Child of both 'User' (Commenter) and 'BlogPost' (Parent Post).
    """
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Connection to User (Comment Author)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    
    # Connection to BlogPost (Parent Post)
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")


# Initialize Database
with app.app_context():
    db.create_all()


'''
===========================================================
HELPER FUNCTIONS & DECORATORS
===========================================================
'''
@login_manager.user_loader
def load_user(user_id):
    """ Flask-Login helper to retrieve user object from DB via ID. """
    return db.get_or_404(User, user_id)


def admin_only(f):
    """
    Custom Decorator: Checks if the current user is authenticated AND has ID=1 (Admin).
    If not, returns 403 Forbidden.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


'''
===========================================================
ROUTES (VIEWS)
===========================================================
'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Handles new user registration using hashing for password security. """
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        
        # Hash Password and Create User
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
        
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handles user login by verifying email and hashed password. """
    form = LoginForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        
        # Validation Logic
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, form.password.data):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
            
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    """ Logs out the current user and redirects to home. """
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    """ Homepage: Displays all blog posts ordered by creation. """
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    """
    Renders an individual post.
    Handles the CommentForm submission if user is logged in.
    """
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()
    
    # Handle Comment Submission
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
            
        new_comment = Comment(
            text=form.comment_text.data,
            comment_author=current_user, # Link to User
            parent_post=requested_post   # Link to Post
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))

    return render_template("post.html", post=requested_post, form=form, current_user=current_user)


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    """ Admin Only: Create a new blog post. """
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    """ Admin Only: Edit an existing blog post. """
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    """ Admin Only: Delete a blog post. """
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=False, port=5002)