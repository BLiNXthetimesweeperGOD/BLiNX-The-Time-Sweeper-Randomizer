#All tables will go in here to make the main script less messy
def badstages(): #A large number of values to avoid (goes beyond the stage count just to be safe)
    badStages = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, 67, 71, 75, 79, 83, 87, 91, 95, 99]
    return badStages

def enemies():
    enemies = [b'\x01\x01\x00\x00', #Chronoblobs
               b'\x01\x02\x00\x00',
               b'\x01\x03\x00\x00',
               b'\x03\x01\x00\x00', #Dust Herders
               b'\x03\x02\x00\x00',
               b'\x03\x03\x00\x00',
               b'\x04\x02\x00\x00', #Keroppers
               b'\x04\x03\x00\x00',
               b'\x05\x01\x00\x00', #Spikers
               b'\x05\x02\x00\x00',
               b'\x05\x03\x00\x00',
               b'\x06\x02\x00\x00', #Molegon
               b'\x07\x03\x00\x00', #Golems
               b'\x07\x05\x00\x00',
               b'\x08\x02\x00\x00', #Gate Keepers
               b'\x08\x03\x00\x00',
               b'\x09\x03\x00\x00', #Ice Turtle
               b'\x0A\x02\x00\x00', #Typhoon
               ]

    return enemies
