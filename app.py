import os
import sys
import babel
from flask import Flask, render_template, url_for, flash, request, redirect, abort   # jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException


from .forms import TravelForm, GuideForm, Registration, LoginForm
from .models import setup_db, Guide, Travel, db, db_drop_and_create_all


app = Flask(__name__)
setup_db(app)
migrate = Migrate(app, db)
CORS(app)

# ----------------------------------------------------------------#
# Controllers
# ----------------------------------------------------------------#
@app.route('/')
@app.route('/home')
def home():
    try:
        page = request.args.get('page', 1, type=int)
        travels=Travel.query.paginate(page=page, per_page=3)
    except Exception:
        abort(404)
    return render_template('home.html', travels=travels)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = GuideForm()
    if form.validate_on_submit():
        flash(f'Account created for guide {form.name.data} {form.surname.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    return render_template('login.html', title='Login')



# ----------------------------------------------------------------#
#  Guides
# ----------------------------------------------------------------#
@app.route('/guides')
def guides():
    try:
        guides=Guide.query.all()
    except Exception:
        abort(404)
    return render_template('guides.html', guides=guides, title='Guides')

# Show Guide
# ----------------------------------------------------------------#
@app.route('/guides/<guide_id>')
def show_guide(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    travels = Travel.query.filter_by(guide_id=guide.id).all()
    data = {
        "id": guide.id,
        "name": guide.name,
        "surname": guide.surname,
        "phone": guide.phone,
        "email": guide.email,
        "image_file": guide.image_file,
    }
    title = 'Guide ' + guide.name + ' ' + guide.surname
    return render_template('show_guide.html', guide=guide, travels=travels, title=title)

# Create Guide
# ----------------------------------------------------------------#
@app.route('/guides/create', methods=['GET'])
def create_guide_form():
    form = GuideForm()
    return render_template('new_guide.html', form=form)

@app.route('/guides/create', methods=['POST'])
def create_guide():
    try:
        form = GuideForm()
        guide = Guide(name = form.name.data, surname = form.surname.data, phone = form.phone.data, email = form.email.data)
        guide.insert()
        flash('Guide ' + form.name.data + ' ' + form.surname.data  + ' was successfully created!', 'success')
    except:
        flash('An error occurred. Guide could not be created.', 'danger')
    return render_template('show_guide.html', form=form, guide=guide)

# Update Guide GET
# ----------------------------------------------------------------#
@app.route('/guides/<guide_id>/edit', methods=['GET'])
def edit_guide_form(guide_id):
    guide=Guide.query.get_or_404(guide_id)
    form = GuideForm()
    form.name.data = guide.name
    form.surname.data = guide.surname
    form.phone.data = guide.phone
    form.email.data = guide.email

    title = 'Guide ' + guide.name + ' ' + guide.surname

    return render_template('edit_guide.html', form=form, guide=guide, title=title)

# Update Guide Travel
# ----------------------------------------------------------------#
@app.route('/guides/<guide_id>/edit', methods=['POST'])
def edit_guide(guide_id):
    guide=Guide.query.get_or_404(guide_id)
    form = GuideForm()
    guide.name = form.name.data
    guide.surname = form.surname.data
    guide.phone = form.phone.data
    guide.email = form.email.data
    guide.update()

    title = 'Guide ' + guide.name + ' ' + guide.surname

    return render_template('show_guide.html', form=form, guide=guide, title=title)

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
@app.route('/travels')
def travels():
    page = request.args.get('page', 1, type=int)
    travels=Travel.query.paginate(page=page, per_page=3)
    return render_template('travels.html', travels=travels)

# Show Travel
# ----------------------------------------------------------------#
@app.route('/travels/<travel_id>')
def show_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    title = 'Trip: ' + travel.title
    return render_template('show_travel.html', travel=travel, title=title)

# Create Travel
# ----------------------------------------------------------------#
@app.route('/travels/create', methods=['GET'])
def create_travel_form():
    form = TravelForm()
    return render_template('new_travel.html', form=form)

@app.route('/travels/create', methods=['POST'])
def create_travel():
    try:
        form = TravelForm()
        travel = Travel(title = form.title.data, content = form.content.data, guide_id = form.guide_id.data)
        travel.insert()
        flash('Trip ' + form.title.data  + ' was successfully created!', 'success')
    except:
        flash('An error occurred. Trip could not be created.', 'danger')
    return render_template('show_travel.html', form=form, travel=travel)

# Update Travel GET
# ----------------------------------------------------------------#
@app.route('/travels/<travel_id>/edit', methods=['GET'])
def edit_travel_form(travel_id):
    travel=Travel.query.get_or_404(travel_id)
    form = TravelForm()
    form.title.data = travel.title
    form.content.data = travel.content
    form.guide_id.data = travel.guide_id

    title = 'Trip ' + travel.title

    return render_template('edit_travel.html', form=form, travel=travel, title=title)

# Update Travel POST
# ----------------------------------------------------------------#
@app.route('/travels/<travel_id>/edit', methods=['POST'])
def edit_travel(travel_id):
    travel=Travel.query.get_or_404(travel_id)
    form = TravelForm()
    travel.title = form.title.data
    travel.content = form.content.data
    travel.guide_id = form.guide_id.data
    travel.update()

    title = 'Trip ' + travel.title

    return render_template('show_travel.html', travel=travel, form=form, title=title)

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


if __name__ == '__main__':
    app.run()
