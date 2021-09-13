from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import desc

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/paste')
@login_required
def paste():
    return render_template('paste.html', user=current_user)

@views.route('/pastes')
@login_required
def pastes():
    return render_template('pastes.html', user=current_user)