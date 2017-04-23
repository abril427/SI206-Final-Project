###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import unittest
import tweepy
import twitter_info # my personal private twitter_info
import json
import sqlite3
import requests


# Begin filling in instructions....


##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

##### END TWEEPY SETUP CODE


##### caching setup: 

CACHE_FNAME = "206_final_project_cache.json"
# Put the rest of your caching setup here:
try:
  cache_file = open(CACHE_FNAME,'r')
  cache_contents = cache_file.read()
  cache_file.close()
  CACHE_DICTION = json.loads(cache_contents)
except:
  CACHE_DICTION = {}

##### end caching setup

##### functions to get cached data from sources (Twitter and OMDB)

def twitterGetUserWithCaching(consumerKey, consumerSecret, accessToken, accessSecret, handle):
  results_url = api.user_timeline(id=handle)

  if handle in CACHE_DICTION: # if we've already made this request
    # print('using cache')
      # use stored response
    response_text = CACHE_DICTION[handle] # grab the data from the cache
  else: # otherwise
    # print('fetching')
    results = results_url
    CACHE_DICTION[handle] = results   

    #cache data
    cache_file = open('206_final_project_cache.json', 'w')
    cache_file.write(json.dumps(CACHE_DICTION))
    cache_file.close()

    response_text = CACHE_DICTION[handle] # whichver way we got the data, load it into a python object
  return response_text # and return it from the function!


def twitterGetSearchWithCaching(consumerKey, consumerSecret, accessToken, accessSecret, searchQuery):

  results_url = api.search(q=searchQuery)

  if ("twitter_"+searchQuery) in CACHE_DICTION: # if we've already made this request
    # print('using cache')
      # use stored response
    response_text = CACHE_DICTION["twitter_"+searchQuery] # grab the data from the cache
  else: # otherwise
    # print('fetching')
    results = results_url
    CACHE_DICTION["twitter_"+searchQuery] = results   

    #cache data
    jsonFile = open('206_final_project_cache.json', 'w')
    jsonFile.write(json.dumps(CACHE_DICTION))
    jsonFile.close()

    response_text = CACHE_DICTION["twitter_"+searchQuery] # whichver way we got the data, load it into a python object
  return response_text # and return it from the function!


def getMovieDataWithCaching(title):
  parameters = {'t': title}
  results_url = 'http://www.omdbapi.com/?'
  resp = requests.get(url=results_url, params=parameters)
  response = json.loads(resp.text)
  if ("omdb_"+title) in CACHE_DICTION: # if we've already made this request
      # use stored response
    response_text = CACHE_DICTION["omdb_" + title] # grab the data from the cache
  else: # otherwise
    results = response
    CACHE_DICTION["imdb_" + title] = results   

    #cache data
    cache_file = open('206_final_project_cache.json', 'w')
    cache_file.write(json.dumps(CACHE_DICTION))
    cache_file.close()

    response_text = CACHE_DICTION[title] # whichver way we got the data, load it into a python object
  return response_text # and return it from the function!



##### create class Tweet here with the following instance variables:
# user_id - this will represent the user who tweeted the tweet and will allow us to reference our users table
# text - this will represent the text of the tweet and will allow us to search for the movie’s mentioned/other material in the tweet
# tweet_id - this will represent the text of the tweet and will act as a primary key in our Tweets table in our database 

# define the following fucntions in class Tweet:
# get_twitter_user() - this fuction should assign the user to the instance variable user and return the value
# __str__()

##### create class TwitterUser here with the following instance variables:
# user_id - this will represent the user who tweeted the tweet and will allow us to reference our users table
# screen_name - twitter user screenname
# description- this will represent the twitter user description
# num_followers - containing the number of followers this user has


##### create class Movie here with the following instance variables:
# title - the title of the movie
# director - the name of the director 
# num_langs - the number of languages in the movie
# rating - the IMDB rating of the movie
# actors - a list of actors in the movie
class Movie():
  """object representing a Movie""" 
  def __init__(self, movie_dict={}):
    self.title = movie_dict['Title']
    self.director = movie_dict['Director']
    self.rating = movie_dict['imdbRating']
    self.actors = movie_dict['Actors']
    self.languages = movie_dict['Language']
     
# define the following fucntions in class Movie:
# search() - this function should search for the three chosen movies in the OMDB in the list and return an accumulate a list of resulting dictionaries
# __str__()


##### call caching functions to store API data (example of working caching functions)

userTweets = twitterGetUserWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, "umich")

searchedTweets = twitterGetSearchWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, "Moonlight")

searchMovies = getMovieDataWithCaching("Moonlight")

newMovie = Movie(searchMovies)

##### select three movie title search terms you will use and put them in a list
##### call search() on this list and save it into a variable movie_dict
##### iterate over movie_dict and create instances of Movie() for each dictornary 
##### call twitterGetSearchWithCaching() on the title of each movie
  ##### save the returning dictornary as an Tweet() instance and create alist of tweets 
##### record information using twitterGetUserWithCaching() about the user who tweeted the Tweet() and all users mentioned in each tweet
  ####create an instance of TwitterUser() for each user and save this into a list

##### START setup of database: 
conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()

# table Tweets, with columns:
# - tweet_id (containing the string id belonging to the Tweet itself, from the data you got from Twitter -- note the id_str attribute) -- this column should be the PRIMARY KEY of this table
# - text (containing the text of the Tweet)
# - user_id (an ID string, referencing the Users table, see below)
# - movie_title (containing the text of the movie title searched and contained in each tweet)
# - num_favs (containing the number of favorites that this tweet has received)
# - retweets (containing the integer representing the number of times the tweet has been retweeted)

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('CREATE TABLE Tweets (tweet_id STRING PRIMARY KEY, text TEXT, user_id STRING, movie_title TEXT, num_favs INTEGER, retweets INTEGER)')

# table Users, with columns:
# - user_id (containing the string id belonging to the user, from twitter data -- note the id_str attribute) -- this column should be the PRIMARY KEY of this table
# - screen_name (containing the screen name of the user on Twitter)
# - num_likes (containing the number of tweets that user has favorited)
# - description (text containing the description of that user on Twitter, e.g. "Lecturer IV at UMSI focusing on programming" or "I tweet about a lot of things" or "Software engineer, librarian, lover of dogs..." -- whatever it is. OK if an empty string)
# - num_tweets (containing the number of tweets a user has made in total)
# - num_followers (containing the number of followers this user has)

cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('CREATE TABLE Users (user_id STRING PRIMARY KEY, screen_name TEXT, num_likes INTEGER, description TEXT, num_tweets INTEGER, num_followers INTEGER)')

# table Movies, with columns:
# - movie_id (containing the id belonging to the movie itself, from the data you got from OMDB) -- this column should be the PRIMARY KEY of this table
# - movie_title (containing the text of the movie title of the movie)
# - director (containig the text of the name of the director of the movie)
# - num_langs (containing the number of languages the movie has in it)
# - rating (containing the REAL value of the rating of the movie)
# - top_actor (containg the text of the name of the top billed actor in the movie)

cur.execute('DROP TABLE IF EXISTS Movies')
cur.execute('CREATE TABLE Movies (movie_id STRING PRIMARY KEY, movie_title TEXT, director TEXT, num_langs INTEGER, rating REAL, top_actor TEXT)')



# You should load into the Users table:
# All of the users that are tweeting about the searched movies. 

userid = {}
for tweet in userTweets:
  key = tweet['user']['id_str']
  if key not in userid:
    userid = {key: '1'}
  
    cur.execute('INSERT INTO Users (user_id, screen_name, num_likes, description, num_tweets, num_followers) VALUES (?, ?, ?, ?, ?, ?)', (key, tweet['user']['screen_name'], tweet['user']['favourites_count'], tweet['user']['description'],tweet['user']['statuses_count'], tweet['user']['followers_count']))
    conn.commit() 

## You should load into the Movies table: 
## Info about the movie searched from the OMDB Api given a specific movie title 



## You should load into the Tweets table: 
## Info about all the tweets that you gather from the timeline of each search.

for tweet in searchedTweets['statuses']:
  query = searchedTweets['search_metadata']['query']
  cur.execute('INSERT INTO Tweets (tweet_id, text, user_id, movie_title, num_favs, retweets) VALUES (?, ?, ?, ?, ?, ?)', (tweet['id_str'], tweet['text'], tweet['user']['id_str'], query, tweet['favorite_count'], tweet['retweet_count']))
  conn.commit() 


##### After data is loaded into the three tables start data manipulation 

##### load the following querines: 
# use list comprehensions to get the len() of the description of each User 
# accumulation of dictionaries to see how many languages are used across movies 





### IMPORTANT: MAKE SURE TO CLOSE YOUR DATABASE CONNECTION AT THE END OF THE FILE HERE SO YOU DO NOT LOCK YOUR DATABASE (it's fixable, but it's a pain). ###
cur.close()


# Put your tests here, with any edits you now need from when you turned them in with your project plan.
class TwitterTests(unittest.TestCase):
  def test_twitter_search_term_caching(self):
    fstr = open("206_final_project_cache.json","r").read()
    self.assertTrue("twitter_Moonlight" in fstr) #Moonlight will be one of the search terms

  def test_twitter_user_caching(self):
    fstr = open("206_final_project_cache.json","r").read()
    self.assertTrue("umich" in fstr) #Moonlight will be one of the search terms

  def test_user_tweets_type(self):
    self.assertEqual(type(userTweets),type([]))

  def test_user_tweets_type2(self):
    self.assertEqual(type(userTweets[1]),type({"hi":3})) #check to see that object in list is a dictionary

#   def test__str__(self):
#     tweet_dict = {user_id: '898832', text: 'This is text', tweet_id: '982381', movie_title: 'This is the title', num_favs: 7, retweets: 10}
#     tweet = Tweet(tweet_dict)
#     tweet_str = tweet.__str__()
#     self.assertTrue("This tweet, 'This is a text', was tweeted tweeted by user 898832 and has 7 favorites and 10 retweets.", "This tweet, 'This is a text', was tweeted tweeted by user 898832 and has 7 favorites and 10 retweets.")

# class MovieTests(unittest.TestCase):
#   def test_type_searh(self):
#     self.assertEqual(type(self.search(["term1, term2, term3"])), type([{"hi": 1}]) )


# class DatabaseTests(unittest.TestCase):
#   def test_users(self):
#     conn = sqlite3.connect('finalproject.db')
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM Users');
#     result = cur.fetchall()
#     self.assertTrue(len(result)>=2,"Testing that there are at least 2 distinct users in the Users table")
#     conn.close()

#   def test_movies(self):
#     conn = sqlite3.connect('finalproject.db')
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM Movies');
#     result = cur.fetchall()
#     self.assertTrue(len(result) == 3,"Testing that there are at 3 distinct movies in the Movies table")
#     conn.close()

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
  unittest.main(verbosity=2)