from system.filesystem import Node


def build_physical_graph():
    root = Node("Office")

    n1 = Node("six-pack", parents=[root])
    n2 = Node("sticks-and-cups", parents=[root])
    n3 = Node("stonehenge", parents=[root])
    n4 = Node("graduation-day", parents=[root])
    n5 = Node("Looking-back", parents=[n1,n2,n3,n4])

    n1.set_password("74")
    n2.set_password("33")
    n3.set_password("52")
    n4.set_password("D")
    n5.set_password("WAsTeD", ignore_caps=False)

    n1.prompt = \
"""Whenever I feel parched, I always have a six-pack of my favorite refreshers.
They’re scattered throughout the room. Find them and solve the equation."""
    n2.prompt = \
"""Whenever I feel bored, I play with my popsicle sticks and cups. Look into the 
mug beside you and make use of its contents. Find the password, make it a number, 
and enter it into the OS."""
    n3.prompt = \
"""Whenever I feel nostalgic, I think about my trip to England years ago. I still 
wonder how they were able to make those stones stand up! Try and figure out the password!"""
    n4.prompt = \
"""Whenever I feel sentimental, I think back fondly on my years at Caltech and 
flip through my precious yearbook. Class of 2014 baby!!! I still remember when I 
first took those steps onto campus during a tour on 6/10. Weirdly enough, My 
first SURF also started on 6/10. Even more surprising, I also graduated on 6/10. 
This is why 6/10 means so much to me! Find the letter on the puzzle."""
    n5.prompt = \
"""Remember all the passwords for the previous 4 nodes. If it’s a number, look 
under the table and use the table. Combine and case-sensitive!"""

    return [root, n1, n2, n3, n4, n5], None
