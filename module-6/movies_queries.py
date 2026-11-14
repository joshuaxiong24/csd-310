# Joshua Xiong
# CSD310-309A Database Development and Use (2271-DD)
# November 21st, 2026


""" import statements """
import mysql.connector  # to connect
from mysql.connector import errorcode

import dotenv  # to use .env file
from dotenv import dotenv_values

# using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # not in .env file
}

db = None  # so the finally block is safe if the connection fails

try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database

    cursor = db.cursor()

    # Query 1: all fields from the studio table
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    studios = cursor.fetchall()

    print("-- DISPLAYING Studio RECORDS --")
    for studio in studios:
        print("Studio ID: {}\nStudio Name: {}\n".format(studio[0], studio[1]))

    # Query 2: all fields from the genre table
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    genres = cursor.fetchall()

    print("\n-- DISPLAYING Genre RECORDS --")
    for genre in genres:
        print("Genre ID: {}\nGenre Name: {}\n".format(genre[0], genre[1]))

    # Query 3: film names with a run time of less than two hours (120 minutes)
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    short_films = cursor.fetchall()

    print("\n-- DISPLAYING Short Film RECORDS --")
    for film in short_films:
        print("Film Name: {}\nRuntime: {}\n".format(film[0], film[1]))

    # Query 4: film names and directors, grouped (ordered) by director
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
    directors = cursor.fetchall()

    print("\n-- DISPLAYING Director RECORDS in Order --")
    for film in directors:
        print("Film Name: {}\nDirector: {}\n".format(film[0], film[1]))

    input("\n\nPress any key to continue...")

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """

    if db is not None:
        db.close()
