import requests
import configparser
import hashlib
import xml.etree.ElementTree as ET
base_url = "https://ws.audioscrobbler.com/2.0"
config = configparser.ConfigParser()
api_key = config["keys"]["key"]
api_secret = config["keys"]["secret"]
loggedin = False

def requestauth(method, params):
    pass

def requestnoauth(method, params):
    fullparams = params.copy()
    fullparams["api_key"] = api_key
    fullparams["method"] = method
    fullparams["api_sig"] = makesignature(fullparams)
    r = requests.get(base_url, params=fullparams)
    tree = ET.parse(r.text)
    return tree.getroot()

def makesignature(params):
    keys = list(params.keys)
    keys.sort()
    string = ""
    for name in keys:
        string += name
        string += params[name]
    string += api_secret
    return md5(string)

def md5(text):
    h = hashlib.md5()
    h.update(text.encode("utf-8"))
    return h.hexdigest()

def login():
    request("auth.getToken")

def trackGetInfo(song_name, artist_name):
    setup()
    response = request("track.getInfo", {
        "artist": artist_name,
        "track": song_name
    })
    return {
        "title": response.find("./name").text,
        "artist": response.find("artist/name").text,
        "duration": int(response.find("./duration").text) / 1000,
        "streams": int(response.find("./playcount").text),
        "summary": response.find("wiki/summary").text,
        "tags": listify(response.findall("toptags/tags/name"))
    }

def listify(elements):
    strings = []
    for element in elements:
        strings.append(element.text)
    return strings

def setup():
    global loggedin
    if not loggedin:
        login()