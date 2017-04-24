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
import re
from collections import Counter

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
  if ("imdb_"+title) in CACHE_DICTION: # if we've already made this request
      # use stored response
    response_text = CACHE_DICTION["imdb_"+title] # grab the data from the cache
  else: # otherwise
    results = response
    CACHE_DICTION["imdb_"+title] = results   

    #cache data
    cache_file = open('206_final_project_cache.json', 'w')
    cache_file.write(json.dumps(CACHE_DICTION))
    cache_file.close()

    response_text = CACHE_DICTION["imdb_"+title] # whichver way we got the data, load it into a python object
  return response_text # and return it from the function!



##### create class Tweet here with the following instance variables:
# user_id - this will represent the user who tweeted the tweet and will allow us to reference our users table
# text - this will represent the text of the tweet and will allow us to search for the movie’s mentioned/other material in the tweet
# tweet_id - this will represent the text of the tweet and will act as a primary key in our Tweets table in our database 

# define the following fucntions in class Tweet:
# get_mentioned_users() - this fuction should find the twitter users that are mentioned in the tweet text
# __str__()
class Tweet():
  """object representing tweet"""
  def __init__(self, tweet_dict={}):
    self.user_id = tweet_dict['user']['id_str']
    self.text = tweet_dict['text']
    self.tweet_id = tweet_dict['id_str']
    self.user = tweet_dict['user']['screen_name']

  def get_mentioned_users(self):
    #match regex to get mentioned users
    mentioned_users = re.findall('\B\@([\w\-]+)', self.text)
    # for result in results:
      # mentioned_users.append(result.group(0))
    if len(mentioned_users) < 1:
      return 'no mentioned users'
    return mentioned_users



##### create class TwitterUser here with the following instance variables:
# user_id - this will represent the user who tweeted the tweet and will allow us to reference our users table
# screen_name - twitter user screenname
# description- this will represent the twitter user description
# num_followers - containing the number of followers this user has
class TwitterUser():
  """object representing a Twitter User"""
  def __init__(self, user_dict={}):
    self.user_id = user_dict['user']['id_str']
    self.screen_name = user_dict['user']['screen_name']
    self.description = user_dict['user']['description']
    self.num_followers = user_dict['user']['followers_count']



##### create class Movie here with the following instance variables:
# title - the title of the movie
# director - the name of the director 
# num_langs - the number of languages in the movie
# rating - the IMDB rating of the movie
# actors - a list of actors in the movie

# define the following fucntions in class Movie:
# __str__()
class Movie():
  """object representing a Movie""" 
  def __init__(self, movie_dict={}):
    self.title = movie_dict['Title']
    self.director = movie_dict['Director']
    self.rating = movie_dict['imdbRating']
    self.actors = movie_dict['Actors']
    self.languages = movie_dict['Language']
     

##### call caching functions to store API data (example of working caching functions)

userTweets = twitterGetUserWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, "umich")
# searchedTweets = twitterGetSearchWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, "Moonlight")
# searchMovies = getMovieDataWithCaching("Moonlight")
# newMovie = Movie(searchMovies)
# # print(searchedTweets['statuses'][1]) this is one tweet
# newTweet = Tweet(searchedTweets['statuses'][3])
# # print(userTweets[0]) #this is one User tweet
# # print(newTweet.get_mentioned_users())
# newUser = TwitterUser(userTweets[0])


##### select three movie title search terms you will use and put them in a list
movieTitlesSearch = ["Moonlight", "Swiss Army Man", "Lion"]


##### iterate over movie_dict and create instances of Movie() for each dictonary 
movie_dicts = [] #list of movie dictionaries 
for movie in movieTitlesSearch:
  resp_dict = getMovieDataWithCaching(movie)
  movie_dicts.append(resp_dict)

movies_list = [] #list of Movies instances
for movie in movie_dicts:
  new_movie = Movie(movie)
  movies_list.append(new_movie)


##### call twitterGetSearchWithCaching() on the title of each movie
twitterSearchResults = []
list_of_searches = []
for movie in movies_list:
  twitterSearchResults = twitterGetSearchWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, movie.title)
  list_of_searches.append(twitterSearchResults)

# ##### save the returning dictornary as an Tweet() instance and create alist of tweets  
tweet_list = []  
for tweet in twitterSearchResults['statuses']:
  newTweet = Tweet(tweet) #create Tweet instances based off the twitter search results for the movie information
  tweet_list.append(newTweet)


##### record information using twitterGetUserWithCaching() about the user who tweeted the Tweet() and all users mentioned in each tweet
tweet_users_list = []
for tweet in tweet_list:
  user = tweet.user
  tweet_users_list.append(user)
  mentioned_users = tweet.get_mentioned_users()
  if mentioned_users != 'no mentioned users':
    for user in mentioned_users:
      tweet_users_list.append(user)

####create an instance of TwitterUser() for each user and save this into a list
user_list = [] #list of TwitterUser instances
list_of_user_dicts = []
for user in tweet_users_list:
  user_resp_dict = twitterGetUserWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, user)
  list_of_user_dicts.append(user_resp_dict[0])
  new_user = TwitterUser(user_resp_dict[0])
  user_list.append(new_user)
#print(user_list) new list of Twitter Users is created for the ENTIRE neighborhood


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
cur.execute('CREATE TABLE Movies (movie_id STRING PRIMARY KEY, movie_title TEXT, director TEXT, languages STRING, rating REAL, top_actor TEXT, actors STRING)')



# You should load into the Users table:
# All of the users that are tweeting about the searched movies. 

userid = {}
for tweet in list_of_user_dicts:
  # key = tweet['user']['id_str']
  if tweet['user']['id_str'] not in userid:
    userid[tweet['user']['id_str']] = '1'

    cur.execute('INSERT INTO Users (user_id, screen_name, num_likes, description, num_tweets, num_followers) VALUES (?, ?, ?, ?, ?, ?)', (tweet['user']['id_str'], tweet['user']['screen_name'], tweet['user']['favourites_count'], tweet['user']['description'],tweet['user']['statuses_count'], tweet['user']['followers_count']))
    conn.commit() 

## You should load into the Movies table: 
## Info about the movie searched from the OMDB Api given a specific movie title 
for movie in movie_dicts:
  actors = movie['Actors']
  actors_list = re.findall('([A-Za-z]+\s[A-Za-z]*),', actors)
  top_billed_actor = actors_list[0]
  cur.execute('INSERT INTO Movies (movie_id, movie_title, director, languages, rating, top_actor, actors) VALUES (?, ?, ?, ?, ?, ?, ?)', (movie['imdbID'], movie['Title'], movie['Director'], movie['Language'], movie['imdbRating'], top_billed_actor, movie['Actors']))
  conn.commit()

## You should load into the Tweets table: 
## Info about all the tweets that you gather from the timeline of each search.

for search in list_of_searches:
  query = search['search_metadata']['query']
  for tweet in search['statuses']:
    cur.execute('INSERT INTO Tweets (tweet_id, text, user_id, movie_title, num_favs, retweets) VALUES (?, ?, ?, ?, ?, ?)', (tweet['id_str'], tweet['text'], tweet['user']['id_str'], query, tweet['favorite_count'], tweet['retweet_count']))
    conn.commit() 


##### After data is loaded into the three tables start data manipulation 
##### load the following possible querines: 
# use list comprehensions to get the len() of the description of each User 
# accumulation of dictionaries to see how many languages are used across movies 

query = "SELECT screen_name, num_tweets FROM Users WHERE num_followers > 1000"
cur.execute(query)
user_popularity = cur.fetchall()

query = "SELECT movie_title, actors FROM Movies"
cur.execute(query)
db_actors = cur.fetchall()
actor_dict = {}
for resp in db_actors:
  res = re.findall('([A-Za-z]+\s[A-Za-z]*),', resp[1])
  num_actors = len(res)
  actor_dict[resp[0]] = num_actors

query = "SELECT text, Users.screen_name FROM Tweets INNER JOIN Users ON Tweets.user_id = Users.user_id" #find the users who have tweeted tweets about the searched movies from all users in the User "neighborhood"
cur.execute(query)
joined_results = cur.fetchall()

descriptions_users = {}
query = "SELECT description, screen_name from Users"
cur.execute(query)
for row in cur:
  if row[0] != '':
    descriptions_users[row[1]] = str(row[0])


cnt = Counter()
most_common_chars = {}
for resp in db_actors:
  most_common_char = Counter(resp[0]).most_common(1)
  if resp[0] not in most_common_chars:
    most_common_chars[resp[0]] = most_common_char[0][0]

#####begin writing to output file 
output_file = open('206_final_output.txt', 'w')
output_file.write("TWITTER SUMMARY FOR OMDB: 4/24/17 \n")
output_file.write('\n')
output_file.write("The three movies being searched for in the omdb databse are: \n")

for movie in movieTitlesSearch:
  output_file.write(movie + "\n")
output_file.write("\nUsers with more than 1000 followers are the following: \n")

for user in user_popularity:
  output_file.write(user[0] + " has tweeted " + str(user[1]) + " tweets")
  output_file.write('\n')
    
for k in actor_dict:
  output_file.write("\n" + k + " has " + str(actor_dict[k]) + " top performing actors listed for this movie.")

output_file.write('\n')
for k in most_common_chars:
  output_file.write("\nThe most common character in the title of " + k + " is " + most_common_chars[k] + " (with arbitraty selection when most common appearance is 1)")

output_file.write('\n')
for result in joined_results:
  output_file.write("\nThe user " + result[1] + " has tweeted about one of the searched movie terms, this is their tweet: " + result[0])

output_file.write('\n\n')
output_file.write('The following users have descriptions listed on their Twitter profiles: \n')
for k in descriptions_users:
  output_file.write("\nThe user " + k + " has the following description: " + descriptions_users[k])


### IMPORTANT: MAKE SURE TO CLOSE YOUR DATABASE CONNECTION AT THE END OF THE FILE HERE SO YOU DO NOT LOCK YOUR DATABASE (it's fixable, but it's a pain). ###
cur.close()


# Put your tests here, with any edits you now need from when you turned them in with your project plan.
class TwitterTests(unittest.TestCase):
  def test_twitter_search_term_caching(self):
    fstr = open("206_final_project_cache.json","r").read()
    self.assertTrue("twitter_Moonlight" in fstr) #Moonlight will be one of the search terms

  def test_twitter_user_caching(self):
    fstr = open("206_final_project_cache.json","r").read()
    self.assertTrue("umich" in fstr) #umich data should be cached 

  def test_user_tweets_type(self):
    self.assertEqual(type(user_resp_dict),type([]))

  def test_user_tweets_type2(self):
    self.assertEqual(type(user_resp_dict[1]),type({"hi":3})) #check to see that object in list is a dictionary

  def test_mentioned_users(self):
    newTweet = Tweet(twitterSearchResults['statuses'][3])
    newTweet.text = "The missuses: Baroness Lloyd Webber & @VAMNit"
    self.assertEqual(newTweet.get_mentioned_users(), ['VAMNit'])

  def test_mentioned_users_is_zero(self):
    newTweet = Tweet(twitterSearchResults['statuses'][3])
    newTweet.text = "The missuses: Baroness Lloyd Webber "
    self.assertEqual(newTweet.get_mentioned_users(), 'no mentioned users')

  def test_mentioned_users_is_more_than_one(self):
    newTweet = Tweet(twitterSearchResults['statuses'][3])
    newTweet.text = "Exploring @Glitch's community for sharing code & projects, it's like the lovechild of @github & @scratch!"
    self.assertEqual(newTweet.get_mentioned_users(), ['Glitch', 'github', 'scratch'])

  def test_creation_of_Movie_instances(self):
    searchMovies = getMovieDataWithCaching("Lion King")
    newMovie = Movie(searchMovies)
    self.assertEqual(type(movies_list[0]), type(newMovie))

  def test_creation_of_Tweet_instances(self):
    searchedTweets = twitterGetSearchWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, "Moonlight")
    newTweet = Tweet(searchedTweets['statuses'][0])
    self.assertEqual(type(tweet_list[0]), type(newTweet))

  def test_creation_of_TwitterUser_instances(self):
    searchedUsers = twitterGetUserWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, "umich")
    newUser = TwitterUser(searchedUsers[0])
    self.assertEqual(type(user_list[0]), type(newUser))

class DatabaseTests(unittest.TestCase):
  def test_tweets(self):
    conn = sqlite3.connect('finalproject.db')
    cur = conn.cursor()
    cur.execute('SELECT movie_title FROM Tweets');
    results = cur.fetchall()
    titles = []
    for result in results:
      if result not in titles:
        titles.append(result)
    self.assertTrue(len(titles),3)
    conn.close()

  def test_users(self):
    conn = sqlite3.connect('finalproject.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users');
    result = cur.fetchall()
    self.assertTrue(len(result)>=2,"Testing that there are at least 2 distinct users in the Users table")
    conn.close()

  def test_movies(self):
    conn = sqlite3.connect('finalproject.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Movies');
    result = cur.fetchall()
    self.assertTrue(len(result) == 3,"Testing that there are at 3 distinct movies in the Movies table")
    conn.close()

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
  unittest.main(verbosity=2)