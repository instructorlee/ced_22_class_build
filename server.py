from flask import Flask, render_template, redirect

from Team import Team

app = Flask(__name__)    

user = {
        'first_name': 'Fred',
        'last_name': 'Flintstone'
    }

@app.route('/') # root / home
def home():
    return render_template('home.html', user = user, team = Team.members) 

@app.route('/team/member/<int:id>')
def view_team_member(id): # how can we do this?

    found_member = Team.get_member(id)

    # Now we have two possible outcomes. What are they and how can we handle them?
    # Demo how someone can fake data in the URL. Don't trust the internet!!
    if found_member == None:
        return render_template('error.html')

    else:
        return render_template('view_member.html', member = found_member)

@app.route('/team/member/delete/<int:id>')
def delete_team_member(id):
    
    Team.delete_member(id)
    return redirect('/')


if __name__=="__main__":   
    app.run(debug=True) 