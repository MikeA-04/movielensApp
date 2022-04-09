# Name: Mike Apreza
# NetID: maprez3
# CS 341 - Project 02 Part 02
#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  # Constructor with all parameters
  def __init__(self, id, title, releaseYear):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = releaseYear
  # Properties
  @property
  def Movie_ID(self):
    return self._Movie_ID
  @property
  def Title(self):
    return self._Title
  @property
  def Release_Year(self):
    return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  # Constructor with all parameters
  def __init__(self, id, title, releaseYear, numReviews, avgRating):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = releaseYear
    self._Num_Reviews = numReviews
    self._Avg_Rating = avgRating
  # Properties
  @property
  def Movie_ID(self):
    return self._Movie_ID
  @property
  def Title(self):
    return self._Title
  @property
  def Release_Year(self):
    return self._Release_Year
  @property
  def Num_Reviews(self):
    return self._Num_Reviews
  @property
  def Avg_Rating(self):
    return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  # Constructor with all parameters
  def __init__(self, id, title, releaseDate, runtime, origLang, budget, revenue, numReviews, avgRating, tagline, genres, prodCompanies):
    self._Movie_ID = id
    self._Title = title
    self._Release_Date = releaseDate
    self._Runtime = runtime
    self._Original_Language = origLang
    self._Budget = budget
    self._Revenue = revenue
    self._Num_Reviews = numReviews
    self._Avg_Rating = avgRating
    self._Tagline = tagline
    self._Genres = genres
    self._Production_Companies = prodCompanies
  # Properties
  @property
  def Movie_ID(self):
    return self._Movie_ID
  @property
  def Title(self):
    return self._Title
  @property
  def Release_Date(self):
    return self._Release_Date
  @property
  def Runtime(self):
    return self._Runtime
  @property
  def Original_Language(self):
    return self._Original_Language
  @property
  def Budget(self):
    return self._Budget
  @property
  def Revenue(self):
    return self._Revenue
  @property
  def Num_Reviews(self):
    return self._Num_Reviews
  @property
  def Avg_Rating(self):
    return self._Avg_Rating
  @property
  def Tagline(self):
    return self._Tagline
  @property
  def Genres(self):
    return self._Genres
  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  # Write the sql
  sql = "SELECT COUNT(Movie_ID) FROM Movies;"
  # Get the value
  total = datatier.select_one_row(dbConn, sql)[0]
  if (total == None): # If error
    return -1
  else:
    return total


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  # Write the sql
  sql = "SELECT COUNT(Rating) FROM Ratings"
  # Get the value
  total = datatier.select_one_row(dbConn, sql)[0]
  if (total == None): # If error
    return -1
  else:
    return total


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all movies.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  movies = []
  # Write the sql
  sql = "SELECT Movie_ID, Title, strftime('%Y', DATE(Release_Date)) FROM Movies WHERE Title LIKE ? ORDER BY Title ASC;"
  # Get the value
  rows = datatier.select_n_rows(dbConn, sql, [pattern])
  if (rows == None): # If error
    return movies
  elif (len(rows) == 0):
    return movies
  else:
    # Store them into objects
    for r in rows:
      movies.append(Movie(r[0], r[1], r[2]))
    return movies


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  # Check if the move_id exists
  check = "SELECT * FROM Movies WHERE Movie_ID = ?;"
  exists = datatier.select_one_row(dbConn, check, [movie_id])
  if (exists == None):
    return None
  elif(len(exists) == 0):
    return None
  # Write the sql for most of the details
  sql = "SELECT Movies.Movie_ID, Title, DATE(Release_Date), Runtime, Original_Language, Budget, Revenue, (CASE WHEN Tagline IS NULL THEN '' ELSE Tagline END) FROM Movies LEFT JOIN Movie_Taglines ON(Movies.Movie_ID = Movie_Taglines.Movie_ID) WHERE Movies.Movie_ID = ?;"
  # Write the sql for the ratings
  sql4 = "SELECT COUNT(Rating), (CASE WHEN COUNT(Rating) IS 0 THEN 0.0 ELSE AVG(Rating) END) FROM Ratings WHERE Movie_ID = ?;"
  # Write the sql for the genres
  sql2 = "SELECT Genre_Name FROM Genres INNER JOIN Movie_Genres ON(Genres.Genre_ID = Movie_Genres.Genre_ID) WHERE Movie_ID = ? ORDER BY Genre_Name ASC;"
  # Write the sql for the production companies
  sql3 = "SELECT Company_Name FROM Companies INNER JOIN Movie_Production_Companies ON(Companies.Company_ID = Movie_Production_Companies.Company_ID) WHERE Movie_ID = ? ORDER BY Company_Name ASC;"
  # Get the value
  row = datatier.select_one_row(dbConn, sql, [movie_id])
  rate = datatier.select_one_row(dbConn, sql4, [movie_id])
  gen = datatier.select_n_rows(dbConn, sql2, [movie_id])
  production = datatier.select_n_rows(dbConn, sql3, [movie_id])
  if (row == None): # If error
    return None
  elif (len(row) == 0):
    return None
  else:
    # Store the genres and production companies into a list
    genres = []
    prodCompanies = []
    for g in gen:
      genres.append(g[0])
    for p in production:
      prodCompanies.append(p[0])
    # Store all the data into the object to return
    return MovieDetails(row[0], row[1], row[2], row[3], row[4], row[5], row[6], rate[0], rate[1], row[7], genres, prodCompanies)
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  movies = []
  # Write the sql
  sql = "SELECT Movies.Movie_ID, Title, strftime('%Y', DATE(Release_Date)), COUNT(Rating), AVG(Rating) FROM Movies INNER JOIN Ratings ON(Movies.Movie_ID = Ratings.Movie_ID) GROUP BY Movies.Movie_ID HAVING COUNT(Rating) >= ? ORDER BY AVG(Rating) DESC LIMIT ?;"
  # Get the data
  rows = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])
  # Store it into and return the object
  if (rows == None):
    return movies
  elif (len(rows) == 0):
    return movies
  else:
    for r in rows:
      movies.append(MovieRating(r[0], r[1], r[2], r[3], r[4]))
    return movies

##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  # Check if the ratings is valid
  if (rating < 0 or rating > 10):
    return 0
  # Check if the move_id exists
  sql = "SELECT * FROM Movies WHERE Movie_ID = ?;"
  exists = datatier.select_one_row(dbConn, sql, [movie_id])
  if (exists == None):
    return 0
  elif (len(exists) == 0):
    return 0
  else: # Then it is valid
    sql = "INSERT INTO Ratings(Movie_ID, Rating) Values(?, ?);"
    ex = datatier.perform_action(dbConn, sql, [movie_id, rating])
    if (ex < 1):
      return 0
    else:
      return ex


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  # Check if the move_id exists
  sql = "SELECT * FROM Movies WHERE Movie_ID = ?;"
  exists = datatier.select_one_row(dbConn, sql, [movie_id])
  if (exists == None):
    return 0
  elif (len(exists) == 0):
    return 0
  # Check to see if the Movie_ID is in Movie_Taglines table
  sql = "SELECT * FROM Movie_Taglines WHERE Movie_ID = ?"
  exist = datatier.select_one_row(dbConn, sql, [movie_id])

  if (exist == None or len(exist) == 0):
    sql = "INSERT INTO Movie_Taglines (Movie_ID, Tagline) VALUES (?, ?);"
    ex = datatier.perform_action(dbConn, sql, [movie_id, tagline])
  else:
    sql = "UPDATE Movie_Taglines SET Tagline = ? WHERE Movie_ID = ?;"
    ex = datatier.perform_action(dbConn, sql, [tagline, movie_id])
    
  if (ex < 1):
    return 0
  else:
    return ex
