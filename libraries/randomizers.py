import random
from libraries.files import *
from libraries.tables import *
enemies = enemies() #Grab the enemy table from (root folder)/libraries/tables.py
def check(file, offset, index, identifier):
    with open(file, "rb") as xbe:
        xbe.seek(offset)
        if xbe.read(4)[index] == identifier:
            return True
        else:
            return False

def checkRange(file, offset, index, identifiers):
    with open(file, "rb") as xbe:
        xbe.seek(offset)
        if xbe.read(4)[index] in identifiers:
            return True
        else:
            return False

def fixOffset(offset, offsetFixer): #Converts RAM offsets to XBE offsets
    return offset-offsetFixer

def replaceMonsters(file, offset, count): #This is where time monster randomization happens
    with open(file, "r+b") as xbe:
        xbe.seek(offset)
        for i in range(count):
            written = False
                
            if check(file, xbe.tell(), 0, 2) == True: #Octoballoons sometimes spawn in the air. Randomize the type instead so the game is still beatable.
                xbe.write(random.choice([b'\x02\x01\x00\x00', b'\x02\x02\x00\x00']))
                written = True

            if check(file, xbe.tell(), 0, 0xD) == True: #Tom Toms should stay as Tom Toms to avoid confusion
                xbe.seek(2, 1)
                xbe.write(pack.byte(random.randint(1, 3)))
                xbe.seek(1, 1)
                written = True

            if check(file, xbe.tell(), 0, 0xB) == True or check(file, xbe.tell(), 0, 0xC) == True: #Spirit enemies break when randomized - just randomize the type instead
                xbe.write(random.choice([b'\x0B\x03\x00\x00', b'\x0B\x04\x00\x00', b'\x0C\x03\x00\x00', b'\x0C\x04\x00\x00']))
                written = True

            if written == False: #Now do the full enemy randomization
                xbe.write(random.choice(enemies))
            
            xbe.seek(32, 1)

def replaceItems(file, offset, count): #This is where item randomization happens
    with open(file, "r+b") as xbe:
        xbe.seek(offset)
        for i in range(count):
            if checkRange(file, xbe.tell(), 0, range(0x71, 0x80)) == False:
                xbe.write(pack.uint(random.randint(0x59, 0x70)))
            else:
                xbe.seek(4, 1)
            
            xbe.seek(36, 1)

def replaceRollingObjectSpawners(file, offset, count): #Needs to be renamed - making multiple functions for 1 table would be very inefficient
    with open(file, "r+b") as xbe:
        xbe.seek(offset)
        for i in range(count):
            #print(hex(xbe.tell()))
            #input()
            if check(file, xbe.tell(), 0, 4) == True: #Barrel spawners
                #Set them to either bombs or barrels
                xbe.write(random.choice([b'\x04\x00\x00\x00',b'\x0F\x00\x00\x00']))
                xbe.seek(32, 1)
                #For barrels, set the explosive barrel spawn chance
                xbe.write(random.choice([b'\x00\xFF\x00\x00\x00\x00\x00\x00', b'\x24\xFF\x00\x00\x00\x00\x00\x00', b'\x7F\xFF\x00\x00\x00\x00\x00\x00']))
            elif check(file, xbe.tell(), 0, 0xF) == True: #Bomb spawners
                #Set them to either bombs or barrels
                xbe.write(random.choice([b'\x04\x00\x00\x00',b'\x0F\x00\x00\x00']))
                xbe.seek(32, 1)
                #For barrels, set the explosive barrel spawn chance
                xbe.write(random.choice([b'\x00\xFF\x00\x00\x00\x00\x00\x00', b'\x24\xFF\x00\x00\x00\x00\x00\x00', b'\x7F\xFF\x00\x00\x00\x00\x00\x00']))
            elif check(file, xbe.tell(), 0, 0) == True and checkRange(file, xbe.tell(), 1, range(0, 1)) == True: #Buttons
                xbe.write(random.choice([b'\x00\x00\x00\x00',b'\x00\x01\x00\x00']))
                xbe.seek(40, 1)
            elif check(file, xbe.tell(), 0, 1) == True and checkRange(file, xbe.tell(), 1, range(0, 1)) == True: #Doors
                xbe.write(random.choice([b'\x01\x00\x00\x00',b'\x01\x01\x00\x00',b'\x01\x02\x00\x00',b'\x01\x03\x00\x00',b'\x01\x04\x00\x00',b'\x01\x06\x00\x00']))
                xbe.seek(40, 1)
            elif check(file, xbe.tell(), 0, 7) == True and checkRange(file, xbe.tell(), 1, range(0, 1)) == True: #Spike doors
                xbe.write(random.choice([b'\x07\x00\x00\x00',b'\x07\x01\x00\x00']))
                xbe.seek(40, 1) 
            else:
                xbe.seek(44, 1)
            
