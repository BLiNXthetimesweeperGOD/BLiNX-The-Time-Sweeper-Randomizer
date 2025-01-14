from libraries.files import *
import hashlib

def getFileContents(filePath):
    with open(filePath, "rb") as file:
        return file.read()
    
def genHash(data):
    algorithm = hashlib.sha256()
    algorithm.update(data)
    return algorithm.hexdigest()

def checkHash(filePath1, filePath2):
    hash1 = genHash(filePath1)
    hash2 = genHash(filePath2)
    return hash1 == hash2

def alignmentCheck(offset):
    return offset % 4 == 0

def checkForByteString(path, string):
    with open(path, 'rb') as file:
        content = file.read(0x100000)
        offset = content.find(string)
        return string in content, offset

def getDefaultXBEFromISO(iso):
    filename = ""
    offset = checkForByteString(iso, b'MICROSOFT*XBOX*MEDIA')[1]
    with open(iso, "r+b") as img:
        img.seek(offset)
        img.read(0x14)
        rootDir = unpack.uint(img.read(4))*2048
        img.seek(rootDir)
        while filename != "default.xbe":
            unneededdata = img.read(4) #Not needed here
            fileOffset = unpack.uint(img.read(4))*2048
            fileSize = unpack.uint(img.read(4))
            fileType, fileNameLength = img.read(2)
            filename = decode.utf8(img.read(fileNameLength))
            currOffset = img.tell()
            while alignmentCheck(currOffset) != True: #For handling alignment/padding
                currOffset+=1
            img.seek(currOffset)
            
        
        img.seek(fileOffset)
        fileData = img.read(0x1000) #Only a small part of the header is needed. We never alter the header in these randomizers.
        fileHash = genHash(fileData)
        backupPath = fileHash+"_BACKUP.xbe"
        if os.path.exists(backupPath): #The backup already exists. Restore it.
            img.seek(fileOffset)
            img.write(getFileContents(backupPath))
                
        else: #If the backup doesn't exist, create it
            with open(backupPath, "w+b") as xbe:
                img.seek(fileOffset)
                xbe.write(img.read(fileSize))

        with open(filename, "w+b") as xbe: #Extract a fresh XBE for randomization
            img.seek(fileOffset)
            xbe.write(img.read(fileSize))
                      
        print(filename, hex(fileOffset), hex(fileSize))
        return filename, fileOffset

def writeDefaultXBEToISO(iso, data, offset):
    with open(iso, "r+b") as img:
        img.seek(offset)
        img.write(data)
