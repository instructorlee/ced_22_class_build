class Team:

    members = [
        {
            'id': 1,
            'type': 'FuzzBall',
            'name': 'Fred',
            'inventory': ['food', 'fireball', 'shield'],
            'can_teleport': True
        },
        {
            'id': 2,
            'type': 'FurOFury',
            'name': 'Fiora',
            'inventory': [],
            'can_teleport': False
        },
        {
            'id': 3,
            'type': 'BeatleBop',
            'name': 'Bob',
            'inventory': ['food', 'sword', 'silly stones'],
            'can_teleport': True
        }
    ]

    @classmethod
    def add_member(cls, member_data):
        member_data['id'] = len(cls.members) + 1 # create an ID
        cls.members.append(member_data)

    @classmethod
    def get_member(cls, id):
        
        found_member = None
        for member in cls.members:
            if member['id'] == id:
                found_member = member

        return found_member

    @classmethod
    def delete_member(cls, id):
        
        start_length = len(cls.members)
        cls.members = [member for member in cls.members if member['id'] != id]

        return start_length != len(cls.members) # do not do this the first time through. Save it for extra functionality