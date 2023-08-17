from requests_oauthlib import OAuth1Session
import os
import json
from dotenv import load_dotenv
import utils

payload = None

# get today's tweet

today = utils.get_current_date_string()
# today = utils.get_yesterday_date_string()
tweet_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", today, "tweet.txt")
with open(tweet_path, "r") as f:
    payload = {"text": f.read()}

load_dotenv()

consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Making the request
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json=payload,
)


# Saving the response as JSON
json_response = response.json()

tweet_response_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", today, "tweet_response.json")

with open(tweet_response_path, "w") as f:
    json.dump(json_response, f, indent=2)


print("Response code: {}".format(response.status_code))
if response.status_code != 201:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )
