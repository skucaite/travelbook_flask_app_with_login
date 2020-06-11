from flask import render_template, url_for, flash, request, redirect, abort, Blueprint
from flask_login import login_user, current_user, login_required
from travelbook import db
from travelbook.models import Travel
from travelbook.forms import TravelForm


travels = Blueprint('travels', __name__)


# Show Travel
# ----------------------------------------------------------------#
@travels.route('/travels/<travel_id>')
def show_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    title = 'Trip: ' + travel.title
    return render_template('show_travel.html', travel=travel, title=title)

# Create Travel
# ----------------------------------------------------------------#
@travels.route('/travels/create', methods=['GET', 'POST'])
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
@travels.route('/travels/<travel_id>/edit', methods=['GET', 'POST'])
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
@travels.route('/travels/<travel_id>/delete', methods=['POST', 'DELETE'])
def delete_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    try:
        travel.delete()
        flash('Deleted!', 'success')
    except:
        flash('There was a problem deleting that guide', 'danger')
    return redirect('/travels')
