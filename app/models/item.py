from app.config.mysqlconnection import connectToMySQL

class Item:

    def __init__(self, data):

        self.id = data['id']
        self.name = data['name']
        self.image_slug = data['image_slug']
        self.is_magical = data['is_magical']
        self.attack = data['attack']
        self.defense = data['defense']
        self.character_id = data['character_id']
   
    @classmethod
    def get_all(cls):
        
        query = """
            SELECT
                *
            FROM
                items;
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
                items 
            WHERE 
                id = %(id)s;
        """
        
        return connectToMySQL('dec_22_cb').query_db(query, {'id': id})

    @classmethod
    def save(cls, data):

        query = """
            INSERT INTO 
                items 
                (name, image_slug, is_magical, attack, defense, character_id) 
            VALUES 
                (%(name)s, %(image_slug)s, %(is_magical)s, %(attack)s, %(defense)s, %(character_id)s);
        """

        result = connectToMySQL('dec_22_cb').query_db(query, data)

        return result

    @classmethod
    def get_one(cls, id):

        query  = """
            SELECT 
                * 
            FROM 
                items 
            WHERE 
                id = %(id)s;
        """

        result = connectToMySQL('dec_22_cb').query_db(query, {'id': id})

        return cls(result[0]) if result else None

    @classmethod
    def update(cls, data):

        query = """
            UPDATE 
                items 
            SET 
                character_id=%(character_id)s,
                image_slug=%(image_slug)s,
                is_magical=%(is_magical)s,
                attack=%(attack)s,
                defense=%(defense)s,
                name=%(name)s
            WHERE 
                id = %(id)s;
        """

        return connectToMySQL('dec_22_cb').query_db(query, data)
