import requests
import configparser
import hashlib
import xml.etree.ElementTree as ET
import webbrowser
base_url = "https://ws.audioscrobbler.com/2.0/"
config = configparser.ConfigParser()
config.read("apikey.ini")
api_key = config["keys"]["key"]
api_secret = config["keys"]["secret"]
loggedin = False
session_key = None
debug = True

# AUTHENTICATION
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
    lfm = ET.XML(r.text)
    if lfm.attrib["status"] != "ok":
        raise RuntimeError(f"Last.FM said: {lfm.find('error').text}")
    if debug:
        print(r.text)
    return lfm.find('*')

def makesignature(params):
    keys = list(params.keys())
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
    token = response.text
    input("Press enter to be redirected to the login page.")
    webbrowser.open (f"http://www.last.fm/api/auth/?api_key={api_key}&token={token}")
    input("Please press enter to continue.")
    response = requestnoauth("auth.getSession", {"token": token})
    global session_key
    session_key = response.find("key").text
    global loggedin
    loggedin = True

# MENU FUNCTIONS
def trackGetInfo(song_name, artist_name):
    setup()
    response = requestauth("track.getInfo", {
        "artist": artist_name,
        "track": song_name
    })
    info = {
        "title": response.find("./name").text,
        "artist": response.find("artist/name").text,
        "duration": int(response.find("./duration").text) / 1000,
        "streams": int(response.find("./playcount").text),
        "tags": listify(response.findall("toptags/tag/name"))
    }
    summary = response.find("wiki/summary")
    if summary == None:
        info["summary"] = "There was no wiki summary available."
    else:
        info["summary"] = summary.text
    return info

def trackGetSimilar(song_name, artist_name):
    setup()
    response = requestauth("track.getSimilar", {
        "artist": artist_name,
        "track": song_name,
        "limit": "5"
    })
    tracks = []
    for track in response.findall("./track"):
        tracks.append({
            "name": track.find("./name").text,
            "artist": track.find("artist/name").text
        })
    return tracks

def artistGetInfo(artist_name):
    setup()
    response = requestauth("artist.getInfo", {
        "artist": artist_name
    })
    info = {
        "title": response.find("./name").text,
        "listeners": int(response.find("stats/listeners").text),
        "tags": listify(response.findall("tags/tag/name"))
    }
    summary = response.find("bio/summary")
    if summary == None:
        info["summary"] = "There was no bio available."
    else:
        info["summary"] = summary.text
    return info

def tagGetInfo(tag_name):
    setup()
    response = requestauth("tag.getInfo", {
        "tag": tag_name
    })
    info = {
        "title": response.find("./name").text,
        "total": int(response.find("./total").text)
    }
    summary = response.find("wiki/summary")
    if summary == None:
        info["summary"] = "There was no summary available."
    else:
        info["summary"] = summary.text
    return info

def tagGetTopTracks(tag_name):
    setup()
    response = requestauth("tag.getTopTracks", {
        "tag": tag_name,
        "limit": "5"
    })
    tracks = []
    for track in response.findall("./track"):
        tracks.append({
            "name": track.find("./name").text,
            "artist": track.find("artist/name").text,
            "rank": int(track.attrib["rank"])
        })
    return tracks

# MORE SETUP / AUTH
def setup():
    global loggedin
    global session_key
    if not loggedin:
        try:
            file = open('session_key.txt', 'r+')
            newkey = file.readline().strip()
            if newkey != "":
                session_key = newkey
                file.close()
                return
        except FileNotFoundError:
            file = open('session_key.txt', 'w')
        login()
        file.write(session_key + '\n')
        file.close()


def listify(elements):
    strings = []
    for element in elements:
        strings.append(element.text)
    return strings