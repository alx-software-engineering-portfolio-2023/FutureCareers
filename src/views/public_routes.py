from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from forms.webforms import SearchForm
from web_scraper.scraper import Search_careerjunction

public = Blueprint("public", __name__)


@public.route('/')
def home():

    return render_template('public/home.html', user=current_user)

@public.route('/search', methods=['GET', 'POST'])
def search():
    #form = SearchForm()
    
    #if form.validate_on_submit():
    results = Search_careerjunction('python')
    
    return render_template("search.html", results=results, user=current_user)  # , form=form
