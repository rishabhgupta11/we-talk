from flask import Flask, g, render_template, redirect, flash, url_for, abort, Response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import models
import forms
from timeago import format

app = Flask(__name__)
app.secret_key = 'wshofj90792jwfjw903u2m093840298.!rajrajhans!'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = models.Anonymous


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    # connect to the database
    g.db = models.DATABASE_proxy
    g.db.connection()
    g.user = current_user


@app.after_request
def after_request(response):
    # close database connection
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('You have successfully registered!', 'success')
        models.User.create_user(
            username=form.username.data,
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Email or password does not match", "danger")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Email or password does not match", "danger")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))


@app.route('/new_post', methods=('GET', 'POST'))
@login_required
def post():
    forme = forms.PostForm()
    if forme.validate_on_submit():
        if forme.image.data.filename:  # Image is present
            models.Post.create(user=g.user._get_current_object(),
                               content=forme.content.data.strip(),
                               image=forme.image.data.read(),
                               imageThere=1)
        else:  # No image uploaded
            models.Post.create(user=g.user._get_current_object(),
                               content=forme.content.data.strip())

        flash("Message Posted!", "success")
        return redirect(url_for('index'))
    return render_template('post.html', form=forme)


@app.route('/home')
def home():
    return render_template('homepage.html')


@app.route('/')
def index():
    stream = models.Post.select().order_by(models.Post.timestamp.desc())
    return render_template('stream.html', stream=stream, format=format)


@app.route('/about')
def about():
    return render_template('about.html')



