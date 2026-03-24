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

def searchArtist():
    artist_name = loginput("\nPlease input the artist name.\n")
    artist = client.artistGetInfo(artist_name)
    print(formatartist(artist))
    user_choice = loginput("\n[1] Find similar artists\n[2] Search for another artist\n[3] Return to menu\n")
    if user_choice == "1":
        findSimilarArtists(artist_name)
    if user_choice == "2":
        searchArtist()

def searchTag():
    tag_name = loginput("\nPlease input the tag name.")
    #request api
    #output info
    user_choice = loginput("\n[1] Find similar tags\n[2] Search for another tag\n[3] Return to menu\n")
    if user_choice == "1":
        findSimilarTags(tag_name)
    if user_choice == "2":
        searchTag()

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
    print("Save")

# OPTIONS WITHIN OPTIONS
def findSimilarTracks(song_name,artist_name):
    #request api
    #output similar
    print(song_name, artist_name) #this is just a filler to see if params work

def findSimilarArtists(artist_name):
    #request api
    #output similar
    print(artist_name) #this is just a filler to see if params work

def findSimilarTags(tag_name):
    #request api
    #output similar
    print(tag_name) #this is just a filler to see if params work

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

def formatduration(seconds):
    return f"{seconds // 60:.0f}:{seconds % 60:02.0f}"

# SAVING
def loginput(prompt):
    response = input(prompt)
    stream = open('pastsessions.txt', 'at')
    stream.write(f"{prompt}: {response}")
    return response