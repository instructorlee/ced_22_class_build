from flask import render_template, redirect, request, session
from app import app

from app.models.character import Character
from app.models.Team import Team


@app.route('/team/member/<int:id>') # localhost:5000/team/member/110
def view_team_member(id):
    
    found_member = Team.get_member(id)

    if found_member == None: # data validation
        return render_template('error.html')

    else:
        return render_template('character/view.html', member = found_member)

@app.route('/team/member/delete/<int:id>')
def delete_team_member(id):
    
    Character.destroy(id)
    return redirect('/dashboard')

@app.route('/team/member/add')
def get_add_member_form():
    return render_template('character/add.html')

@app.route('/team/member/add', methods=['POST'])
def add_member():
    
    new_team_member = {
        'name': request.form['name'],
        'type': request.form['type'],
        'can_teleport': request.form['can_teleport'],
        'power_points': request.form['power_points']
    }

    Character.save(new_team_member)
    
    return( redirect('/dashboard') )

@app.route('/team/member/update/<int:id>')
def get_update_member_form(id):

    if 'user_id' not in session:
        return redirect('/')

    character = Character.get_one(id)

    if character and character.user_id == int(session['user_id']):
        return render_template('character/update.html', member=Character.get_one(id))
    
    return  redirect('/dashboard')

@app.route('/team/member/update', methods=['POST'])
def update_member():

    member_to_update = Character.get_one(int(request.form['id']))
    
    if member_to_update:
        Character.update({
            'id': member_to_update.id,
            'name': request.form['name'],
            'type': request.form['type'],
            'can_teleport': request.form['can_teleport'],
            'power_points': request.form['power_points']
        })

    return( redirect('/dashboard') )