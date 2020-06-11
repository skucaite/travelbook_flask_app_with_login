from flask import render_template, request, abort, Blueprint
from travelbook.models import Guide



main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
@main.route('/travels')
def home():
    try:
        page = request.args.get('page', 1, type=int)
        travels=Travel.query.order_by(Travel.id.desc()).paginate(page=page, per_page=3)
    except Exception:
        abort(404)
    return render_template('home.html', travels=travels)


@main.route('/about')
def about():
    return render_template('about.html', title='About')
