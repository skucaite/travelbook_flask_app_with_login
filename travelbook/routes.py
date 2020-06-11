import os
import secrets
# import babel
from PIL import Image
from flask import render_template, url_for, flash, request, redirect, abort
from travelbook import app, db, bcrypt, mail
from travelbook.forms import (TravelForm, GuideForm, RegistrationForm, LoginForm,
                    RequestResetForm, ResetPasswordForm)
from travelbook.models import Guide, Travel
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message



# ----------------------------------------------------------------#
# Controllers
# ----------------------------------------------------------------#
@app.route('/')
@app.route('/home')
@app.route('/travels')
def home():
    try:
        page = request.args.get('page', 1, type=int)
        travels=Travel.query.order_by(Travel.id.desc()).paginate(page=page, per_page=3)
    except Exception:
        abort(404)
    return render_template('home.html', travels=travels)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
# If we want just save picture:
    # form_picture.save(picture_path)

# This will resize picture (don't forget to install Pillow):
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
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

# ----------------------------------------------------------------#
#  Guides
# ----------------------------------------------------------------#
@app.route('/guides')
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
@app.route('/guides/<guide_id>')
def show_guide(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    travels = Travel.query.filter_by(guide_id=guide.id).all()
    guide.image_file = url_for('static', filename='profile_pics/' + guide.image_file)
    title = 'Guide ' + guide.name + ' ' + guide.surname
    return render_template('show_guide.html', guide=guide, travels=travels, title=title)

# Delete Guide
# ----------------------------------------------------------------#
@app.route('/guides/<guide_id>', methods=['POST', 'DELETE'])
def delete_guide(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    try:
        guide.delete()
        flash('Deleted!', 'success')
    except:
        flash('There was a problem deleting that guide', 'danger')
    return redirect('/guides')

# ----------------------------------------------------------------#
#  Travels
# ----------------------------------------------------------------#

# Show Travel
# ----------------------------------------------------------------#
@app.route('/travels/<travel_id>')
def show_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    title = 'Trip: ' + travel.title
    return render_template('show_travel.html', travel=travel, title=title)

# Create Travel
# ----------------------------------------------------------------#
@app.route('/travels/create', methods=['GET', 'POST'])
@login_required
def create_travel():
    form = TravelForm()
    if form.validate_on_submit():
        travel = Travel(title = form.title.data,
                        content = form.content.data,
                        guide = current_user)
        try:
            travel.insert()
            flash('Trip ' + form.title.data  + ' was successfully created!', 'success')
            return redirect('/travels')
        except:
            flash('An error occurred. Trip could not be created.', 'danger')
    return render_template('travel.html', title='New Travel', form=form, legend='New Travel')

# Update Travel
# ----------------------------------------------------------------#
@app.route('/travels/<travel_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_travel(travel_id):
    travel=Travel.query.get_or_404(travel_id)
    if travel.guide != current_user:
        abort(403)
    form = TravelForm()
    if form.validate_on_submit():
        travel.title = form.title.data
        travel.content = form.content.data
        try:
            travel.update()
            flash('Your travel has been updated!', 'success')
            return redirect(url_for('show_travel', travel_id=travel.id))
        except:
            flash('An error occurred. Trip could not be updated.', 'danger')
    elif request.method == 'GET':
        form.title.data = travel.title
        form.content.data = travel.content
    title = 'Trip ' + travel.title

    return render_template('travel.html', form=form, travel=travel,
                                title=title, legend='Update Travel')

# Delete Travel
# ----------------------------------------------------------------#
@app.route('/travels/<travel_id>/delete', methods=['POST', 'DELETE'])
def delete_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    try:
        travel.delete()
        flash('Deleted!', 'success')
    except:
        flash('There was a problem deleting that guide', 'danger')
    return redirect('/travels')

# Only Guides travels
# ----------------------------------------------------------------#
@app.route("/my_travels")
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
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='jurgita.codes@mail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
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


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
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
