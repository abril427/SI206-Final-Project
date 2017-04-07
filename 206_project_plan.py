## Your name: Abril Vela
## The option you've chosen: Option 2

# Put import statements you expect to need here!
import unittest
import tweepy
import twitter_info # my personal private twitter_info
import json
import sqlite3
















# Write your test cases here.
class TwitterDataTests(unittest.TestCase):
  def test_twitter_caching(self):
    fstr = open("206_final_project_cache.json","r").read()
    self.assertTrue("Moonlight" in fstr) #Moonlight will be one of the search terms
  
  def test_tweets_type(self):
    self.assertEqual(type(searched_tweets),type([]))

  def test_tweets_type2(self):
    self.assertEqual(type(searched_tweets[18]),type({"hi":3})) #check to see that object in list is a dictionary

  def test_get_user(self):
    tweets = open("206_final_project_cache.json","r").read()
    tweet = Tweet(tweets[0])
    user = tweet.get_twitter_user()
    self.assertTrue(tweet.user, user)

  def test__str__(self):
    tweet_dict = {user_id: '898832', text: 'This is text', tweet_id: '982381', movie_title: 'This is the title', num_favs: 7, retweets: 10}
    tweet = Tweet(tweet_dict)
    tweet_str = tweet.__str__()
    self.assertTrue("This tweet, 'This is a text', was tweeted tweeted by user 898832 and has 7 favorites and 10 retweets.", "This tweet, 'This is a text', was tweeted tweeted by user 898832 and has 7 favorites and 10 retweets.")

class Movie(unittest.TestCase):
  def test_type_searh(self):
    self.assertEqual(type(self.search(["term1, term2, term3"])), type([{"hi": 1}]) )


class DatabaseTests(unittest.TestCase):
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

if __name__ == "__main__":
  unittest.main(verbosity=2)
## Remember to invoke all your tests...