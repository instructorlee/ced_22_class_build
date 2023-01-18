from flask import render_template, redirect, request, session
from app import app

from app.models.character import Character
from app.models.item import Item

user = {
        'first_name': 'Fred',
        'last_name': 'Flintstone'
    }

@app.route('/') # root / home
def home():
    return render_template('home/home.html') 

@app.route('/dashboard') 
def dashboard():

    if 'user_id' not in session:
        return redirect('/')

    return render_template('home/dashboard_alt.html', user = user, team = Character.get_all(), team_items=Item.get_all())
