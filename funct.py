import client
import matplotlib.pyplot as plt
import textwrap
import session

# MENU OPTIONS
def searchSong():
    song_name = loginput("\nPlease input the song name.\n")
    artist_name = loginput("Please input the artist name.\n")
    try:
        track = client.trackGetInfo(song_name, artist_name)
    except RuntimeError as e:
        print(e)
        searchSong()
        return
    print(formattrack(track))
    user_choice = loginput("\n[1] Find similar songs\n[2] Search for another song\n[3] Return to menu\n")
    if user_choice == "1":
        findSimilarTracks(song_name,artist_name)
    elif user_choice == "2":
        searchSong()
    elif user_choice == "3":
        pass
    else:
        print("The selection was invalid. Returning to the menu.")

def searchArtist():
    artist_name = loginput("\nPlease input the artist name.\n")
    try:
        artist = client.artistGetInfo(artist_name)
    except RuntimeError as e:
        print(e)
        searchArtist()
        return
    print(formatartist(artist))
    user_choice = loginput("\n[1] Find similar artists\n[2] Search for another artist\n[3] Return to menu\n")
    if user_choice == "1":
        findSimilarArtists(artist_name)
    elif user_choice == "2":
        searchArtist()
    elif user_choice == "3":
        pass
    else:
        print("The selection was invalid. Returning to the menu.")

def searchTag():
    tag_name = loginput("\nPlease input the tag name.\n")
    try:
        tag = client.tagGetInfo(tag_name)
    except RuntimeError as e:
        print(e)
        searchTag()
        return
    print(formattag(tag))
    tracks = client.tagGetTopTracks(tag_name)
    print("Top tracks from this tag:")
    print(formattagtracks(tracks))
    user_choice = loginput("\n[1] Find similar tags\n[2] Search for another tag\n[3] Return to menu\n")
    if user_choice == "1":
        findSimilarTags(tag_name)
    elif user_choice == "2":
        searchTag()
    elif user_choice == "3":
        pass
    else:
        print("The selection was invalid. Returning to the menu.")

def seeCharts():
    user_choice = loginput("[1] See top tracks\n[2] See top artists\n[3] See top tags\n[4] Return to menu\n")
    if user_choice == "1":
        tracks = client.chartGetTopTracks()
        fig, ax = plt.subplots()
        ax.bar(findxtrackchart(tracks), findytrackchart(tracks))
        ax.set_ylabel('Listeners')
        ax.set_title('Top songs by listener count')
        ax.yaxis.get_major_formatter().set_scientific(False)
        plt.show()
    elif user_choice == "2":
        artists = client.chartGetTopArtists()
        fig, ax = plt.subplots()
        ax.bar(findxartistchart(artists), findyartistchart(artists))
        ax.set_ylabel('Listeners')
        ax.set_title('Top artists by listener count')
        ax.yaxis.get_major_formatter().set_scientific(False)
        plt.show()
    elif user_choice == "3":
        tags = client.chartGetTopTags()
        fig, ax = plt.subplots()
        ax.bar(findxtagchart(tags), findytagchart(tags))
        ax.set_ylabel('Reach')
        ax.set_title('Top tags by reach')
        ax.yaxis.get_major_formatter().set_scientific(False)
        plt.show()
    elif user_choice == "4":
        pass
    else:
        print("The selection was invalid.")
        seeCharts()

def save(user_name):
    user_choice = input("[1] - View your past sessions\n[2] - Save and exit this session\n")
    if user_choice == "1":
        sessions = session.loadsessions(user_name)
        if len(sessions) == 0:
            print("No sessions found.")
            return
        session_number = input(f"Choose a session between 1-{len(sessions)}.\n")
        id = int(session_number) - 1
        print("--PAST SESSIONS--\n\n")
        for record in sessions[id]:
            print(f"{record['prompt']}\n    {record['response']}")
    elif user_choice == "2":
        session.savesession(user_name)
    else:
        print("The selection was invalid.")
        save(user_name)

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

def findxtrackchart(tracks):
    x = []
    for track in tracks:
        x.append(textwrap.fill(f"{track['title']} by {track['artist']}", width=20))
    return x

def findytrackchart(tracks):
    y = []
    for track in tracks:
        y.append(track['listeners'])
    return y

def findxartistchart(artists):
    x = []
    for artist in artists:
        x.append(textwrap.fill(f"{artist['artist']}", width=20))
    return x

def findyartistchart(artists):
    y = []
    for artist in artists:
        y.append(artist['listeners'])
    return y

def findxtagchart(tags):
    x = []
    for tag in tags:
        x.append(textwrap.fill(f"{tag['name']}", width=20))
    return x

def findytagchart(tags):
    y = []
    for tag in tags:
        y.append(tag['reach'])
    return y

def formatduration(seconds):
    return f"{seconds // 60:.0f}:{seconds % 60:02.0f}"

# SAVING
def loginput(prompt):
    return session.loginput(prompt)