from app.config.mysqlconnection import connectToMySQL

from app.models.item import Item

class Character:

    NOT_ENOUGH_POWER_POINTS = 'not_enough_power_points'

    def __init__(self, data):

        self.id = data['id']
        self.type=data['type']
        self.name = data['name']
        self.power_points = data['power_points']
        self.can_teleport = data['can_teleport']
        self.user_id = data['user_id']

        self.items = []
   
    @classmethod
    def get_all(cls):
        
        query = """
            SELECT
                *
            FROM
                characters;
        """

        results = connectToMySQL('dec_22_cb').query_db(query)
        
        return [cls(character) for character in results] # list comprehension

        """
        characters = []

        for character in results:
            characters.append( cls(character) )

        return characters
        """

    @classmethod
    def destroy(cls, id):

        query  = """
            DELETE FROM 
                characters 
            WHERE 
                id = %(id)s;
        """
        
        return connectToMySQL('dec_22_cb').query_db(query, {'id': id})

    @classmethod
    def save(cls, data):

        query = """
            INSERT INTO 
                characters 
                (type, name, can_teleport, power_points) 
            VALUES 
                (%(type)s, %(name)s, %(can_teleport)s, %(power_points)s);
        """

        result = connectToMySQL('dec_22_cb').query_db(query, data)

        return result

    @classmethod
    def get_one(cls, id):

        query  = """
            SELECT 
                * 
            FROM 
                dec_22_cb.characters

            LEFT JOIN items ON items.character_id = characters.id

            WHERE
                characters.id = %(id)s;
        """

        results = connectToMySQL('dec_22_cb').query_db(query, {'id': id})

        if not results:
            return None

        character = Character(results[0])

        for row in results:
            if row['items.id']: # skip when character has no items
                character.items.append(Item({
                    'id': row['items.id'],
                    'name': row['items.name'],
                    'image_slug': row['image_slug'],
                    'is_magical': row['is_magical'],
                    'attack': row['attack'],
                    'defense': row['defense'],
                    'character_id': row['character_id']
                }))

        return character

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

        return connectToMySQL('dec_22_cb').query_db(query, data)

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
