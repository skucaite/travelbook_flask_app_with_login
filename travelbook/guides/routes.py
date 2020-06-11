from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email




guides = Blueprint('guides', __name__)


@guides.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        guide = Guide(name = form.name.data,
                    surname = form.surname.data,
                    phone = form.phone.data,
                    email = form.email.data,
                    password = hashed_password)
        try:
            guide.insert()
            flash('Guide' + form.name.data + ' ' + form.surname.data + ' was successfully created!', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('An error occurred. Guide could not be created.', 'danger')
    return render_template('register.html', title='Register', form=form)


@guides.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Guide.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@guides.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@guides.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = GuideForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.phone = form.phone.data
        current_user.email = form.email.data
        current_user.update()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.phone.data = current_user.phone
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

#  All Guides
# ----------------------------------------------------------------#
@guides.route('/guides')
def guides():
    try:
        guides=Guide.query.all()
        for guide in guides:
            guide.image_file = url_for('static', filename='profile_pics/' + guide.image_file)
    except Exception:
        abort(404)
    return render_template('guides.html', guides=guides, title='Guides')

# Show Guide
# ----------------------------------------------------------------#
@guides.route('/guides/<guide_id>')
def show_guide(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    travels = Travel.query.filter_by(guide_id=guide.id).all()
    guide.image_file = url_for('static', filename='profile_pics/' + guide.image_file)
    title = 'Guide ' + guide.name + ' ' + guide.surname
    return render_template('show_guide.html', guide=guide, travels=travels, title=title)

# Delete Guide
# ----------------------------------------------------------------#
@guides.route('/guides/<guide_id>', methods=['POST', 'DELETE'])
def delete_guide(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    try:
        guide.delete()
        flash('Deleted!', 'success')
    except:
        flash('There was a problem deleting that guide', 'danger')
    return redirect('/guides')

# Only Guide's travels
# ----------------------------------------------------------------#
@guides.route("/my_travels")
@login_required
def guide_travels():
    page = request.args.get('page', 1, type=int)
    guide = current_user
    travels = Travel.query.filter_by(guide=guide)\
        .order_by(Travel.id.desc())\
        .paginate(page=page, per_page=3)
    return render_template('guide_travels.html', travels=travels, guide=guide)

# ----------------------------------------------------------------#
# Password reset
# ----------------------------------------------------------------#
@guides.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Guide.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@guides.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Guide.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        try:
            user.update()
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('An error occurred. Guide could not be created.', 'danger')
    return render_template('reset_token.html', title='Reset Password', form=form)
