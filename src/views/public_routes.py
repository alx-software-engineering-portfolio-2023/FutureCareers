from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from src.forms.webforms import SearchForm
from src.web_scraper.scraper import Search_careerjunction

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
    
    results = Search_careerjunction(request.form.get("search"))
        
    return render_template("public/search.html", user=current_user, form=form, results=results)

    # else:
    #     return render_template("public/search.html", user=current_user, form=form)
