import struct
import random
import os
def getOffsets(file): #Old code, could use a rewrite
    sectionName = []
    sectionAddresses = []
    sectionMath = []
    name = []
    xbeTitleInfoStartAddress = 0x110 # Where info like the company compiling the XBE and game name is stored
    sectionPointerStartAddress = 0x120 #          Where in the XBE to jump to to get to the section pointers
    namestring = ""
    with open(file, 'rb') as f:
        FINDS = [b'\x0f\xb6\x47\x02\x8d\x14\x80\xc1\xe2\x04\x8b\x82',       #Prop table
                 b'\x56\x8D\x34\x40\x50\x8D\x34\xB5',                       #Map table
                 b'\x74\x31\x8b\x08\x3b\xcb\x8b\x70\x04\x7e\x28\x8b\xf9\x90'#Stage layouts
                 ]
        tables = ["Prop table", "Map table", "Stage layouts"]
        offsets = []
        FindID = 0
        complete = 0
        CHECK = False
        xbename = os.path.basename(file)
        print("XBE Name:", xbename)
        try:
            for FIND in FINDS:
                f.seek(0)
                FindID = 0
                CHECK = False
                while True:
                    scannerByte = f.read(1)
                    if scannerByte[0] == FIND[FindID]:
                        FindID+=1
                        CHECK = True
                    if scannerByte[0] != FIND[FindID] and CHECK == False:
                        FindID = 0
                    CHECK = False
                    if FindID == len(FIND)-1:
                        if complete != 2:
                            f.seek(1,1)
                            #print(hex(f.tell()))
                        if complete == 2:
                            
                            f.seek(-27,1)
                        stageLayoutsOffset = struct.unpack("<I", f.read(4))[0]
                        offsets.append(stageLayoutsOffset)
                        print("%s:" % (tables[complete]), hex(stageLayoutsOffset))
                        complete += 1
                        break
        except:
            "Platinum Hits or MOTAS detected"
        f.seek(0x11C)
        totalSections = struct.unpack('<I', f.read(4))[0]#               The number of sections in this XBE file
        f.seek(xbeTitleInfoStartAddress)
        titleInfoAddress = struct.unpack('<i', f.read(4))[0]
        f.seek(titleInfoAddress+0xC)#                                  Skip the stuff that isn't the game name
        namestring2 = ""
        for i in range(int(0x90/2)):
            letter = f.read(1)
            null = f.read(1)
            if letter == b'\x00':
                for l in name:
                    namestring = namestring+chr(l[0])
                break
            name.append(letter)
        for letter in namestring:
            if letter != ":":
                namestring2 = str(namestring2+letter)
        f.seek(sectionPointerStartAddress)
        sectionPTRStart = f.seek(int(struct.unpack('<I',  f.read(4))[0]-0x10000))#  The start of the pointers
        number = 0
        sectionData = []#Where this script stores the retrieved info on sections
        number = sectionPTRStart
        for i in range(totalSections):#Get the section names and addresses
            Data = struct.unpack('<I', f.read(4))[0]
            sectionStartRAMAddress = struct.unpack('<I', f.read(4))[0]#The area in RAM where this section starts
            sectionEndRAMAddress = struct.unpack('<I', f.read(4))[0]#The area in RAM where this section ends
            sectionStartAddress = struct.unpack('<I', f.read(4))[0]#The area in the XBE where this section starts
            sectionEndAddress = struct.unpack('<I', f.read(4))[0]#The area in the XBE where this section ends
            sectionNameAddress = struct.unpack('<I', f.read(4))[0]-0x10000#The address of the name of this section
            f.seek(sectionNameAddress)
            A = str(f.read(0x20))
            sectionTitle1 = A.split('\\')[0]
            sectionTitle2 = sectionTitle1.split('\'')[1]#Remove last of Python IO stuff from the section name
            sectionDataInfo = sectionTitle2, sectionStartAddress, sectionEndAddress, sectionStartRAMAddress, sectionEndRAMAddress
            sectionData.append(sectionDataInfo)
            f.seek(sectionPTRStart)
            print(f"Section Name: {sectionTitle2}\nSection start address (XBE): {hex(sectionStartAddress)}\nSection Start Address (RAM): {hex(sectionStartRAMAddress)}\nSection type ID: {hex(Data)}\nValue used for adjustment: {hex(sectionStartRAMAddress-sectionStartAddress)}\n")
            number += 0x38
            f.seek(number)
            if sectionTitle2 == ".data":
                sectionMath = sectionStartRAMAddress-sectionStartAddress
                C = 0
                for offset in offsets:
                    NewOffset = (sectionMath-offset)*-1
                    print(tables[C]+" (adjusted):", hex(NewOffset))
                    if tables[C].startswith("Stage"):
                        return NewOffset, sectionMath
                    C+=1
                if C == 2: #Platinum Hits
                    return 0x372918, sectionMath
