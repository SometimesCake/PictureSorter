#!/usr/bin/env python3
##################################################################
# Author: Darren Holtz
# Date: 1/22/2023
# Last Update: 1/22/2023
# Version: 1.0 
#
#   Program to take in a directory and hash every file recursivly
#   and save the resultes to a csv file.
#
##################################################################

import argparse
import glob
import os
import sys
import filetype
import datetime
import time
import time

import sc_utilities as utils

def main():
    directoryListingVersion = str(1.0)

    argparser = argparse.ArgumentParser(description='Creates a directory listing and saves results to a csv file.')
    argparser.version = directoryListingVersion
    argparser.add_argument('-d', metavar='startDirectory', action='store', help='Start directory.', required=True)
    argparser.add_argument('-w', metavar='outFile', action='store', help='File to write results to.', required=False)
    argparser.add_argument('--md5', action='store_true', help='Include MD5 in the output.', required=False)
    argparser.add_argument('--sha1', action='store_true', help='Include SHA1 in the output.', required=False)
    argparser.add_argument('--sha256', action='store_true', help='Include SHA256 the output.', required=False)
    argparser.add_argument('-v', action='store_true', help='Enable verbose notifications.', required=False)
    

    args = argparser.parse_args()

    direcotyListing = buildDirectoryListing(args.d, args.md5, args.sha1, args.sha256, args.v)
    
    if args.w != None:
        try:
            with open(args.w,'w') as outputFile:
                outputFile.write(direcotyListing)
        except Exception as e:
            sys.stderr.write("Error writing to file: " + args.w + "\n")
    else:
        print(direcotyListing)

############################################################################
#   Returns a string containing the directory listing of the requested path 
############################################################################
def buildDirectoryListing(path, md5, sha1, sha256, verbose):

    # Build Headder line
    directoryListing = "File Names, File Size Bytes, File Size String, Create Time, Accessed Time, Modified Time, FileType"
    if md5:
        directoryListing += ", md5"
    if sha1:
        directoryListing += ", sha1"
    if sha256: 
        directoryListing += ", sha256"
    directoryListing += "\n"

    # Load files
    fileList = []
    for filename in glob.iglob(path + '**/**', recursive=True, include_hidden=True):
        if os.path.isfile(filename):
            fileList.append(filename)
            fileCount += 1
            if verbose:
                print(f' Loading: {fileCount}', end='\r')
    
    if verbose:
        print (" ")
        print ("Loading Complete")

    
    processedCount = 0
    bytesProcessed = 0
    startTime = time.time()

    for filename in fileList:
        # File path and name
        directoryListing += filename

        # File size bytes
        fileSize = os.path.getsize(filename)
        bytesProcessed += fileSize
        directoryListing += ", " +  str(fileSize)

        # File size Pretty
        directoryListing += ", " +  utils.bytesToStr(fileSize)

        # File date times
        directoryListing += ", " +  str(datetime.datetime.fromtimestamp(os.path.getctime(filename)))
        directoryListing += ", " +  str(datetime.datetime.fromtimestamp(os.path.getatime(filename)))
        directoryListing += ", " +  str(datetime.datetime.fromtimestamp(os.path.getmtime(filename)))

        # File type
        directoryListing += ", " + str(filetype.guess_mime(filename))
            
        # MD5
        if md5:
            directoryListing += ", " + utils.md5sum(filename)

        # SHA1
        if sha1:
            directoryListing += ", " + utils.sha1sum(filename)

        # SHA256
        if sha256: 
            directoryListing += ", " + utils.sha256sum(filename)

        # End of line
        directoryListing += "\n"
        
        # End Loop Time
        loopEndTime = time.time()

        if verbose:
            processedCount += 1
            totalTime = time.strftime("%H:%M:%S", time.gmtime(loopEndTime - startTime))
            calculatedETA = time.strftime("%H:%M:%S", time.gmtime((((loopEndTime-startTime) * fileCount)/processedCount)- (loopEndTime-startTime)))
            utils.print_percent_complete(processedCount, fileCount, 40, str(processedCount) + "/" + str(fileCount) + " " + utils.bytesToStr(bytesProcessed) + " Processing Time: " + totalTime + " ETA: " + calculatedETA)

    return directoryListing

if __name__ == "__main__":
    main()
