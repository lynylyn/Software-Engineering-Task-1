import requests
import configparser
base_url = "https://ws.audioscrobbler.com/2.0"
config = configparser.ConfigParser()

network = pylast.LastFMNetwork(
    api_key=config["keys"]["key"]
    api_secret=config["keys"]["secret"]
)
