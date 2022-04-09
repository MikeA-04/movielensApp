# Name: Mike Apreza
# NetID: maprez3
# Class: CS 341
# Overview: This project overall uses Python3 and SQLite. This file
#   uses only Python3. There will be a loop asking the user to
#   input the command they want to execute. If "x", then the 
#   program will end. Else, the commands will run by calling on
#   functions, which will ask the user for further input.
#   Inside those functions, other functions would be called
#   to run all the queries.

import sqlite3
import objecttier

###########################################################  
#
# print_stats
# Given a connection to the MovieLens database, executes various
# functions to retrieve and output basic stats.
#
def print_stats(dbConn):
  # Get the data and print it out formatted
  print("General stats:")
  movies = objecttier.num_movies(dbConn)
  reviews = objecttier.num_reviews(dbConn)
  print("  # of movies:", f"{movies:,}")
  print("  # of reviews:", f"{reviews:,}")

###########################################################  
#
# getMovies
# Given a connection to the MovieLens database, ask the user
# for input and output the movies if any. If there are more
# than 100, a message will be shown. If None, an error 
# message will be shown.
#
def getMovies(dbConn):
  print()
  search = input("Enter movie name (wildcards _ and % supported): ")
  movies = objecttier.get_movies(dbConn, search)
  if (movies == None or len(movies) == 0): # Error or no movies
    print("\n")
    print("# of movies found: 0")
  elif (len(movies) > 100): # more than 100 movies
    print("\n")
    print("# of movies found:", len(movies))
    print()
    print("There are too many movies to display, please narrow your search and try again...")
  else:
    print("\n")
    print("# of movies found:", len(movies))
    for m in movies:
      print(m.Movie_ID, ":", m.Title, f"({m.Release_Year})")

###########################################################  
#
# getMovieDetails
# Given a connection to the MovieLens database, ask the user
# for a movie id and output the details. If None, an error 
# message will be shown.
#
def getMovieDetails(dbConn):
  print()
  id = input("Enter movie id:")
  d = objecttier.get_movie_details(dbConn, id)
  if (d == None):
    print("\nNo such movie...")
  else:
    print()
    print(d.Movie_ID, ":", d.Title)
    print("  Release date:", d.Release_Date)
    print("  Runtime:", d.Runtime, "(mins)")
    print("  Orig language:", d.Original_Language)
    print("  Budget:", f"${d.Budget:,}", "(USD)")
    print("  Revenue:", f"${d.Revenue:,}", "(USD)")
    print("  Num reviews:", d.Num_Reviews)
    print("  Avg rating:", f"{d.Avg_Rating:.2f}", "(0..10)")
    print("  Genres:", end=" ")
    if (d.Genres == []):
      print("\n")
    else:
      for g in d.Genres:
        print(g + ", ", end="")
    print("\n")
    print("  Production companies:", end=" ")
    if (d.Production_Companies == []):
      print("\n")
    else:
      for pd in d.Production_Companies:
        print(pd + ", ", end="")
    print("\n")
    print("  Tagline:", d.Tagline)
  print("\n")

###########################################################  
#
# topNmovies
# Given a connection to the MovieLens database, ask the user
# for the top N movies with X reviews. If None or and empty list,
# nothing is shown.
#
def topNmovies(dbConn):
  print("\n")
  # Get first value and validate it
  num = int(input("N? "))
  if (num <= 0):
    print("Please enter a positive value for N...\n")
    return
  # Get second value and validate it
  reviews = int(input("min number of reviews? "))
  if (reviews < 1):
    print("Please enter a positive value for min number of reviews...\n")
    return
  # Else, both are valid
  movies = objecttier.get_top_N_movies(dbConn, num,reviews)
  # Check to see the results
  if (movies == None or movies == []):
    print()
  else:
    print("\n")
    for m in movies:
      # Movie_ID: int
      #   Title: string
      #   Release_Year: string
      #   Num_Reviews: int
      #   Avg_Rating: float
      print(m.Movie_ID, ":", m.Title, f"({m.Release_Year}),", "avg rating =", f"{m.Avg_Rating:.2f}", f"({m.Num_Reviews} reviews)")
    print()

###########################################################  
#
# insertReview
# Given a connection to the MovieLens database, ask the user
# for the rating they want to insert. If valid, then asks for
# the movie id. If neither valid, error message is shown 
# after each input (only one can be shown).
#
def insertReview(dbConn):
  rating = int(input("\nEnter rating (0..10): "))
  if (rating < 0 or rating > 10):
    print("Invalid rating...\n")
    return
  id = input("Enter movie id: ")
  result = objecttier.add_review(dbConn, id, rating)
  # Check to see if successfully added
  if (result == 0):
    print("\nNo such movie...")
  else:
    print("\nReview successfully inserted")
  print("\n")

###########################################################  
#
# setTagline
# Given a connection to the MovieLens database, ask the user
# for the tagline they want to insert. Then, it asks for
# the movie id. If the id isn't valid, error message is shown 
# after each input (only one can be shown). If valid, a success
# message is shown.
#
def setTagline(dbConn):
  print("\n")
  tagline = input("tagline? ")
  id = input("movie id?")
  result = objecttier.set_tagline(dbConn, id, tagline)
  # Check to see if it was done
  if (result == 0):
    print("\nNo such movie...")
  else:
    print("\nTagline successfully set")
  print()

#############################################################
#
# main
#
print('** Welcome to the MovieLens app **')
print()

dbConn = sqlite3.connect('MovieLens.db')

# print basics
print_stats(dbConn)

# Go into the loop
cmd = input("\nPlease enter a command (1-5, x to exit): ")
while (cmd != "x"):
  if (cmd == "1"):
    getMovies(dbConn)
  elif (cmd == "2"):
    getMovieDetails(dbConn)
  elif (cmd == "3"):
    topNmovies(dbConn)
  elif (cmd == "4"):
    insertReview(dbConn)
  elif (cmd == "5"):
    setTagline(dbConn)
  else:
    print("**Error, unknown command, try again...\n")
  # Ask for input again
  cmd = input("\nPlease enter a command (1-5, x to exit): ")


#
# done
#