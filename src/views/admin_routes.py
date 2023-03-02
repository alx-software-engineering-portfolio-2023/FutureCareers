from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from src.__init__ import db
from src.models.models import User
from src.forms.webforms import RegistrationForm, SearchForm

admin = Blueprint("admin", __name__)


@admin.route('/dashboard')
@login_required
def dashboard():
    form = SearchForm()
    our_users = User.query.all()

    return render_template('admin/dashboard.html', user=current_user, our_users=our_users, form=form)


@admin.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    form = RegistrationForm()
    user_to_update = User.query.get_or_404(id)

    if request.method == 'POST':
        user_to_update.name = request.form['name']
        user_to_update.surname = request.form['surname']
        user_to_update.email = request.form['email']

        try:
            db.session.commit()
            flash("User Updated Succesfully")

            return render_template('admin/dashboard.html', form=form, user=user_to_update, id=id)

        except:
            flash("Encountered an Error!...Try Again!")

            return render_template('admin/profile.html', form=form, user=user_to_update, id=id)

    else:

        return render_template("admin/profile.html", form=form, user=user_to_update, id=id)


@admin.route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id:
        delete_user = User.query.get_or_404(id)
        form = RegistrationForm

        try:
            db.session.delete(delete_user)
            db.session.commit()

            flash("User Deleted Succesfully!")
            return redirect(url_for('auth.login'))

        except:
            flash("Whoops! Encountered a problem deleting the user")
            return render_template('admin/profile.html', form=form)

    else:
        flash("Requires authorization!! You are not the Admin of This Profile..")
        return redirect(url_for('admin.dashboard'))


# @admin.route('/stats')
# @login_required
# def statistics():
#     form = SearchForm()
    
#     return render_template("admin/statistics.html", user=current_user, form=form)
