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
