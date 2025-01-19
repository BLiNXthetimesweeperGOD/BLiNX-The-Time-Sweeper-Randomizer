#Config file script
def loadSettingFromConfigFile(setting):
    with open("config.txt", "r") as config:
        settings = config.readlines()
    for line in settings:
        if line.startswith(setting):
            if "\n" in line:
                return line.split("=")[1][0:-1]
            else:
                return line.split("=")[1]
        
def createConfigFile(): #Creates a basic config file with all of the default comments and settings in it
    defaultSettings = '''? T is True, F is False
? Not all of these are implemented yet!
? General functionality
UseSeed=F
Seed=What's a seed
RandomizeEnemies=T
RandomizeTrash=T
RandomizeItems=T
RandomizeInteractiveObjects=T
RandomizeItemVisuals=F
? Patches (boss gold drops is a patch, so it has been moved to this section)
RandomizeBossGoldDrops=T
GoldSpawnsOverSomeCrystals=T
? Save box color settings
RandomizeBoxColors=F
CustomizeBoxColors=T
? If custom colors are turned on, modify these
? The color order is BGRA
Box1=00 00 FF FF
Box2=00 FF 00 FF
Box3=FF 00 00 FF
? Shop randomization settings
RandomizeShopVisualsAndPrices=T
'''
    with open("config.txt", "w") as config:
        config.write(defaultSettings)
