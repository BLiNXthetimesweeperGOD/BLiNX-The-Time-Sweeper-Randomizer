import random
from libraries.files import *
from libraries.configLoader import *
def checkForByteString(path, string):
    with open(path, 'rb') as file:
        content = file.read()
        offset = content.find(string)
        return string in content, offset

def randomizeShopVisualsAndPrices(xbe, active):
    if active == "T":
        badRanges = []
        badRanges.extend(range(0x04, 0x14))
        badRanges.extend(range(0x1F, 0x28))
        badRanges.extend(range(0x2E, 0x3C))
        entries = []
        status, offset = checkForByteString(xbe, b'\xd8\x0fI?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x04\x00\x00\x00\x0f\x00\x00\x00\x15\x00\x00\x00\xc8\x00\x00\x00')
        offset+=0x20
        with open(xbe, "r+b") as patch:
            patch.seek(offset)
            for entry in range(0x46):
                if entry not in badRanges:
                    entries.append(patch.read(12))
                else:
                    patch.seek(12, 1)
            patch.seek(offset)
            random.shuffle(entries)
            index = 0
            for entry in range(0x46):
                if index not in badRanges:
                    patch.write(entries.pop(0))
                else:
                    patch.seek(12, 1)
                    #print(hex(patch.tell()))
                index+=1
    else:
        print("Shop item visual/price randomization is disabled in the config file. Skipping...")

def randomizeTimeControlColors(xbe, active):
    if active == "T":
        with open(xbe, "r+b") as patch:
            status, offset = checkForByteString(xbe, b'\xFF\x60\xE0\x00\x60\xC0\xFF\x00')
            patch.seek(offset)
            for timeControlColor in range(5):
                R = pack.ubyte(random.randint(0, 255))
                G = pack.ubyte(random.randint(0, 255))
                B = pack.ubyte(random.randint(0, 255))
                A = b'\x00'
                patch.write(B+G+R+A) #Merge all byte strings into one and write them
    else:
        print("Time control color randomization is disabled in the config file. Skipping...")

def customizeBoxColors(xbe, active):
    if active == "T":
        with open(xbe, "r+b") as patch:
            status, offset = checkForByteString(xbe, b'\x80\x80\xff\xe0\x80\xff\xa0\xe0\xff\xa0\x80\xe0')
            patch.seek(offset)
            saveBoxes = [loadSettingFromConfigFile("Box1").split(" "), loadSettingFromConfigFile("Box2").split(" "), loadSettingFromConfigFile("Box3").split(" ")]
            for box in saveBoxes:
                for color in box:
                    patch.write(pack.ubyte(int(f'0x{color}', 16)))
            
    else:
        print("Save box color customization is disabled in the config file. Skipping...")

def randomizeBoxColors(xbe, active):
    if active == "T":
        with open(xbe, "r+b") as patch:
            status, offset = checkForByteString(xbe, b'\x80\x80\xff\xe0\x80\xff\xa0\xe0\xff\xa0\x80\xe0')
            patch.seek(offset)
            for boxColor in range(3):
                #Please note that these are in BGRA order in the xbe
                R = pack.ubyte(random.randint(0, 255))
                G = pack.ubyte(random.randint(0, 255))
                B = pack.ubyte(random.randint(0, 255))
                A = pack.ubyte(random.randint(200, 255)) #Keep this number high to ensure the box is always visible
                patch.write(B+G+R+A) #Merge all byte strings into one and write them
    else:
        print("Save box color randomization is disabled in the config file. Skipping...")

def makeGoldSometimesSpawnInPlaceOfCrystals(xbe, active):
    if active == "T":
        status, offset = checkForByteString(xbe, b'\x99\xB9\x06\x00\x00\x00\xF7\xF9\x83\xC2\x59')
        if not status:
            print("Gold sometimes spawns in place of crystals patch error:\nByte string not found! You might be using a unique version of BLiNX or a pre-patched XBE.")
        else:
            with open(xbe, "r+b") as patch:
                patch.seek(offset)
                patch.write(b'\x99\xB9\x18\x00\x00\x00\xF7\xF9\x83\xC2\x59')
    else:
        print("Gold sometimes spawning in place of crystals is disabled in the config file. Skipping...")

def randomizeBossDrops(xbe, active):
    validPatches = [
        b'\x99\xB9\x04\x00\x00\x00\xF7\xF9\x83\xC2\x48',  # Drop golem parts
        b'\x99\xB9\x03\x00\x00\x00\xF7\xF9\x83\xC2\x4D',  # Drop bombs
        b'\x99\xB9\x01\x00\x00\x00\xF7\xF9\x83\xC2\x52',  # Drop traffic cones
        b'\x99\xB9\x02\x00\x00\x00\xF7\xF9\x83\xC2\x53',  # Drop bullets (watch out! Danger!)
        b'\x99\xB9\x06\x00\x00\x00\xF7\xF9\x83\xC2\x59',  # Drop time crystals
        b'\x99\xB9\x0C\x00\x00\x00\xF7\xF9\x83\xC2\x5F',  # Drop both crystals and gold
        b'\x99\xB9\x06\x00\x00\x00\xF7\xF9\x83\xC2\x65',  # Drop gold (lucky!)
        b'\x99\xB9\x04\x00\x00\x00\xF7\xF9\x83\xC2\x71',  # Drop cat medals
    ]

    if active == "T":
        status, offset = checkForByteString(xbe, b'\x99\xB9\x06\x00\x00\x00\xF7\xF9\x83\xC2\x65')
        if not status:
            print("Randomizing boss drops patch error:\nByte string not found! You might be using a unique version of BLiNX or a pre-patched XBE.")
        else:
            with open(xbe, "r+b") as patch:
                patch.seek(offset)
                patch.write(random.choice(validPatches))
    else:
        print("Randomizing boss drops is disabled in the config file. Skipping...")
