import sys
import psycopg2
import psycopg2.extras
import random

from os import system

from db.db import Database
from entities import band, track, album
from entities.band import Genres, Band
from enum import Enum, auto


class Menu:
    def __init__(self, database):
        self.database = database

    def print_main_menu(self):
        print("choose your action")
        print("1) select entity to interact")
        print("2) get all")
        print("3) search")
        print("4) generate random entities")
        print("5) exit")

    def clear(self):
        system('clear')

    def print_actions_menu(self):
        print("actions:")
        print("1) create")
        print("2) read")
        print("3) update")
        print("4) delete")
        print("5) back")

    def print_search_menu(self):
        print("1) Band by exists field (bool)")
        print("2) Band by genre filed (enum)")
        print("3) Band by name (without word)")
        print("4) Album by name (full phrase)")
        print("5) back")


    def search_menu_handler(self):
        local_loop = 1
        while local_loop == 1:
            self.clear()
            print("SEARCH\n")
            self.print_search_menu()
            try:
                n = int(input("\naction: "))
                if n == 1:
                    exists = bool(input("0 for false | 1 for true: "))
                    bands = self.database.get_bands_by_exists_attr(exists)
                    if bands != None:
                        for band in bands:
                            print("\n", band, "\n")
                    else:
                        print("No result")
                    input()

                elif n == 2:
                    genre = int(input("Genre (0 rock, 1 rap, 2 punk, 3 chanson, 4 classic): "))
                    bands = self.database.get_bands_by_genre(list(Genres)[genre])
                    for b in bands:
                        print("\n", b, "\n")
                    input()

                elif n == 3:
                    name = input("Name: ")
                    bands = self.database.search_by_word_not_belong(name)
                    if len(bands) == 0:
                        print('empty')
                    else:
                        for b in bands:
                            print("\n", b, "\n")
                    input()
                elif n == 4:
                    phrase = input("Phrase: ")
                    res = self.database.search_by_phrase(phrase)
                    if len(res) == 0:
                        print('empty')
                    else:
                        for r in res:
                            print("\n", r, "\n")
                    input()

                elif n == 5:
                    local_loop = 0                        
            except Exception as e:
                print("%s" % e)
                input()
        
    def album_interact(self):
        local_loop = 1
        while local_loop == 1:
            self.clear()
            print("\nALBUM ACTION\n")
            self.print_actions_menu()
            try:
                # print("1) create")
                # print("2) read")
                # print("3) update")
                # print("4) delete")
                # print("5) back")
                n = int(input())
                if n == 1:
                    print()
                    try:
                        name = input("Name: ")
                        band_id = int(input("Band id:"))
                        a = album.Album(name, 0)
                        self.database.add_album(band_id, a)
                    except Exception as e:
                        print("%s" % e)
                        input()
                elif n == 2:
                    print()
                    try:
                        id = int(input("Album id to get: "))
                        a = self.database.get_album_by_id(id)
                        if a != None:
                            a.print_self()
                        else:
                            print("no entity")
                            input()
                        input()
                    except Exception as e:
                        print("%s" % e)
                        input()
                elif n == 3:
                    print()
                    try:
                        id = int(input("id: "))
                        a = self.database.get_album_by_id(id)
                        if a != None:
                            changed = False
                            print("\nold entity")
                            a.print_self()
                            print()
                            
                            if input("Change tracksCount? (Y/N)") == 'Y':
                                na = album.Album(input("new name: "), int(input("tracksCount: ")), id)
                            else:
                                na = album.Album(input("new name: "), a.tracksCount, id)
                            self.database.edit_song(id, na)
                            input()
                        else:
                            print("No entity")
                            input()
                    except Exception as e:
                        print("%s" % e)
                        input()
                elif n == 4:
                    print()
                    try:
                        id = int(input("id: "))
                        self.database.delete_album_by_id(id)
                        print()
                    except Exception as e:
                        print("%s" % e)
                        input()
                elif n == 5:
                    local_loop = 0
                    
            except Exception as e:
                print("%s" % e)
                input()

    def song_interact(self):
        local_loop = 1
        while local_loop == 1:
            self.clear()
            print("SONG ACTIONS\n")
            self.print_actions_menu()
            try:
                n = int(input("\naction: "))
                if n == 1:
                    print()
                    name = input("song name: ")
                    try:
                        length = int(input("song length: "))
                        number_in_album = int(input("number in album: "))
                        album_id = int(input("album id: "))
                        s = track.Track(name, length, number_in_album)
                        self.database.add_song(album_id, s)
                    except Exception as e:
                        print("%s" % e)
                    input()
                elif n == 2:
                    print()
                    try:
                        id = int(input("id: "))
                        s = self.database.get_song_by_id(id)
                        if s != None:
                            s.print_self()
                        else:
                            print("no entity")
                            input()
                        input()
                    except Exception as e:
                        print("%s" % e)
                        input()
                elif n == 3:
                    print()
                    try:
                        id = int(input("id: "))
                        s = self.database.get_song_by_id(id)
                        if s != None:
                            print("\nold entity")
                            s.print_self()
                            print()
                            s = track.Track(input("new name: "), int(input("new length: ")), id)
                            self.database.edit_song(id, s)
                            input()
                        else:
                            print("No entity")
                            input()
                    except Exception as e:
                        print("%s" % e)
                        input()
                
                elif n == 4:
                    print()
                    try:
                        id = int(input("id: "))
                        self.database.delete_song_by_id(id)
                        print()
                    except Exception as e:
                        print("%s" % e)
                elif n == 5:
                    local_loop = 0
                else:
                    print("wrong command")
                    input()
            except Exception as e:
                print("%s" % e)


    def band_interact(self):
        local_loop = 1
        while local_loop == 1:
            self.clear()
            print("BAND ACTIONS\n")
            self.print_actions_menu()
            try:
                n = int(input("action: "))
                if n == 1:
                    self.clear()
                    print("BAND ACTIONS\n")
                    self.print_actions_menu()
                    try:
                        name = input("Band name: ")
                        genre = int(input("Genre (0 rock, 1 rap, 2 punk, 3 chanson, 4 classic): "))
                        if genre > 4 or genre < 0:
                            print("wrong genre")
                            input()
                            break
                        exists = int(input("Exists (1 true, 0 false): "))
                        if exists < 0 or exists > 1:
                            print("wrong ex")
                            input()
                            break
                        b = Band(name, list(Genres)[genre], bool(exists))
                        self.database.add_band(b)
                        print("added")                 
                    except Exception as e:
                        print("%s" % e)
                    input()
                elif n == 2:
                    self.clear()
                    print("BAND ACTIONS\n")
                    self.print_actions_menu()
                    try:
                        id = input("id: ")
                        band = self.database.get_band_by_id(int(id))
                        if band != None:
                            band.print_self()
                        else:
                            print("no entity")
                            input()
                        input()
                    except Exception as e: 
                        print("%s" % e)
                        input()
                elif n == 3:
                    self.clear()
                    print("BAND ACTIONS\n")
                    self.print_actions_menu()
                    try:
                        id = input("id: ")
                        band = self.database.get_band_by_id(int(id))
                        print("old entity")
                        if band != None:
                            band.print_self()
                            print()
                            name = input("Band name: ")
                            genre = int(input("Genre (0 rock, 1 rap, 2 punk, 3 chanson, 4 classic): "))
                            if genre > 4 or genre < 0:
                                print("wrong genre")
                                input()
                                break
                            exists = int(input("Exists (1 true, 0 false): "))
                            if exists < 0 or exists > 1:
                                print("wrong ex")
                                input()
                                break
                            b = Band(name, list(Genres)[genre], bool(exists))
                            self.database.edit_band(id, b)
                            input()
                        else:
                            print("no entity")
                            input()
                    except Exception as e: 
                        print("%s" % e)
                        input()
                elif n == 4:
                    self.clear()
                    print("BAND ACTIONS\n")
                    self.print_actions_menu()
                    id = input("id: ")
                    if self.database.delete_band_by_id(id):
                        print("deleted!")
                        input()
                    else:
                        print("smth wrong")
                        input()
                elif n == 5:
                    local_loop = 0
                else:
                    print("wrong command")
                    input()
            except Exception as e:
                print("%s" % e)
                input()

    def select_entity_menu(self):
        local_loop = 1
        while local_loop == 1:
            self.clear()
            print("You are in entity selection menu")
            print("1) band")
            print("2) album")
            print("3) song")
            print("4) back")
            try:
                n = int(input("select: "))
                if n == 1:
                    self.band_interact()
                elif n == 2:
                    self.album_interact()
                elif n == 3:
                    self.song_interact()
                elif n == 4:
                    local_loop = 0
            except Exception as e:
                print("%s" % e)
                input()


    def get_all_menu(self):
        local_loop = 1
        while local_loop == 1:
            self.clear()
            print("you are at 'get all' menu")
            print("1) band")
            print("2) album")
            print("3) song")
            print("4) back")
            try:
                n = int(input("select: "))
                if n == 1:
                    print('bands')
                    bands = self.database.select_all('bands')
                    for b in bands:
                        print(b)
                    input()
                elif n == 2:
                    print('albums')
                    albums = self.database.select_all('albums')
                    for a in albums:
                        print(a)
                    input()
                elif n == 3:
                    print('songs')
                    songs = self.database.select_all('songs')
                    for s in songs:
                        print(s)
                    input()
                elif n == 4:
                    local_loop = 0
            except Exception as e:
                print("%s" % e)
                input()
        
    def main_loop(self):
        loop = 1

        while loop == 1:
            self.clear()
            self.print_main_menu()
            n = input("choice: ")
            try:
                n = int(n)
                if n == 1:
                    self.clear()
                    self.select_entity_menu()
                elif n == 2:
                    self.clear()
                    self.get_all_menu()
                elif n == 3:
                    self.clear()
                    self.search_menu_handler()
                elif n == 4:
                    self.clear()
                    self.database.fill_db_with_random_entities(int(input("Number of entities in each table:")))
                elif n == 5:
                    loop = 0
                else:
                    print("wrong choice")
                    input()

            except Exception as e:
                print("%s" % e)
                input()

