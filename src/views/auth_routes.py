from flask import Blueprint, request, render_template, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


from forms.webforms import RegistrationForm, LoginForm
from __init__ import db
from models.models import User


auth = Blueprint("auth", __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the User."""
     
    form = RegistrationForm()

    # Validate Form
    if form.validate_on_submit():
        user =  User.query.filter_by(email=form.email.data).first()
        
        if user is None:
            # Hash the password
            hashed_password = generate_password_hash(
                form.password1.data, "sha256")

            new_user = User(name=form.name.data, surname=form.surname.data,
                        email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
           
            flash("Account Created Successfully!")
            return redirect(url_for('auth.login'))
        
        else:
            flash("Username already exists!! Choose another Username")
            
        form.name.data = ''
        form.surname.data = ''
        form.email.data = ''
        form.password1.data = ''

    return render_template('auth/register.html', form=form, user=current_user)
    

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Logs In the User."""
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            # Check the password hash if it matches the typed password
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                
                if user.id == 1:
                    flash("Hello Admin")
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash("Signed In Successfully")
                    return redirect(url_for('member.dashboard'))
            else:
                flash("Incorrect password! - Try Again")
        else:
            flash("Incorrect Username. Try Again")

    return render_template('auth/login.html', form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """Logs out the user."""
    
    logout_user()
    flash("You have been Logged out")
    return redirect(url_for('auth.login'))

