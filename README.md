# PictureSorter
This was a fun program to list all pictures/files in a list of directories, find any duplicates and
sort the photos I wanted to keep. 

## Directory Listing
First step in the process. Program to list and hash every file recursivly in a directory.

usage: directoryListing.py [-h] -d startDirectory [-w outFile] [--md5] [--sha1] [--sha256] [-v]
directoryListing.py: error: the following arguments are required: -d

    -h  Help listing
    -d  Directory to list files
    -w  File to save results to.
    --md5   set flag to calculate md5 of listed files
    --sha1  set flag to calculate sha1 of listed files
    --sha256    set flag to calculate sha256 of listed files

This is a work in progress, and my first project using GitHub. 