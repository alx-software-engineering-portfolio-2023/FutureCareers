from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from forms.webforms import RegistrationForm
from models.models import db, User


member = Blueprint("member", __name__)


@member.route('/dashboard')
@login_required
def dashboard():

    return render_template("member/dashboard.html", user=current_user)


@member.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    form = RegistrationForm()
    user_to_update = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user_to_update.name = request.form['name']
        user_to_update.surname = request.form['surname']
        user_to_update.email= request.form['email']
        user_to_update.password1 = ''
        user_to_update.password2 = ''
        
        try:
            db.session.commit()
            flash("User Updated Succesfully")
            
            return render_template('member/profile.html', form=form, user=user_to_update, id=id)
        
        except:
            flash("Encountered an Error!...Try Again!")
            
            return render_template('member/profile.html', form=form, user=user_to_update, id=id)
    
    else:
        
        return render_template("member/profile.html", form=form, user=user_to_update, id=id)


@member.route('/delete')
@login_required
def delete(id):

    return redirect(url_for('member.dashboard'))


@member.route('/saved')
@login_required
def saved():

    return render_template("member/saved.html", user=current_user)


@member.route('/deadlines')
@login_required
def deadlines():

    return render_template("member/deadlines.html", user=current_user)
