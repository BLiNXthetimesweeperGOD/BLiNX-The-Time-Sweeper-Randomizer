import random
from libraries.files import *
from libraries.tables import *
from libraries.OffsetGrabber import *
from libraries.configLoader import *
from libraries.patches import *
from libraries.randomizers import *
print("MOTAS isn't supported. Do not use MOTAS with this randomizer.")
isomode = False
xbe = dialogs.file()

if not os.path.exists("config.txt"): #If no config file exists, create one
    print("No config file exists. Creating the default config file...")
    createConfigFile()

if fileTools.ext(xbe) == "iso":
    print("ISO detected, switching modes")
    isomode = True
    from libraries.XISO import *
    iso = xbe
    xbe, rewriteOffset = getDefaultXBEFromISO(xbe)
    
outputName = fileTools.nameNoExt(xbe)+"_RANDO.xbe" #The name of the randomized XBE
fileTools.copy(xbe, outputName)                    #Create a copy of the XBE for randomization

seedPrints = 0
seed = 0

def seedGenerator():
    global seedPrints, seed
    setting = loadSettingFromConfigFile("UseSeed")
    if setting == "F":
        seed = seed #Set the seed to what it was last time it was set to ensure compatibility with string seeds
        if seedPrints == 0: #Only show the seed once - this is to avoid setting it multiple times, requiring a unique seed for each level
            seed = str(random.randint(1, 90000000)) #Converted to a string to ensure it (hopefully) always works when entered as the seed in the config file
            print(f"Seed: {seed}")
            seedPrints = 1
    elif setting == "T":
        seed = loadSettingFromConfigFile("Seed")
        if seedPrints == 0:
            print(f"Seed: {seed}")
            seedPrints = 1
    else:
        print("You entered an invalid setting into UseSeed. No seed will be generated or used.")
        return None
    
    return seed
        
def check(file, offset, index, identifier):
    with open(file, "rb") as xbe:
        xbe.seek(offset)
        if xbe.read(4)[index] == identifier:
            return True
        else:
            return False

def fixOffset(offset, offsetFixer): #Converts RAM offsets to XBE offsets
    return offset-offsetFixer

def parseTableHeader(blinx, headerOffset):
    blinx.seek(headerOffset)
    count = unpack.uint(blinx.read(4))
    objectTableOffset = fixOffset(unpack.uint(blinx.read(4)), offsetFixer)
    return count, objectTableOffset

def getOffsetFromTable(blinx, tableOffset, offsetFixer, tableID, stage):
    stages = 0xA0
    blinx.seek((tableOffset+(stage*4))+(stages*tableID))
    entry = fixOffset(unpack.uint(blinx.read(4)), offsetFixer)
    return entry
            
patched = False
badStages = badstages()
#enemies = enemies() #Grab the enemy table from (root folder)/libraries/tables.py
tableOffset, offsetFixer = getOffsets(xbe) #Get the start offset of the table and a value to correct pointers

with open(xbe, "rb") as blinx: #It's him!
    for stage in range(40):
        #These are pointers to the table headers. Since some are going to end up being less than 0, we do a check later on to avoid those ones.
        trash =       getOffsetFromTable(blinx, tableOffset, offsetFixer, 0, stage)
        UNKNOWN=      getOffsetFromTable(blinx, tableOffset, offsetFixer, 1, stage)
        item  =       getOffsetFromTable(blinx, tableOffset, offsetFixer, 2, stage)
        interactive = getOffsetFromTable(blinx, tableOffset, offsetFixer, 3, stage)
        enemy =       getOffsetFromTable(blinx, tableOffset, offsetFixer, 4, stage)
        camera =      getOffsetFromTable(blinx, tableOffset, offsetFixer, 5, stage)
        
        random.seed(seedGenerator()) #Set the seed before the patches
        
        #Patches
        if not patched:
            makeGoldSometimesSpawnInPlaceOfCrystals(outputName, loadSettingFromConfigFile("GoldSpawnsOverSomeCrystals"))
            randomizeBossDrops(outputName, loadSettingFromConfigFile("RandomizeBossGoldDrops"))
            patched = True

        #Randomizers
        random.seed(seedGenerator()) #Set the seed again for enemies
        if loadSettingFromConfigFile("RandomizeEnemies") == "T":
            if stage not in badStages:
                if enemy > 0:
                    count, offset = parseTableHeader(blinx, enemy)
                    replaceMonsters(outputName, offset, count)
                    
        random.seed(seedGenerator()) #Set the seed again for items
        if loadSettingFromConfigFile("RandomizeItems") == "T":
            if stage not in badStages:
                if item > 0:
                    count, offset = parseTableHeader(blinx, item)
                    replaceItems(outputName, offset, count)
                    
        random.seed(seedGenerator()) #Set the seed again for interactive objects
        if loadSettingFromConfigFile("RandomizeInteractiveObjects") == "T":
            if stage not in badStages:
                if interactive > 0:
                    count, offset = parseTableHeader(blinx, interactive)
                    replaceRollingObjectSpawners(outputName, offset, count)
                    
if isomode == True:
    with open(outputName, "rb") as xbe:
        writeDefaultXBEToISO(iso, xbe.read(), rewriteOffset)

