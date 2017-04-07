## Your name: Abril Vela
## The option you've chosen: Option 2

# Put import statements you expect to need here!
import unittest
import tweepy
import twitter_info # my personal private twitter_info
import json
import sqlite3
















# Write your test cases here.
class TestCases(unittest.TestCase):
  def test_twitter_caching(self):
    fstr = open("206_final_project_cache.json","r").read()
    self.assertTrue("Moonlight" in fstr) #Moonlight will be one of the search terms
 
 def test_get_user(self):
    tweets = open("206_final_project_cache.json","r").read()
    tweet = Tweet(tweets[0])
    user = tweet.get_twitter_user()
    self.assertTrue(tweet.user, user)

  


if __name__ == "__main__":
  unittest.main(verbosity=2)
## Remember to invoke all your tests...