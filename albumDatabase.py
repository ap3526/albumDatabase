#!/usr/bin/env python3
#
#This program will help maintain a flat-file database of album information. Depending on the argument, the user can
#view artist/album information, add a new album to the database, or delete an album from the database

import sys
import os

albumTracks = {}
#function traverses through a list of lists, where each sublist contains artist and album information
def listAlbums():
    listOfAll = makeList()
    listOfAll.sort()
    artistList = []
    for x in range(len(listOfAll)):
        if listOfAll[x][0] in artistList:
            continue
        else:
            artistList.append(listOfAll[x][0])
    for artist in range(len(artistList)):
        print(artist+1,artistList[artist])
    while True:
        chooseArtist = input("Enter Artist Number or q to Quit: ")
        if chooseArtist == 'q':
            exit()
        else:
            albumList = albumMenu(chooseArtist, listOfAll, artistList)
            for album in range(len(albumList)):
                print(album+1, albumList[album])

            go = True
            while go is True:
                chooseAlbum = input("Enter Album Number or a to Go Back: ")
                if chooseAlbum == 'a':
                    artistMenu(listOfAll)
                    go = False
                else:
                    songMenu(chooseAlbum, listOfAll, albumList)
                    back = input("Enter a to go back: ")
                    if back == 'a':
                        for album in range(len(albumList)):
                            print(album+1, albumList[album])
#function displays the menu of artists
def artistMenu(contentList):
    artistList = []
    for x in range(len(contentList)):
        if contentList[x][0] in artistList:
            continue
        else:
            artistList.append(contentList[x][0])
    for artist in range(len(artistList)):
        print(artist+1,artistList[artist])
    return artistList
#function displays the menu of albums
def albumMenu(selection, contentList, artistList):
    albumList = []
    selection = int(selection)
    value = selection - 1
    albumList.append(contentList[value][1])
    for x in range(len(contentList)):
        if x == value:
            continue
        elif contentList[value][0] == contentList[x][0]:
            albumList.append(contentList[x][1])
    albumList.sort()
    return albumList
#function displays the menu of songs
def songMenu(selection, contentList, albumList):
    songList = []
    selection = int(selection)
    value = selection - 1
    for x in range(len(contentList)):
        if contentList[x][1] == albumList[value]:
            for y in range(2,len(contentList[x])):
                songList.append(contentList[x][y])
    for songs in songList:
        print(songs)
#functions creates a list of lists with the contents of the database
def makeList():
    listOfAll = []
    each = []
    for line in open(os.environ["CDDB"]).readlines():
        if line.startswith("\n") and each:
            listOfAll.append(each[:])
            each = []
        if line == "\n":
            continue
        each.append(line.strip("\n"))
    if not each:
        pass
    else:
        listOfAll.append(each)

    return listOfAll
#function displays artist and album information, allowing the user to delete an album from the database
def deleteAlbum():
    listOfAll = makeList()
    
    listOfAll.sort()
    artistList = []
    for x in range(len(listOfAll)):
        if listOfAll[x][0] in artistList:
            continue
        else:
            artistList.append(listOfAll[x][0])
    for artist in range(len(artistList)):
        print(artist+1,artistList[artist])
    chooseArtist = input("Enter Artist Number or q to Quit: ")
    if chooseArtist == 'q':
        exit()
    else:
        albumList = []
        chooseArtist = int(chooseArtist)
        value = chooseArtist - 1
        albumList.append(listOfAll[value][1])
        for x in range(len(listOfAll)):
            if x == value:
                continue
            elif listOfAll[value][0] == listOfAll[x][0]:
                albumList.append(listOfAll[x][1])
        albumList.sort()
        for album in range(len(albumList)):
            print(album+1, albumList[album])
        chooseAlbum = input("Enter Album Number or a to Go Back: ")
        if chooseAlbum == 'a':
            exit()
        else:
            chooseAlbum = int(chooseAlbum)
            for x in range(len(listOfAll)):
                if listOfAll[x][1] == albumList[chooseAlbum-1]:
                    del listOfAll[x][0:]
    temp = open('test.txt', 'w+')
    for x in range(len(listOfAll)):
        if not x:
            pass
        temp.write("\n")
        for y in range(len(listOfAll[x])):
            temp.write(listOfAll[x][y] + "\n")
    temp.close()
    os.rename('test.txt', os.environ["CDDB"])

#function allows the user to add an album to the database
def addAlbum():
    trackList = []
    listOfAll = makeList()
    artist = input("Artist? ")
    album = input("Album Name? ")
    release = input("Release Date? ")
    trackList.append(release)
    for x in range(len(listOfAll)):
        if listOfAll[x][0] == artist:
            if listOfAll[x][1] == (release + ' ' +  album):
                print("Album already exists")
                exit(0)
    track = input("Track List? (Enter q when done) ")
    while track != "q":
        trackList.append(track)
        track = input("Next track: ")
    albumTracks[album] = trackList
    database = open(os.environ["CDDB"], 'a+')
    database.write(artist + "\n")
    database.write(release + ' ' + album + "\n")
    for key,val in albumTracks.items():
        for track in val[1:]:
            database.write("-" +  track + "\n")
    database.write("\n")
    database.close()
#function prints a usage message
def printUsage():
    print ("-l List Albums")
    print ("-d Delete an album")
    print ("-a Add an album")
    print ("-h Show usage message and quit")

if __name__ == "__main__":
    #checks if an environment was supplied
    if "CDDB" not in os.environ:
        print("No environment supplied")
        exit(0)
    #checks to make sure arguments are valid
    if len(sys.argv) == 2:
        if(sys.argv[1].strip() == "-l"):
            listAlbums()
        elif(sys.argv[1].strip() == "-d"):
            deleteAlbum()
        elif(sys.argv[1].strip() == "-a"):
            addAlbum()
        elif(sys.argv[1].strip() == "-h"):
            printUsage()
            exit(0)
        else:
            printUsage()
            exit(0) 
    else:
        printUsage()
        exit(0)
