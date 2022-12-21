from flask import Flask, render_template, request, redirect

from Team import Team

app = Flask(__name__)

user_data = {
    'first_name': 'Fred',
    'last_name': 'Flintstone'
}

@app.route('/') # root / home
def home():
    return render_template('home.html', user=user_data, team=Team.members) 

@app.route('/team/member/<int:id>') # localhost:5000/team/member/110
def view_team_member(id):
    
    found_member = Team.get_member(id)

    if found_member == None: # data validation
        return render_template('error.html')

    else:
        return render_template('view_member.html', member = found_member)

@app.route('/team/member/add')
def get_add_member_form():
    return render_template('add_member.html')

@app.route('/team/member/add', methods=['POST'])
def add_member():
    
    new_team_member = {
        'name': request.form['name'],
        'type': request.form['type'],
        'can_teleport': request.form['can_teleport'],
        'inventory': [] # how can inventory be added since it is not passed in?
    }

    Team.add_member(new_team_member)
    
    return( redirect('/') )

@app.route('/team/member/update/<int:id>')
def get_update_member_form(id):
    return render_template('update_member.html', member = Team.get_member(id))

@app.route('/team/member/update', methods=['POST'])
def update_member():

    member_to_update = Team.get_member(int(request.form['id']))
    
    if member_to_update:
        member_to_update['name'] = request.form['name']
        member_to_update['type'] = request.form['type']
        member_to_update['can_teleport'] = int(request.form['can_teleport'])

        Team.save_member(member_to_update)

    return( redirect('/') )


if __name__=="__main__":   
    app.run(debug=True) 