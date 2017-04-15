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

  if searchQuery in CACHE_DICTION: # if we've already made this request
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

userTweets = twitterGetUserWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, "umich")

searchedTweets = twitterGetSearchWithCaching(consumer_key, consumer_secret, access_token, access_token_secret, "Easter")





# Put your tests here, with any edits you now need from when you turned them in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)