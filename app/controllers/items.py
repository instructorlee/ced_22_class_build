from flask import render_template, redirect, request
from app import app

from app.models.item import Item
from app.models.character import Character

@app.route('/item/add')
def get_add_item_form():
    return render_template('item/add.html', characters = Character.get_all())

@app.route('/item/add', methods=['POST'])
def add_inventory_item():
    
    Item.save(request.form)

    return( redirect('/dashboard') ) 

@app.route('/item/update/<int:id>')
def get_update_item_form(id):
    return render_template('item/update.html', item = Item.get_one(id))

@app.route('/item/update', methods=['POST'])
def update_inventory_item():

    Item.update(request.form)
    return( redirect('/dashboard') ) 

@app.route('/item/delete/<int:id>')
def delete_inventory_item(id):
    
    Item.destroy(id)
    return redirect('/dashboard')