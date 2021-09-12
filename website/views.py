from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/paste')
def paste():
    return render_template('paste.html')