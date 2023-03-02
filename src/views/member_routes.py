from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, make_response
from flask_login import login_required, current_user
from src.forms.webforms import RegistrationForm, SearchForm
from src.models.models import db, User, Saved
from datetime import datetime

member = Blueprint("member", __name__)


@member.route('/dashboard')
@login_required
def dashboard():
    form = SearchForm()
    
    return render_template("member/dashboard.html", user=current_user, form=form)


@member.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    form = RegistrationForm()
    user_to_update = User.query.get_or_404(id)

    if id == current_user.id:
        if request.method == 'POST':
            user_to_update.name = request.form['name']
            user_to_update.surname = request.form['surname']
            user_to_update.email = request.form['email']

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
    form = SearchForm()
    saved_jobs = Saved.query.order_by(Saved.id)
    
    return render_template("member/saved.html", user=current_user, form=form, saved_jobs=saved_jobs)


@member.route('/deadlines')
@login_required
def deadlines():
    form = SearchForm()
    saved_jobs = Saved.query.order_by(Saved.closing_date)
    
    return render_template("member/deadlines.html", user=current_user, form=form, saved_jobs=saved_jobs)


@member.route("/save", methods=["POST"])
@login_required
def save():
    req = request.get_json()
    
    title = req["title"]
    description = req["description"]
    link = req["link"]
    closing_date = req["closing_date"] + " 00:00:00"
    closing_date = datetime.strptime(closing_date, '%Y-%m-%d %H:%M:%S')

    job = Saved(job_title=title, description=description, link=link, applied_to=False, closing_date=closing_date, user_id=current_user.id)
    db.session.add(job)
    db.session.commit()

    res = make_response(jsonify({"success": "fa-solid fa-bookmark"}), 200)

    return res


@member.route('/saved/')
@login_required
def delete_saved():
    form = SearchForm()
    delete_saved_job = Saved.query.order_by(Saved.id).first()
    
    if current_user.id == delete_saved_job.user_id:
    
        # if delete_saved_job:
        try:
            db.session.delete(delete_saved_job)
            db.session.commit()
            flash("Deleted successfully!")
                
            saved_jobs = Saved.query.order_by(Saved.closing_date)
            return render_template('member/saved.html', user=current_user, form=form, id=id, saved_jobs=saved_jobs)
        except:
            flash("An Error Occurred...failed to delete selection.")
            saved_jobs = Saved.query.order_by(Saved.closing_date)
            return render_template('member/saved.html', user=current_user, form=form, id=id, saved_jobs=saved_jobs)
        # else:
        #     flash("Could not perform operation, No record was found.")
        #     saved_jobs = Saved.query.order_by(Saved.closing_date)
        #     return render_template('member/saved.html', user=current_user, form=form, id=id, saved_jobs=saved_jobs)
    
    else:
        flash("Unauthorized Access!!!!")
        return redirect(url_for('auth.logout'))
