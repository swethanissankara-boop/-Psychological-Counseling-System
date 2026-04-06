from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user
from models import User
from extensions import db
from forms import LoginForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data, role='jp')
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect('/jp/dashboard')
    return render_template('jp_login.html', form=form)

@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')