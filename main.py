from funct import *
import client
client.setup()
while True:
    user_choice = loginput("\n[1] Search for a song\n[2] Search for an artist\n[3] Search for a tag\n[4] See top music\n[5] Save and exit\n")
    if user_choice == "1":
        searchSong()
    elif user_choice == "2":
        searchArtist()
    elif user_choice == "3":
        searchTag()
    elif user_choice == "4":
        seeCharts()
    elif user_choice == "5":
        save()
    else:
        print("The selection was invalid.")