from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.models import User
from forms.webforms import RegistrationForm

admin = Blueprint("admin", __name__)


@admin.route('/dashboard')
@login_required
def dashboard():
    
        
    return render_template('admin/dashboard.html', user=current_user)


@admin.route('/profile/<int:id>')
@login_required
def profile(id):
    form = RegistrationForm()
    # user_id == current_user.id
    admin_to_update = User.query.get_or_404(id)
    
    if admin_to_update.id == 1:
        if request.method == "POST":
            return render_template('admin/profile.html', form=form, user=admin_to_update, id=id)

    else:
        flash("Access Denied...!!")
        return redirect(url_for('auth.logout'))
    
    return render_template('admin/profile.html', form=form, user=admin_to_update, id=id)

@admin.route('/stats')
@login_required
def statistics():
    
    return render_template("admin/statistics.html", user=current_user)