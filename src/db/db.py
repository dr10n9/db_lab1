import sys
import psycopg2
import psycopg2.extras
import random
import string

from entities.album import Album
from entities.band import Band
from entities.track import Track
from entities.band import Genres

class Database:
    connection = None
    cursor = None

    def connect(self, databaseName):
        try:
            self.connection = psycopg2.connect(
                host='127.0.0.1',
                dbname=databaseName,
                user='postgres',
                password='1'
            )
            self.cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print("%s" % (e))

    def select_all(self, tableName):
        if(self.cursor != None):
            try:
                self.cursor.execute("SELECT * FROM %s" % (tableName))
                rows = self.cursor.fetchall()
                if len(rows) == 0:
                    print("table is empty")
                else:
                    return rows
            except Exception as e:
                print("%s" % (e))
        else:
            print('err')

    def add_band(self, band):
        if(self.cursor != None):
            query = self.cursor.mogrify(
                "INSERT INTO bands (name, genre, exists) VALUES(%s, %s, %s)", (band.name, band.genre, band.exists))
            self.cursor.execute(query)
            self.connection.commit()
        else:
            print('err')

    #add_block

    def add_song(self, album_id, song):
        if self.cursor != None:
            query = self.cursor.mogrify(
                "INSERT INTO songs (name, length) VALUES(%s, %s)", (song.name, song.length)
            )
            self.cursor.execute(query)
            album_new = self.get_album_by_id(album_id)
            album_new.tracksCount += 1
            self.connection.commit()
            song_id = self.get_song_id_by_name(song.name)
            query = self.cursor.mogrify(
                "INSERT INTO songalbum (songid, albumid) VALUES(%s, %s)", (song_id, album_id)
            )
            self.cursor.execute(query)
            self.connection.commit()
            self.edit_album(album_id, album_new)

    def add_album(self, band_id, album):
        if self.cursor != None:
            query = self.cursor.mogrify(
                "INSERT INTO albums (name, trackscount) VALUES(%s, %s)", (album.name, album.tracksCount))
            self.cursor.execute(query)
            self.connection.commit()
            album_id = self.get_album_id_by_name(album.name)
            query = self.cursor.mogrify(
                "INSERT INTO bandalbum (bandid, albumid) VALUES (%s, %s)", (band_id, album_id))
            self.cursor.execute(query)
            self.connection.commit()
        else:
            print("err")

    #edit_block

    def edit_band(self, band_id, updated):
        if(self.cursor != None):
            try:
                self.cursor.execute(self.cursor.mogrify("UPDATE bands SET name='%s', genre='%s', exists='%s' WHERE id='%s'" % (
                    updated.name, updated.genre, updated.exists, band_id)))
                self.connection.commit()
            except Exception as e:
                print("%s" % e)
        else:
            print('err')

    def edit_album(self, album_id, updated_album):
        try:
            query = self.cursor.mogrify(
                "UPDATE albums SET name='%s', trackscount='%s' WHERE id='%s'" % (
                    updated_album.name, updated_album.tracksCount, album_id))
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print("%s" % e)
    
    def edit_song(self, song_id, updated_song):
        try:
            query = self.cursor.mogrify(
                "UPDATE songs SET name='%s', length='%s' WHERE id = '%s'" % (
                    updated_song.name, updated_song.length, song_id
                ))
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print("%s" % e)
            return False

    #delete_block
    def delete_band_by_id(self, band_id):
        try:
            query = self.cursor.mogrify(
                "DELETE FROM bandalbum WHERE bandid='%s'" % band_id
            )
            self.cursor.execute(query)
            query = self.cursor.mogrify(
                "DELETE FROM bands WHERE id='%s'" % band_id
            )
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print("%s" % e)
            return False

    def delete_song_by_id(self, song_id):
        try:
            query = self.cursor.mogrify(
                "DELETE FROM songalbum WHERE songid='%s'" % song_id
            )
            self.cursor.execute(query)
            query = self.cursor.mogrify(
                "DELETE FROM songs WHERE id='%s'" % song_id
            )
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print("%s" % e)
            return False

    def delete_album_by_id(self, album_id):
        try:
            query = self.cursor.mogrify(
                "DELETE FROM songalbum WHERE songid='%s'" % album_id
            )
            self.cursor.execute(query)
            query = self.cursor.mogrify(
                "DELETE FROM bandalbum WHERE songid='%s'" % album_id
            )
            self.cursor.execute(query)
            query = self.cursor.mogrify(
                "DELETE FROM albums WHERE id='%s'" % album_id
            )
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print("%s" % e)
            return False


    #get_block

    def get_band_by_name(self, band_name):
        try:
            self.cursor.execute(
                "SELECT * FROM bands where name='%s'" % band_name)
            res = self.cursor.fetchall()
            print(res)
            if len(res) != 0:
                res = res[0]
                res = Band(res[1], res[2], res[3], res[0])
                return res
        except Exception as e:
            print("%s" % e)
            return None

    def get_band_by_id(self, band_id):
        try:
            query = self.cursor.mogrify("SELECT * FROM bands where id='%s'" % band_id)
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            if len(res) != 0:
                res = res[0]
                res = Band(res[1], self.__genre_from_string(res[2]), res[3], res[0])
                return res
        except Exception as e:
            print("%s" % e)
            return None     

    def get_album_by_id(self, album_id):
        try:
            self.cursor.execute(
                "SELECT * FROM albums WHERE id='%s'" % album_id)
            res = self.cursor.fetchall()
            if len(res) != 0:
                res = res[0]
                res = Album(res[1], res[2], res[0])
                return res
        except Exception as e:
            print("%s" % e)
            return None

    def get_song_by_id(self, song_id):
        try:
            query = "SELECT * FROM songs WHERE id='%s'" % song_id
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            if len(res) != 0:
                res = res[0]
                res = Track(res[1], res[2], res[0])
                return res
        except Exception as e:
            print("%s" % e)
            return None

    def get_band_id_by_name(self, band_name):
        try:
            self.cursor.execute(self.cursor.mogrify(
                "SELECT id FROM bands WHERE name='%s'" % band_name))
            band_id = self.cursor.fetchall()
            if len(band_id) != 0:
                return band_id[0][0]
            else:
                return -1
        except Exception as e:
            print("%s" % e)
            return None

    def get_album_id_by_name(self, album_name):
        try:
            self.cursor.execute(self.cursor.mogrify(
                "SELECT id FROM albums WHERE name='%s'" % album_name))
            album_id = self.cursor.fetchall()
            if len(album_id) != 0:
                return album_id[0][0]
            else:
                return -1
        except Exception as e:
            print("%s" % e)
            return None
    
    def get_song_id_by_name(self, song_name):
        try:
            self.cursor.execute(self.cursor.mogrify(
                "SELECT id FROM songs WHERE name='%s'" % song_name))
            song_id = self.cursor.fetchall()
            if len(song_id) != 0:
                return song_id[0][0]
            else:
                return -1
        except Exception as e:
            print("%s" % e)
            return None

    #generate_random_entity_block

    def generate_random_band(self):
        b = Band(self.__generate_random_string(1, 15), self.__generate_random_genre(), random.choice([True, False]))
        return b

    def generate_random_album(self):
        a = Album(self.__generate_random_string(1, 10), 0)
        return a

    def generate_random_track(self):
        t = Track(self.__generate_random_string(1, 15), random.randint(60, 240))
        return t
    
    def fill_db_with_random_entities(self, quantity):
        bands = []
        albums = []
        songs = []
        for i in range(0, quantity):
            print(i)
            bands.append(self.generate_random_band())
            albums.append(self.generate_random_album())
            songs.append(self.generate_random_track())
        print(bands, "\n", albums, "\n", songs)

        for band in bands:
            self.add_band(band)
        
        for album in albums:
            self.add_album(bands[random.randint(0, quantity-1)].id, album)
            album.id = self.get_album_id_by_name(album.name)
        
        for song in songs:
            self.add_song(albums[random.randint(0, quantity-1)].id, song)

    # search+block

    def get_bands_by_exists_attr(self, exists: bool):
        try:
            query = self.cursor.mogrify("SELECT * FROM bands WHERE exists='%s'" % (exists))
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print('%s' % e)
            return None

    def get_bands_by_genre(self, genre: Genres):
        try:
            query = self.cursor.mogrify("SELECT * FROM bands WHERE genre='%s'" % genre.value)
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print('%s' % e)
            return None

    def search_by_word_not_belong(self, word):
        query = f"""SELECT * FROM bands WHERE to_tsvector(name) @@ to_tsquery('!{word}');"""
        self.cursor.execute(query)
        print('ok')
        return self.cursor.fetchall()

    # def search_by_phrase(self, phrase):
    #     query = f"""SELECT * FROM renting_list 
    #               JOIN renters USING(driver_license) 
    #               JOIN cars USING (car_number) 
    #               WHERE to_tsvector(model) @@ phraseto_tsquery('{phrase}');"""
    #     self.cursor.execute(query)
    #     return self.cursor.fetchall()

    @staticmethod
    def __generate_random_string(min: int, max: int):
        s = string.ascii_letters
        return ''.join(random.sample(s, random.randint(min, max)))       

    @staticmethod
    def __generate_random_genre():
        return random.choice(list(Genres))

    @staticmethod
    def __genre_from_string(str):
        if str == 'punk':
            return Genres.PUNK
        if str == 'rock':
            return Genres.ROCK
        if str == 'rap':
            return Genres.RAP
        if str == 'chanson':
            return Genres.CHANSON
        if str == 'classic':
            return Genres.CLASSIC