from funct import *
import client
client.setup()
user_name = input("Please input your name.\n")
while True:
    user_choice = loginput("\n[1] Search for a song\n[2] Search for an artist\n[3] Search for a tag\n[4] See top music\n[5] Save and exit\n[6] Request help\n")
    if user_choice == "1":
        searchSong()
    elif user_choice == "2":
        searchArtist()
    elif user_choice == "3":
        searchTag()
    elif user_choice == "4":
        seeCharts()
    elif user_choice == "5":
        save(user_name)
    elif user_choice == "6":
        user_choice = input("What do you need help with?\n[1] - Beginning\n[2] - Bugs\n[3] - Controls\n")
        if user_choice == "1":
            print("To get started, head back to the menu, and input the number beside the action you'd like to carry out. If it's your first time, I'd suggest hitting '1' and pressing enter to search for a song of your choice.")
        elif user_choice == "2":
            print("Please submit any bug reports via email - @evelyn.starling@education.nsw.gov.au")
        elif user_choice == "3":
            print("The controls are pretty simple. Press one of the numbers beside an option in the menu presented, and input tracks, songs, and tag names when prompted.")
        else:
            print("Sorry, that selection was invalid.")
    else:
        print("The selection was invalid.")