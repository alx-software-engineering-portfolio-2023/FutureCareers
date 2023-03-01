from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from forms.webforms import SearchForm
from web_scraper.scraper import Search_careerjunction

public = Blueprint("public", __name__)


@public.route('/')
def home():

    return render_template('public/home.html', user=current_user)


@public.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@public.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    
    # if form.validate_on_submit():
    results = Search_careerjunction("java")
        # print(form.search.data)
        
    return render_template("public/search.html", user=current_user, form=form, results=results)

    # else:
    #     return render_template("public/search.html", user=current_user, form=form)
