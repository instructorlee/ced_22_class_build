from flask import render_template, redirect, request
from app import app

from app.models.character import Character

user_data = {
    'first_name': 'Fred',
    'last_name': 'Flintstone'
}

@app.route('/') # root / home
def home():
    return render_template('home/home.html') 

@app.route('/dashboard') 
def dashboard():
    return render_template('home/dashboard.html', user = user_data, team = Character.get_all()) # list of team members
