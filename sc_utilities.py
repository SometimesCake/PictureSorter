#########################################################################
# Author: Darren Holtz
# Date: 10/04/2022
# Last Update: 01/18/2023
# Version: 1.1
#   1.0 Utilities useful in most Python Scripts are stored here.
#   2.0 Added Hashing functions.
#       
#########################################################################

import math
import os
import sys
import hashlib

#########################################################################
# Prints a completion bar that is updated with each subsequent call.
#########################################################################
def print_percent_complete(index, total, bar_len=50, title='processing'):

    percent_complete = (index+1)/total*100
    percent_complete = round(percent_complete,1)
    if percent_complete > 100:
        percent_complete = 100

    done = round(percent_complete/(100/bar_len))
    togo = bar_len-done

    done_str = '*'*int(done)
    togo_str = '-'*int(togo)

    print(f'\t{title} [{done_str}{togo_str}] {percent_complete}%', end='\r')

    #if round(percent_complete) == 100:
    if index == total:
        print(" ")
        print("Complete")

#########################################################################
# Checks the OS running and returns the appropriate folder deliminiter. 
# Better ways:  Depricated
# import os
# os.sep 
# path = os.path.join('folder_name', 'file_name')
#########################################################################
def getFolderDelimiter():
    return os.sep

#########################################################################
# Checks if the folder in the path exists, if not it builds the 
# directory and the path. No return. 
#########################################################################
def checkPath(mypath):
    slash = getFolderDelimiter()
    pathList = mypath.split(slash)
    buildPath = ""
    for mydir in pathList:
        buildPath = buildPath + mydir + slash
        if not(os.path.isdir(buildPath)):
            os.mkdir(buildPath, 0o666)

#########################################################################
# Takes a number of bytes and returns a string representation of the 
# bytes rounded to the nearest .00 places
#########################################################################
def bytesToStr(byteCount):
    if byteCount < 1:
        return "0 B"
    
    byteUnits = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    unit = int(math.floor(math.log(byteCount,1024)))
    unitPower = math.pow(1024, unit)
    unitConversion = round(byteCount / unitPower, 2)
    
    return str(unitConversion) + " " + byteUnits[unit]

#########################################################################
# Attempts to undo the bytesToStr function. Grainularity will be lost 
# from the original. 
#########################################################################
def strToBytes(byteString):
    byteUnits = {"B":0, "KB":1, "MB":2, "GB":3, "TB":4, "PB":5, "EB":6, "ZB":7, "YB":8}
    byteToken = byteString.split(" ")

    baseByte = float(byteToken[0])
    if len(byteToken) > 1:
        byteUnit = byteString.split(" ")[1].strip()
    else:
        # if no unit identified, default to byte.
        byteUnit = "B"
    
    return math.floor(baseByte * (math.pow(1024,byteUnits[byteUnit])))

#########################################################################
# Returns the SHA1 of a file.
#########################################################################
def sha1sum(filename):
    return hashsum(filename, hashlib.sha1())

#########################################################################
# Returns the md5 of a file.
#########################################################################
def md5sum(filename):
    return hashsum(filename, hashlib.md5())

#########################################################################
# Returns the sha256 of a file.
#########################################################################
def sha256sum(filename):
    return hashsum(filename, hashlib.sha256())

#########################################################################
# Returns the hash value of the file, returns -1 on failure.
#########################################################################
def hashsum(filename, hashBuild):
    
    # open file for reading in binary mode
    try:
        with open(filename,'rb') as file:
        # loop till the end of the file
            block = 0
            while block != b'':
               # read 1024 bytes at a time
                block = file.read(1024)
                hashBuild.update(block)
    except Exception as e:
        sys.stderr.write("Error reading input file: " + filename + "\n")
        return -1
    
    # return the hex representation of digest
    return hashBuild.hexdigest()

#########################################################################
# Load a text file into an array of strings.
#########################################################################
def loadTextFile (filename):
    returnArray = []

    try:
        with open(filename,'r') as file:
            returnArray = file.readlines()
                
    except Exception as e:
        sys.stderr.write("Error reading input file: " + filename + "\n")
        return -1
    
    return returnArray