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
    
    if id == current_user.id:
        if request.method == 'POST':
            user_to_update.name = request.form['name']
            user_to_update.surname = request.form['surname']
            user_to_update.email= request.form['email']
            
            try:
                db.session.commit()
                flash("User Updated Succesfully")
                
                return render_template('member/dashboard.html', form=form, user=user_to_update, id=id)
            
            except:
                flash("Encountered an Error!...Try Again!")
                
                return render_template('member/profile.html', form=form, user=user_to_update, id=id)
        
        else:
            
            return render_template("member/profile.html", form=form, user=user_to_update, id=id)
    else:
        flash("Not your profile...")
        return redirect(url_for('member.dashboard'))
        

@member.route('/delete/<int:id>')
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
            return render_template('member/profile.html', form=form)
        
    else:
        flash("Requires authorization!! You are not an Admin..")
        return redirect(url_for('dashboard'))


@member.route('/saved')
@login_required
def saved():

    return render_template("member/saved.html", user=current_user)


@member.route('/deadlines')
@login_required
def deadlines():

    return render_template("member/deadlines.html", user=current_user)

