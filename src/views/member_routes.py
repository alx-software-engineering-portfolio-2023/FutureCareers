from flask import Blueprint, render_template
from flask_login import login_required, current_user

member = Blueprint("member", __name__)


@member.route('/dashboard')
@login_required
def dashboard():

    return render_template("member/dashboard.html")
