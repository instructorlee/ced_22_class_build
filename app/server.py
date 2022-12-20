from flask import Flask, render_template, redirect, url_for

from Team import Team

app = Flask(__name__)

user_data = {
    'first_name': 'Fred',
    'last_name': 'Flintstone'
}

@app.route('/') # root / home
def home():

    team = Team.members

    print ( team )
    
    return (redirect ('/team/member/234'))

    # return render_template('home.html', user=user_data, team=Team.members) 

@app.route('/team/member/<int:id>') # localhost:5000/team/member/110
def view_team_member(id):
    
    found_member = Team.get_member(id)

    if found_member == None:
        return render_template('error.html')

    else:
        return render_template('view_member.html', member = found_member)


if __name__=="__main__":   
    app.run(debug=True) 