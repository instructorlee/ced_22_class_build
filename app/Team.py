class Team:

    members = [
        {
            'id': 1,
            'type': 'FuzzBall',
            'name': 'Fred',
            'power_points': 5,
            'can_teleport': True
        },
        {
            'id': 2,
            'type': 'FurOFury',
            'name': 'Fiora',
            'power_points': 8,
            'can_teleport': False
        },
        {
            'id': 3,
            'type': 'BeatleBop',
            'name': 'Bob',
            'power_points': 3,
            'can_teleport': True
        }
    ]

    @classmethod
    def add_member(cls, member_data):
        member_data['id'] = len(cls.members) + 1 # create an ID
        cls.members.append(member_data)

    @classmethod
    def save_member(cls, member_data):
        cls.members = [member_data if data['id'] == member_data['id'] else data for data in cls.members] # list comprehension

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



In class yesterday, someone asked about adding styling to specific elements like this:

`
<div style="width: 200px; height: 200px; background-color: red;">Some Red Text</a>
`

You were probably told to never do this. It is important to know that, in CSS, there are really, mostly, only guidelines and good practices.

It is good practice to NOT do this because it makes it difficult to style a page when the CSS is in different places.

However, when working with dynamic data, and, later, React, it is totally acceptable to do something 'surgical' when you need that type of control.ConnectionRefusedError

For example, using a dynamic color, we can do this:

`
<div class='box' style="background-color: {{ color }};">Some Red Text</a>
`

This allows us to put the basic properties of our element in a CSS file. Then just change the background color as needed.