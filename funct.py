import client

# MENU OPTIONS
def searchSong():
    song_name = loginput("\nPlease input the song name.\n")
    artist_name = loginput("Please input the artist name.\n")
    track = client.trackGetInfo(song_name, artist_name)
    print(formattrack(track))
    user_choice = loginput("\n[1] Find similar songs\n[2] Search for another song\n[3] Return to menu\n")
    if user_choice == "1":
        findSimilarTracks(song_name,artist_name)
    if user_choice == "2":
        searchSong()
    if user_choice == "3":
        pass
    else:
        print("The selection was invalid. Returning to the menu.")

def searchArtist():
    artist_name = loginput("\nPlease input the artist name.\n")
    artist = client.artistGetInfo(artist_name)
    print(formatartist(artist))
    user_choice = loginput("\n[1] Find similar artists\n[2] Search for another artist\n[3] Return to menu\n")
    if user_choice == "1":
        findSimilarArtists(artist_name)
    if user_choice == "2":
        searchArtist()
    if user_choice == "3":
        pass
    else:
        print("The selection was invalid. Returning to the menu.")

def searchTag():
    tag_name = loginput("\nPlease input the tag name.\n")
    tag = client.tagGetInfo(tag_name)
    print(formattag(tag))
    tracks = client.tagGetTopTracks(tag_name)
    print("Top tracks from this tag:")
    print(formattagtracks(tracks))
    user_choice = loginput("\n[1] Find similar tags\n[2] Search for another tag\n[3] Return to menu\n")
    if user_choice == "1":
        findSimilarTags(tag_name)
    if user_choice == "2":
        searchTag()
    if user_choice == "3":
        pass
    else:
        print("The selection was invalid. Returning to the menu.")

def seeCharts():
    user_choice = loginput("[1] See top tracks\n[2] See top artists\n[3] See top tags\n[4] Return to menu\n")
    if user_choice == "1":
        #generate w matplotlib
        print("See top tracks")
    if user_choice == "2":
        #generate w matplotlib
        print("See top artists")
    if user_choice == "3":
        #generate w matplotlib
        print("See top tags")

def save():
    user_name = input("Please input your name.")
    stream = open('pastsessions.txt', 'at')
    stream.write(f"{prompt}: {response}")

# OPTIONS WITHIN OPTIONS
def findSimilarTracks(song_name,artist_name):
    tracks = client.trackGetSimilar(song_name, artist_name)
    print("Here are some similar tracks:")
    print(formatsimilartracks(tracks))

def findSimilarArtists(artist_name):
    artists = client.artistGetSimilar(artist_name)
    print("Here are some similar artists:")
    print(formatsimilarartists(artists))

def findSimilarTags(tag_name):
    tags = client.tagGetSimilar(tag_name)
    print("Here are some similar tags:")
    print(formatsimilartags(tags))

# FORMATTING
def formattrack(track):
    return f'''
{track["title"]} by {track["artist"]}
{formatduration(track["duration"])}
{track["streams"]} streams
This song is tagged as: {", ".join(track["tags"])}

{track["summary"]}
'''

def formatartist(artist):
    return f'''
{artist["title"]}
{artist["listeners"]} listeners
This artist is tagged as: {", ".join(artist["tags"])}

{artist["summary"]}
'''

def formattag(tag):
    return f'''
{tag["title"]}
This tag has been used {tag["total"]} times.

{tag["summary"]}
'''

def formattagtracks(tracks):
    s = ""
    for track in tracks:
        s = s + f'[{track["rank"]}]. {track["name"]} by {track["artist"]}\n'
    return s

def formatsimilartracks(tracks):
    s = ""
    for track in tracks:
        s = s + f'{track["name"]} by {track["artist"]}\n'
    return s

def formatsimilarartists(artists):
    s = ""
    for artist in artists:
        s = s + f'{artist["name"]}\n'
    return s

def formatsimilartags(tags):
    s = ""
    for tag in tags:
        s = s + f'{tag["name"]}\n'
    return s

def formatduration(seconds):
    return f"{seconds // 60:.0f}:{seconds % 60:02.0f}"

# SAVING
def loginput(prompt):
    response = input(prompt)
    stream = open('pastsessions.txt', 'at')
    stream.write(f"{prompt}: {response}")
    return response