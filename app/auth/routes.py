from app.auth.forms import LoginForm
from app.models import User

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user

from app.auth import bp

@bp.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        if user.is_admin:
            return redirect(url_for('admin.admin'))
        return redirect(url_for('index'))

    if 'token' in request.args:
        user = User.query.filter_by(username=request.args.get('user')).first()
        if user is not None or user.token == request.args.get('token'):
            login_user(user, remember=True if 'remember' in request.args else False)
            return redirect(url_for('index'))
        else:
            flash('Invalid token')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', title='Sign In', form=form)
