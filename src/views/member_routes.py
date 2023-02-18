from flask import Blueprint

member = Blueprint("member", __name__)


@member.route('/register')
def register():

    return "Registered Member"
