from flask import Flask, request, render_template, redirect
import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', # change the user and password as needed
                                    password = 'rootroot', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # if the query is an insert, return the id of the last row, since that is the row we just added
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # if the query is a select, return everything that is fetched from the database
                    # the result will be a list of dictionaries
                    result = cursor.fetchall()
                    return result
                else:
                    # if the query is not an insert or a select, such as an update or delete, commit the changes
                    # return nothing
                    self.connection.commit()
            except Exception as e:
                # in case the query fails
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# this connectToMySQL function creates an instance of MySQLConnection, which will be used by server.py
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)

class Character:

    def __init__(self, data):

        self.id = data['id']
        self.type = data['type']
        self.name = data['name']
        self.can_teleport = data['can_teleport']
        self.power_points = data['power_points']

    @classmethod
    def get_all(cls):

        query = """
            SELECT
                *
            FROM
                characters;
        """

        results = connectToMySQL('dec_22_cb').query_db(query) # show in debugger

        characters = []

        for character in results:
            characters.append(cls(character))

        return characters

        # return [cls(character) for character in results] # list comprehension

    @classmethod
    def save(cls, data):

        query = """
            INSERT INTO 
                characters 
                (type, name, can_teleport, power_points) 
            VALUES 
                (%(type)s, %(name)s, %(can_teleport)s, %(power_points)s);
        """

        result = connectToMySQL('dec_22_cb').query_db(query,data)

        return result

    @classmethod
    def get_one(cls, id):

        query  = """
            SELECT 
                * 
            FROM 
                characters 
            WHERE 
                id = %(id)s;
        """

        result = connectToMySQL('dec_22_cb').query_db(query, {'id': id})

        return cls(result[1]) if result else None

    @classmethod
    def update(cls, data):

        query = """
            UPDATE 
                characters 
            SET 
                type=%(type)s,
                name=%(name)s,
                can_teleport=%(can_teleport)s,
                power_points=%(power_points)s
            WHERE 
                id = %(id)s;
        """

        return connectToMySQL('dec_22_cb').query_db(query,data)

    @classmethod
    def destroy(cls, id):

        query  = """
            DELETE FROM 
                characters 
            WHERE 
                id = %(id)s;
        """
        
        return connectToMySQL('dec_22_cb').query_db(query, {'id': id})

    def run(self, direction, map):

        map.set_character_position(self, True)

        if direction == 'north':
            self.position.y -=1

        elif direction == 'east':
            self.position.x += 1

        elif direction == 'south':
            self.position.y += 1

        elif direction == 'west':
            self.position.x -= 1

        if self.power_points >= 2:
            print( f'{self.name} is running {direction}.')
            self.power_points -= 2

            map.set_character_position(self)

            return True

        else:
            print( f'{self.name} only has {self.power_points} Power Points and cannot run.')
            return self.NOT_ENOUGH_POWER_POINTS

    def rest(self):

        if self.power_points < 10:
            print( f'{self.name} is resting.')
            self.power_points += 1
            return True

        else:
            print( f'{self.name} has {self.power_points} Power Points and does not need to rest.')
            return False

    def teleport(self, map):

        if self.power_points >= 4 and self.can_teleport:
            print( f'{self.name} is teleporting.')
            self.power_points -= 4
            return True

        elif self.power_points < 4:
            print( f'{self.name} only has {self.power_points} Power Points and cannot teleport.')
            return self.NOT_ENOUGH_POWER_POINTS

        else:
            print( f'{self.name} is not able to teleport.')
            return False

    def list_inventory(self):

        for item in self.inventory:
                print ( item )

app = Flask(__name__)    

user = {
        'first_name': 'Fred',
        'last_name': 'Flintstone'
    }

@app.route('/') # root / home
def home():
    return render_template('home.html') 

@app.route('/dashboard') 
def dashboard():
    return render_template('dashboard.html', user = user, team = Character.get_all())

@app.route('/team/member/<int:id>')
def view_team_member(id): # how can we do this?

    found_member = Character.get_one(id)

    # Now we have two possible outcomes. What are they and how can we handle them?
    # Demo how someone can fake data in the URL. Don't trust the internet!!
    if found_member == None:
        return render_template('error.html')

    else:
        return render_template('view_member.html', member = found_member)

@app.route('/team/member/delete/<int:id>')
def delete_team_member(id):
    
    Character.destroy(id)
    return redirect('/dashboard')

@app.route('/team/member/add')
def get_add_team_member_form():
    return render_template('add_member.html')

@app.route('/team/member/add', methods=['POST'])
def add_team_member():
    
    # how can the lines below be refactored?
    new_team_member = {
        'name': request.form['name'],
        'type': request.form['type'],
        'can_teleport': request.form['can_teleport'],
        'power_points': request.form['power_points']
    }

    Character.save(new_team_member)

    #Team.add_member(new_team_member)

    return( redirect('/dashboard') ) # redirect to the rounte, not the route function name.

@app.route('/team/member/update/<int:id>')
def get_update_team_member_form(id):
    return render_template('update_member.html', member=Character.get_one(id))

@app.route('/team/member/update', methods=['POST'])
def update_team_member():

    member_to_update = Character.get_one(request.form['id'])

    if member_to_update:
        Character.update({
            'id': member_to_update.id,
            'name': request.form['name'],
            'type': request.form['type'],
            'can_teleport': request.form['can_teleport'],
            'power_points': request.form['power_points']
        })

    """
        member_to_update = Team.get_member(int(request.form['id']))
        
        if member_to_update:
            member_to_update['name'] = request.form['name']
            member_to_update['type'] = request.form['type']
            member_to_update['can_teleport'] = int(request.form['can_teleport'])

            Team.save_member(member_to_update)
    """

    return( redirect('/dashboard') ) # redirect to the route, not the route function name.
    
if __name__=="__main__":   
    app.run(debug=True) 