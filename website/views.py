from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Paste
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/paste', methods=['GET', 'POST'])
@login_required
def paste():
    errors = {}
    isError = False
    title = ''
    code = ''
    if request.method == 'POST':
        title = request.form.get('title').strip()
        code = request.form.get('code').strip()
        
        if len(title) < 1:
            errors['title'] = "Title must be required."
            isError = True
        if len(code) < 1:
            errors['code'] = "Code must be required."
            isError = True

        if isError == False:
            new_paste = Paste(title=title, code=code, user_id=current_user.id)
            db.session.add(new_paste)
            db.session.commit()
            flash("Pasted code successfully!", category='success')
            return redirect(url_for('views.pastes'))

    return render_template('paste.html', title=title, code=code, errors=errors, user=current_user)

@views.route('/pastes')
@login_required
def pastes():
    return render_template('pastes.html', user=current_user)

@views.route('/<int:id>')
@login_required
def paste_detail(id):
    paste = Paste.query.get(id)
    return render_template('paste_detail.html', user=current_user, paste=paste)

@views.route('/delete/<int:id>')
@login_required
def delete(id):
    paste = Paste.query.get(id)
    if paste and paste.user_id == current_user.id:
        db.session.delete(paste)
        db.session.commit()
        flash('Paste deleted!', category='success')

    return redirect(url_for('views.pastes'))