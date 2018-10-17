import sys
import psycopg2
import psycopg2.extras
import random

from os import system

from db.db import Database
from entities import band, track, album
from entities.band import Genres, Band
from enum import Enum, auto

def clear():
    system('clear')

LOOP_RANGE = 15
current_datbase = Database()
current_datbase.connect('lab1')

def print_main_menu():
    print("choose your action")
    print("1) select entity to interact")
    print("2) get all")
    print("3) search")
    print("4) exit")


def print_actions_menu():
    print("actions:")
    print("1) create")
    print("2) read")
    print("3) update")
    print("4) delete")
    print("5) back")

def print_search_menu():
    print("1) Band by exists field (bool)")
    print("2) Band by genre filed (enum)")
    print("3) Song by name (without word)")
    print("4) Album by name (full phrase)")
    print("5) back")

def band_interact():
    local_loop = 1
    while local_loop == 1:
        clear()
        print("BAND ACTIONS\n")
        print_actions_menu()
        try:
            n = int(input("action: "))
            if n == 1:
                clear()
                print("BAND ACTIONS\n")
                print_actions_menu()
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
                    current_datbase.add_band(b)
                    print("added")                 
                except Exception as e:
                    print("%s" % e)
                input()
            elif n == 2:
                clear()
                print("BAND ACTIONS\n")
                print_actions_menu()
                try:
                    id = input("id: ")
                    band = current_datbase.get_band_by_id(int(id))
                    band.print_self()
                    input()
                except Exception as e: 
                    print("%s" % e)
                    input()
            elif n == 3:
                clear()
                print("BAND ACTIONS\n")
                print_actions_menu()
                try:
                    id = input("id: ")
                    band = current_datbase.get_band_by_id(int(id))
                    print("old entity")
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
                    current_datbase.edit_band(id, b)
                    input()
                except Exception as e: 
                    print("%s" % e)
                    input()
            elif n == 4:
                clear()
                print("BAND ACTIONS\n")
                print_actions_menu()
                id = input("id: ")
                if current_datbase.delete_band_by_id(id):
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

def select_entity_menu():
    local_loop = 1
    while local_loop == 1:
        clear()
        print("You are in entity selection menu")
        print("1) band")
        print("2) album")
        print("3) song")
        print("4) back")
        try:
            n = int(input("select: "))
            if n == 1:
                band_interact()
            elif n == 4:
                local_loop = 0
        except Exception as e:
            print("%s" % e)
            input()


def get_all_menu():
    local_loop = 1
    while local_loop == 1:
        clear()
        print("you are at 'get all' menu")
        print("1) band")
        print("2) album")
        print("3) song")
        print("4) back")
        try:
            n = int(input("select: "))
            if n == 1:
                print('bands')
                bands = current_datbase.select_all('bands')
                for b in bands:
                    print(b)
                input()
            elif n == 2:
                print('albums')
                albums = current_datbase.select_all('albums')
                for a in albums:
                    print(a)
                input()
            elif n == 3:
                print('songs')
                songs = current_datbase.select_all('songs')
                for s in songs:
                    print(s)
                input()
            elif n == 4:
                local_loop = 0
        except Exception as e:
            print("%s" % e)
            input()
    

loop = 1

while loop == 1:
    clear()
    print_main_menu()
    n = input("choice: ")
    try:
        n = int(n)
        if n == 1:
            clear()
            select_entity_menu()
        elif n == 2:
            clear()
            get_all_menu()
        elif n == 3:
            clear()
        elif n == 4:
            loop = 0
        else:
            print("wrong choice")
            input()

    except Exception as e:
        print("%s" % e)
        input()

