#Config file script
def loadSettingFromConfigFile(setting):
    with open("config.txt", "r") as config:
        settings = config.readlines()
    for line in settings:
        if line.startswith(setting):
            return line.split("=")[1][0:-1]
        
def createConfigFile(): #Creates a basic config file with all of the default comments and settings in it
    defaultSettings = '''? T is True, F is False
? General functionality
UseSeed=F
Seed=BLINX_3_IS_REAL_PLEASE_BELIEVE_ME
RandomizeEnemies=T
RandomizeTrash=T
RandomizeItems=T
RandomizeItemVisuals=F
? Patches
GoldSpawnsOverSomeCrystals=T
'''
    with open("config.txt", "w") as config:
        config.write(defaultSettings)
