from flask import render_template, redirect, request, flash
from app import app
from flask_bcrypt import Bcrypt

from app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/user/register', methods=['POST'])
def register():
    pass

@app.route('/user/login', methods=['POST'])
def login():
    pass