import requests
import configparser
import hashlib
import xml.etree.ElementTree as ET
import webbrowser
base_url = "https://ws.audioscrobbler.com/2.0"
config = configparser.ConfigParser()
api_key = config["keys"]["key"]
api_secret = config["keys"]["secret"]
loggedin = False
session_key = None

def requestauth(method, params):
    fullparams = params.copy()
    fullparams["sk"] = session_key
    return requestnoauth(method, fullparams)

def requestnoauth(method, params):
    fullparams = params.copy()
    fullparams["api_key"] = api_key
    fullparams["method"] = method
    fullparams["api_sig"] = makesignature(fullparams)
    r = requests.get(base_url,
                     params=fullparams,
                     headers={"user-agent": "Evelyn Starling's Project <evechrsta@gmail.com>"})
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
    response = requestnoauth("auth.getToken", {})
    #lfm status ok ahhh error handling aahhh
    token = response.find("token").text
    webbrowser.open (f"http://www.last.fm/api/auth/?api_key={api_key}&token={token}")
    input("Please press enter to continue.")
    response = requestnoauth("auth.getSession", {"token": token})
    global session_key
    session_key = response.find("session/key").text


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