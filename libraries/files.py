import struct
import tkinter as tk
from tkinter import filedialog
import os
import zlib

class fileTools:
    """
    A class to handle various operations involving OS
    """
    def ext(filepath):
        return os.path.splitext(filepath)[1][1:]
    def name(path):
        return os.path.basename(path)
    def nameNoExt(path):
        return os.path.splitext(os.path.basename(path))[0]
    def size(path):
        return os.path.getsize(path)
    def folder(path):
        return os.path.dirname(path)
    def compress(data):
        return zlib.compress(data)
    def decompress(data):
        return zlib.decompress(data)
    def copy(inpath, outpath):
        with open(inpath, "rb") as i:
            with open(outpath, "w+b") as o:
                o.write(i.read())
            

class dialogs:
    """
    You can quickly open a folder/file dialog with this class
    """
    def file():
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename()
        root.destroy()
        return file
    def files():
        root = tk.Tk()
        root.withdraw()
        files = filedialog.askopenfilenames()
        root.destroy()
        return files
    def folder():
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory()
        root.destroy()
        return folder
    def listedFolder():
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory()
        root.destroy()
        return os.listdir(folder)

class encode:
    """
    You can quickly encode various types of strings with this class
    """
    def utf8(data):
        return data.encode("UTF-8")
    
    def utf16(data):
        return data.encode("UTF-16")
    
    def utf32(data):
        return data.encode("UTF-32")
    
    def ascii(data):
        return data.encode("ASCII")

class decode:
    """
    You can quickly decode various types of strings with this class
    """
    def utf8(data):
        return data.decode("UTF-8")
    
    def utf16(data):
        return data.decode("UTF-16")
    
    def utf32(data):
        return data.decode("UTF-32")
    
    def ascii(data):
        return data.decode("ASCII")

class pack:
    """
    You can pack a single value at a time with this class
    """
    def byte(value):
        return struct.pack("<b", value)
    
    def ubyte(value):
        return struct.pack("<B", value)
    
    def short(value):
        return struct.pack("<h", value)
    
    def ushort(value):
        return struct.pack("<H", value)
    
    def int(value):
        return struct.pack("<i", value)
    
    def uint(value):
        return struct.pack("<I", value)
    
    def long(value):
        return struct.pack("<q", value)
    
    def ulong(value):
        return struct.pack("<Q", value)
    
    def float(value):
        return struct.pack("<f", value)
    
    def double(value):
        return struct.pack("<d", value)

class multipack:
    """
    You can pack multiple values at once with this class
    """
    def byte(values):
        return struct.pack("<{}b".format(len(values)), *values)
    
    def ubyte(values):
        return struct.pack("<{}B".format(len(values)), *values)
    
    def short(values):
        return struct.pack("<{}h".format(len(values)), *values)
    
    def ushort(values):
        return struct.pack("<{}H".format(len(values)), *values)
    
    def int(values):
        return struct.pack("<{}i".format(len(values)), *values)
    
    def uint(values):
        return struct.pack("<{}I".format(len(values)), *values)
    
    def long(values):
        return struct.pack("<{}q".format(len(values)), *values)
    
    def ulong(values):
        return struct.pack("<{}Q".format(len(values)), *values)
    
    def float(values):
        return struct.pack("<{}f".format(len(values)), *values)
    
    def double(values):
        return struct.pack("<{}d".format(len(values)), *values)

class unpack:
    """
    You can unpack a single value at a time with this class
    """
    def byte(data):
        return struct.unpack("<b", data)[0]
    
    def ubyte(data):
        return struct.unpack("<B", data)[0]

    def short(data):
        return struct.unpack("<h", data)[0]
    
    def ushort(data):
        return struct.unpack("<H", data)[0]
    
    def int(data):
        return struct.unpack("<i", data)[0]
    
    def uint(data):
        return struct.unpack("<I", data)[0]

    def long(data):
        return struct.unpack("<q", data)[0]
    
    def ulong(data):
        return struct.unpack("<Q", data)[0]
    
    def float(data):
        return struct.unpack("<f", data)[0]
    
    def double(data):
        return struct.unpack("<d", data)[0]

class multiunpack:
    """
    You can unpack multiple values at once with this class
    """
    def byte(data):
        count = len(data)
        return struct.unpack("<{}b".format(count), data)
    
    def ubyte(data):
        count = len(data)
        return struct.unpack("<{}B".format(count), data)

    def short(data):
        count = len(data) // 2
        return struct.unpack("<{}h".format(count), data)
    
    def ushort(data):
        count = len(data) // 2
        return struct.unpack("<{}H".format(count), data)
    
    def int(data):
        count = len(data) // 4
        return struct.unpack("<{}i".format(count), data)
    
    def uint(data):
        count = len(data) // 4
        return struct.unpack("<{}I".format(count), data)

    def long(data):
        count = len(data) // 8
        return struct.unpack("<{}q".format(count), data)
    
    def ulong(data):
        count = len(data) // 8
        return struct.unpack("<{}Q".format(count), data)
    
    def float(data):
        count = len(data) // 4
        return struct.unpack("<{}f".format(count), data)
    
    def double(data):
        count = len(data) // 8
        return struct.unpack("<{}d".format(count), data)

