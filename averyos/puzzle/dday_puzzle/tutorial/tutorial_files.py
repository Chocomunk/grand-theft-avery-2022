from system.filesystem import File


# TODO: Consider "help" program
START_MSG = \
"""
 ---------------------------------------- Welcome to AveryOS! ----------------------------------------

AveryOS is an Institution-designed internal operating system. To support our goal of deceiving the general populace,
AveryOS operates on a graph-based filesystem where nodes may or may not be connected and may or may not have loops... :).

To get started, type `pepelaugh`. Folder icons indicate directories/nodes, file icons indicate... files..., and gear 
icons indicate programs. All programs you encounter will stay with you over the entire filesystem.
"""


security = File("security_update.txt", 
"""
Note to self: I’ve changed all my command names to stump weebs and Institution invaders alike.\n\
        Nobody will catch on. -DO-n't even try, nothing is getting through
"""
)

doc_notes = File("notes.txt", 
"""This new security system should be enough to fend off attacks.
My institution journal will be safe from prying eyes..."""
)

avery_desc1 = File("avery-house.txt", "Avery House: The House closest to the north pole.")
avery_desc2 = File("avery-desc.txt",
    "Avery House has no murals because R. Stanton Avery proclaimed that the walls should be ‘as white as Avery Paper.")

readme1 = File("README1.md","What the hell?")
readme2 = File("README2.md","Why the fuck?")
readme3 = File("README3.md","What's the point?")
readme4 = File("README4.md","If you keep reading these, you’re never going to get anywhere.")
readme5 = File("README5.md","Why on God’s green Earth are you still reading?")
readme6 = File("README6.md","Nobody hired by the Institution could possibly be dumb enough to still be reading.")

caught_file = File("goodfilename.txt",
"""
Hello there! Looks like you poked your nose a little too deep and stumbled into my trap :). Imagine being as dumb as this
guy. shesh
"""
)

gameover = File("gameover.txt",
"""
Looks like internet hackers are getting better and better nowadays. Nice job getting this far, intruder, but thats as 
far as you go. Unfortunately for you, you can only find the way out in my office!
"""
)

gameon = File("game-is-on.txt",
"""Looks like an institution spy broke into my office... Now the real game is on! 
You want my intel? Then come and get it. I've secured everything I have, good luck getting through!
"""
)