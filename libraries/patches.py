import random

def checkForByteString(path, string):
    with open(path, 'rb') as file:
        content = file.read(0x150000)
        offset = content.find(string)
        return string in content, offset

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
